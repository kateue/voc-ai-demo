// frontend/src/api.js
const BASE = import.meta.env.VITE_BACKEND_URL || "http://localhost:10000";

export async function extractFeedback(text) {
    const res = await fetch(`${BASE}/api/extract`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
    });

    let body = null;
    try {
        body = await res.json();
    } catch {
        throw new Error(`Invalid JSON response from backend (${res.status})`);
    }

    if (!res.ok) {
        // bubble up server-provided error message when present
        const message = body?.message || body?.error || `Request failed (${res.status})`;
        throw new Error(message);
    }

    return body;
}
