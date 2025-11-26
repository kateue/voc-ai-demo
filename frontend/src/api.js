// frontend/src/api.js
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "https://your-backend-url.onrender.com";

export async function callExtractAPI(text) {
  const res = await fetch(`${BACKEND_URL}/api/extract`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text })
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API error: ${res.status} - ${body}`);
  }
  return res.json();
}
