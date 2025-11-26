# Voice of Customer — Pain Point Extractor

Small full‑stack demo that extracts and summarizes customer pain points from text feedback using OpenAI GPT-4o-mini. Users paste feedback into a simple React UI and receive structured JSON insights (summary, pain points with counts, themes, sentiment).

Live demo: https://vocaidemo.netlify.app

## Features
- Paste single or multiple feedback items and get a concise structured output.
- Backend: Flask calling OpenAI (gpt-4o-mini). 
- Frontend: React + Vite UI that displays results and backend errors. 
- Health endpoint for quick diagnostics.

## Repo layout
- backend/ — Flask API (app.py)
- frontend/ — React + Vite frontend

## Requirements
- Node.js (v16+)
- Python 3.10+ (recommended)
- An OpenAI API key with access to the model used

## Local development

### Backend
1. cd backend
2. Create & activate a venv:
   - PowerShell:
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
   - CMD:
     python -m venv .venv
     .\.venv\Scripts\activate.bat
3. Install deps:
   pip install -r requirements.txt
   (If no file exists: pip install flask flask-cors openai)
4. Set environment variable:
   - PowerShell: $env:OPENAI_API_KEY="sk-..."
   - CMD: set OPENAI_API_KEY=sk-...
5. Run:
   python app.py
6. Health: GET /health
   Default port: 10000 (honors PORT env var)

### Frontend
1. cd frontend
2. Install:
   npm install
3. Configure backend URL for dev / deploy:
   - Local: VITE_BACKEND_URL=http://localhost:10000
   - Netlify: set VITE_BACKEND_URL to the deployed backend URL
4. Run dev:
   npm run dev

## Deploy
- Backend: Render
  - Ensure OPENAI_API_KEY is set as an environment variable.
  - Confirm the service can make outbound requests to OpenAI.
- Frontend: Netlify 
  - Set VITE_BACKEND_URL to the backend public URL and redeploy.

## API
- GET /health
  - Response: { "status": "ok", "openai_key_set": true|false }

- POST /api/extract
  - Body: { "text": "customer feedback" }
  - Success: JSON { summary, pain_points, themes, sentiment }
  - Errors: Returns JSON with error and message fields (useful for debugging)

## Troubleshooting
- Error: missing_api_key — Set OPENAI_API_KEY on your backend host.
- OpenAI request failed — Check backend logs for auth/model/quota errors.
- Frontend shows backend messages directly in UI for easier debug.

## Example screenshots

**1) Sample UI input**  
![Here is an amazon review of a product](amazon-review.png)  

![Paste feedback into the text box and click "Extract Pain Points"](/voc-ui.png)  
Paste one or many customer feedback items and submit. Use the text box to add raw feedback and click **Extract Pain Points** to run analysis.

**2) Results view (JSON output)**  
![Results section showing summary, pain points, themes, and sentiment](/voc-results.png)  
The app returns a structured result:
- **Summary:** concise 1–2 sentence overview  
- **Pain points:** list of issues with counts (how many times each appears)  
- **Themes:** comma-separated topics extracted from the text  
- **Sentiment:** `positive` | `mixed` | `negative`

## Security & privacy
- Do not commit API keys.
- Avoid exposing secrets or full stack traces in production.
- This demo is not intended for sensitive or regulated data.

## Notes
- Uses GPT-4o-mini for demonstration; model access and quotas are subject to OpenAI account limitations.
