const API_URL = "http://127.0.0.1:8000/api/chat";

export async function sendMessage(payload) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Backend error");
  }

  return await response.json();
}
