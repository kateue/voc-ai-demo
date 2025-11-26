# backend/app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI


# Initialize
app = Flask(__name__)
CORS(app)

# Validate key at startup (so logs show immediately if missing)
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    app.logger.error("OPENAI_API_KEY is not set in environment. Set this in Render environment variables.")
    client = None
else:
    client = OpenAI(api_key=OPENAI_KEY)

# Add a simple health endpoint for quick checks
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "openai_key_set": bool(OPENAI_KEY)}), 200

# Prompt template and instructions
SYSTEM_PROMPT = """
You are an assistant that extracts customer pain points from feedback.
Return a JSON object only (no extra commentary) with the following schema:
{
  "summary": "Short 1-2 sentence summary of overall feedback",
  "pain_points": [
    {"text": "single pain point sentence", "count": integer},
    ...
  ],
  "themes": ["theme1", "theme2", ...],
  "sentiment": "positive|mixed|negative"
}
Count is how many times the pain point appears in the text. Group similar points together.
If input is empty, return an object with empty arrays and summary "".
Be concise and factual.
"""

def build_user_prompt(customer_text: str):
    return f"Customer feedback text:\n\n{customer_text}\n\nExtract pain points, count frequency, list themes, and give overall sentiment."

@app.route("/api/extract", methods=["POST"])
def extract():
    data = request.json or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({
            "summary": "",
            "pain_points": [],
            "themes": [],
            "sentiment": "mixed"
        })

    if not OPENAI_KEY or client is None:
        app.logger.error("Missing OpenAI API key on backend request attempt.")
        return jsonify({
            "error": "missing_api_key",
            "message": "OpenAI API key is not set on the backend. Set OPENAI_API_KEY in Render environment variables."
        }), 500

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(text)}
            ],
            max_tokens=600,
            temperature=0.0
        )
        content = resp.choices[0].message.get("content", "").strip()
        import json
        try:
            parsed = json.loads(content)
        except Exception:
            idx = content.find("{")
            if idx != -1:
                parsed = json.loads(content[idx:])
            else:
                parsed = {
                    "summary": content,
                    "pain_points": [],
                    "themes": [],
                    "sentiment": "mixed"
                }
        return jsonify(parsed)
    except Exception as e:
        app.logger.exception("OpenAI request failed")
        # return the actual error message so the frontend shows it (avoid returning secrets)
        return jsonify({
            "error": "backend_openai_error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
