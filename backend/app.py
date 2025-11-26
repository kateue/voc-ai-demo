# backend/app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI


# Initialize
app = Flask(__name__)
CORS(app)  # Allow calls from frontend domain; in production add origins list

# Use the official OpenAI client (set OPENAI_API_KEY in Render env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    # Make a chat completion request to GPT-4o-mini
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
        # The assistant's content should be a JSON string - parse it
        content = resp.choices[0].message.get("content", "").strip()
        # Attempt to return parsed JSON safely
        import json
        try:
            parsed = json.loads(content)
        except Exception:
            # If model returns text plus JSON, attempt to find first '{' and parse
            idx = content.find("{")
            if idx != -1:
                parsed = json.loads(content[idx:])
            else:
                # fallback minimal structured output
                parsed = {
                    "summary": content,
                    "pain_points": [],
                    "themes": [],
                    "sentiment": "mixed"
                }
        return jsonify(parsed)
    except Exception as e:
        # For dev visibility; in prod avoid returning full trace
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
