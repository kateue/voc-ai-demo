import React, { useState } from "react";
import { extractFeedback } from "./api";

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  async function handleSubmit(e) {
    e?.preventDefault?.();
    setErrorMessage(null);
    setLoading(true);
    setResult(null);

    try {
      const data = await extractFeedback(text);
      setResult(data);
    } catch (err) {
      setErrorMessage(err?.message || "Unexpected error. Try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <h1>Voice of Customer — Pain Point Extractor</h1>
      <p>Paste customer feedback (one or many comments). Click extract to see pain points and themes.</p>

      <form onSubmit={handleSubmit}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={10}
          placeholder="Paste feedback here..."
        />
        <div>
          <button type="submit" disabled={loading}>
            {loading ? "Extracting..." : "Extract Pain Points"}
          </button>
        </div>
      </form>

      {errorMessage && (
        <div style={{ color: "crimson", marginTop: 12 }}>
          Error: {errorMessage}
        </div>
      )}

      {result && (
        <div className="result">
          <h2>Summary</h2>
          <p>{result.summary}</p>

          <h3>Pain Points</h3>
          {result.pain_points && result.pain_points.length ? (
            <ul>
              {result.pain_points.map((p, i) => (
                <li key={i}>
                  {p.text} {p.count ? <em>({p.count})</em> : null}
                </li>
              ))}
            </ul>
          ) : (
            <p>No pain points found.</p>
          )}

          <h3>Themes</h3>
          <p>{(result.themes || []).join(", ")}</p>

          <h3>Sentiment</h3>
          <p>{result.sentiment}</p>
        </div>
      )}

      <footer>
        <small>Demo app — powered by GPT-4o-mini (OpenAI free tier). Your input is used for demo only.</small>
      </footer>
    </div>
  );
}
