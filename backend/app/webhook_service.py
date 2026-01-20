import asyncio
import json
import logging
import os
import time
import hmac
import hashlib
import random
from typing import Any, Dict, Optional

import httpx

from .store import Storage

logger = logging.getLogger("webhook_service")
logger.setLevel(os.getenv("WEBHOOK_LOG_LEVEL", "INFO"))
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s webhook:%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class WebhookClient:
    """Async webhook delivery client with HMAC signing, retries and logging.

    Usage:
      client = WebhookClient()
      await client.send(url, payload, secret=os.getenv('WEBHOOK_SECRET'))

    For non-blocking delivery in FastAPI handlers use `background_tasks.add_task(client.send, ...)`.
    """

    def __init__(self, storage: Optional[Storage] = None, client: Optional[httpx.AsyncClient] = None):
        self.storage = storage or Storage()
        self.client = client or httpx.AsyncClient(timeout=10)

    async def send(
        self,
        url: str,
        event: Dict[str, Any],
        secret: Optional[str] = None,
        max_retries: int = 4,
        timeout: int = 10,
        backoff_base: float = 0.5,
    ) -> Dict[str, Any]:
        """Send event payload to `url` with HMAC signing and retries.

        Returns a result dict with keys: `success`, `status_code`, `attempts`, `error`.
        """
        payload = event or {}
        payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        timestamp = str(int(time.time()))
        signature = self._sign(payload_json, timestamp, secret)

        headers = {
            "Content-Type": "application/json",
            "X-Timestamp": timestamp,
            "X-Signature": signature,
            "X-Event-Type": str(payload.get("event_type", "")),
        }

        attempt = 0
        last_error = None
        result = {"success": False, "status_code": None, "attempts": 0, "error": None}

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Sending webhook to {url}, attempt {attempt}")
                resp = await self.client.post(url, content=payload_json, headers=headers, timeout=timeout)
                result["status_code"] = resp.status_code
                result["attempts"] = attempt
                if 200 <= resp.status_code < 300:
                    result["success"] = True
                    logger.info(f"Webhook delivered to {url} (status={resp.status_code})")
                    # record a lightweight event log (do not include sensitive payload)
                    await self._log_event_sent(payload, url, resp.status_code)
                    return result
                else:
                    last_error = f"Non-2xx status: {resp.status_code}"
                    logger.warning(f"Webhook to {url} returned {resp.status_code}")
            except Exception as e:
                last_error = str(e)
                logger.exception(f"Error sending webhook to {url}: {e}")

            # Exponential backoff with jitter
            sleep_base = backoff_base * (2 ** (attempt - 1))
            jitter = random.uniform(0, sleep_base * 0.5)
            sleep_for = sleep_base + jitter
            logger.info(f"Retrying in {sleep_for:.2f}s (attempt {attempt}/{max_retries})")
            await asyncio.sleep(sleep_for)

        result["error"] = last_error
        logger.error(f"Failed to deliver webhook to {url} after {max_retries} attempts: {last_error}")
        # record failed attempt as event
        await self._log_event_failed(payload, url, last_error)
        return result

    def _sign(self, payload_json: str, timestamp: str, secret: Optional[str]) -> str:
        if not secret:
            return ""
        mac = hmac.new(secret.encode("utf-8"), msg=(timestamp + "." + payload_json).encode("utf-8"), digestmod=hashlib.sha256)
        return mac.hexdigest()

    async def _log_event_sent(self, payload: Dict[str, Any], url: str, status_code: int):
        try:
            evt = {
                "event_type": payload.get("event_type", "response_generated"),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "data": {"url": url, "status_code": status_code},
            }
            await self.storage.log_event(evt)
        except Exception:
            logger.exception("Failed recording webhook sent event")

    async def _log_event_failed(self, payload: Dict[str, Any], url: str, error: Optional[str]):
        try:
            evt = {
                "event_type": payload.get("event_type", "webhook_failed"),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "data": {"url": url, "error": error},
            }
            await self.storage.log_event(evt)
        except Exception:
            logger.exception("Failed recording webhook failed event")


_default_client: Optional[WebhookClient] = None


def get_default_webhook_client() -> WebhookClient:
    global _default_client
    if _default_client is None:
        _default_client = WebhookClient()
    return _default_client


async def send_webhook_background(url: str, event: Dict[str, Any], secret: Optional[str] = None):
    """Convenience wrapper that schedules the send in background (fire-and-forget)."""
    client = get_default_webhook_client()
    # schedule and don't await so caller can remain non-blocking
    asyncio.create_task(client.send(url, event, secret=secret))
