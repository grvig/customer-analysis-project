import { useState } from "react";
import { askQuestion } from "../services/aiService";

export default function AIAssistant() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const handleAsk = async () => {
    if (!question.trim()) return;

    try {
      setLoading(true);
      setResponse(null);

      const data = await askQuestion(question);

      setResponse(data);

      setHistory((prev) => [
        question,
        ...prev.filter((q) => q !== question).slice(0, 4),
      ]);
    } catch (error) {
      console.error(error);

      setResponse({
        sql: "Error",
        rows: [],
        answer: "Failed to retrieve data.",
      });
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
            <h3>User Question</h3>
            <p>{question}</p>
          </div>

          <div className="response-section">
            <h3>Generated SQL</h3>
            <pre>{response.sql}</pre>
          </div>

          <div className="response-section">
            <h3>Query Results</h3>
            <pre>
              {JSON.stringify(
                response.rows,
                null,
                2
              )}
            </pre>
          </div>

          <div className="response-section">
            <h3>AI Answer</h3>
            <p>{response.answer}</p>
          </div>
        </div>
      )}
    </div>
  );
}