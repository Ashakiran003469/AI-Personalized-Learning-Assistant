import os
import json
import uuid
from typing import Optional, Dict, Any
from datetime import datetime

from .services.supabase_service import SupabaseClient

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)


class Storage:
    """
    Storage wrapper:
    - Uses Supabase if available
    - Falls back to local JSON if Supabase fails
    """

    def __init__(self):
        self.supabase = SupabaseClient()

    # -----------------------------
    # READ LEARNER CONTEXT
    # -----------------------------
    async def get_user_context(self, user_id: Optional[str]) -> Dict[str, Any]:
        if not user_id:
            return {}

        if self.supabase.available():
            try:
                record = await self.supabase.get_learner(user_id)
                if record:
                    return record
            except Exception as e:
                print("❌ Supabase get_learner failed:", e)

        # Local fallback
        path = os.path.join(DATA_DIR, f"learner_{user_id}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        return {}

    # -----------------------------
    # CREATE LEARNER
    # -----------------------------
    async def create_learner(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inserts ONLY columns that exist in Supabase:
        - external_user_id
        - full_name
        - metadata
        - skill_levels
        - language_preference
        """

        external_user_id = user_info.get("external_user_id") or str(uuid.uuid4())

        record = {
            "external_user_id": external_user_id,
            "full_name": user_info.get("full_name"),
            "metadata": user_info.get("metadata") or {},
            "skill_levels": user_info.get("skill_levels"),          # nullable
            "language_preference": user_info.get("language_preference"),  # nullable
        }

        # 🔍 Debug visibility
        print("📤 INSERT learner payload →", record)

        if self.supabase.available():
            try:
                await self.supabase.insert_learner(record)
                return record
            except Exception as e:
                print("❌ Supabase insert_learner failed:", e)

        # Local JSON fallback
        path = os.path.join(DATA_DIR, f"learner_{external_user_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)

        return record

    # -----------------------------
    # UPDATE PROGRESS
    # -----------------------------
    async def update_progress(
        self,
        user_id: Optional[str],
        session_id: str,
        data: Dict[str, Any],
    ):
        record = {
            "learner_id": user_id or "anonymous",
            "session_id": session_id,
            "topic": data.get("topic"),
            "mastery_level": data.get("mastery_level"),
            "interaction_count": data.get("interaction_count"),
            "details": data,
            "created_at": datetime.utcnow().isoformat(),
        }

        if self.supabase.available():
            try:
                await self.supabase.insert_progress(record)
                return
            except Exception as e:
                print("❌ Supabase insert_progress failed:", e)

        # Local fallback
        path = os.path.join(DATA_DIR, "progress_log.jsonl")
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    # -----------------------------
    # LOG EVENTS
    # -----------------------------
    async def log_event(self, event: Dict[str, Any]):
        if self.supabase.available():
            try:
                await self.supabase.insert_event(event)
                return
            except Exception as e:
                print("❌ Supabase insert_event failed:", e)

        path = os.path.join(DATA_DIR, "events.jsonl")
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
