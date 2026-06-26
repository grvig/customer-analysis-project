import { useState } from "react";
import { askQuestion } from "../services/aiService";

export default function AIAssistant() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState(() => {
    try { return JSON.parse(localStorage.getItem("queryHistory") || "[]"); }
    catch { return []; }
  });

  const handleAsk = async () => {
    if (!question.trim()) return;

    try {
      setLoading(true);
      setResponse(null);
      setError(null);

      const data = await askQuestion(question);

      if (!data.success) {
        setError(data.error || "The AI could not answer this question.");
        return;
      }

      setResponse(data);

      setHistory((prev) => {
        const updated = [question, ...prev.filter((q) => q !== question).slice(0, 4)];
        localStorage.setItem("queryHistory", JSON.stringify(updated));
        return updated;
      });
    } catch (err) {
      setError("Could not reach the server. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="ai-banner">
        AI Business Intelligence Assistant
      </div>

      <h2>AI Assistant</h2>

      <p className="assistant-subtitle">
        Ask questions about customers, calls, services,
        complaints, revenue, surveys and branch performance.
      </p>

      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleAsk();
          }
        }}
        placeholder="Ask a question..."
      />

      <button
        onClick={handleAsk}
        disabled={loading}
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {loading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>
            Generating SQL and retrieving insights...
          </p>
        </div>
      )}

      {error && (
        <div className="error-box">
          <p>{error}</p>
        </div>
      )}

      {history.length > 0 && (
        <div className="history-box">
          <h3>Recent Queries</h3>

          {history.map((item, index) => (
            <p key={index}>{item}</p>
          ))}
        </div>
      )}

      {response && (
        <div className="result-box">
          <div className="response-section">
            <h3>AI Answer</h3>
            <p>{response.answer}</p>
          </div>

          {response.rows && response.rows.length > 0 && (
            <div className="response-section">
              <h3>Data</h3>
              <div style={{ overflowX: "auto" }}>
                <table className="results-table">
                  {response.columns && response.columns.length > 0 && (
                    <thead>
                      <tr>
                        {response.columns.map((col, i) => (
                          <th key={i}>{col}</th>
                        ))}
                      </tr>
                    </thead>
                  )}
                  <tbody>
                    {response.rows.map((row, i) => (
                      <tr key={i}>
                        {(Array.isArray(row) ? row : [row]).map((cell, j) => (
                          <td key={j}>{cell !== null && cell !== undefined ? String(cell) : "—"}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}