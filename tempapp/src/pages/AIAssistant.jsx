import { useState } from "react";
import { askQuestion } from "../services/aiService";

export default function AIAssistant() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);

  const handleAsk = async () => {
    const data = await askQuestion(question);
    setResponse(data);
  };

  return (
    <div>
      <h2>AI Assistant</h2>

      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question..."
      />

      <button onClick={handleAsk}>Ask</button>

      {response && (
        <div className="result-box">
          <h3>User Question</h3>
          <p>{question}</p>

          <h3>Generated SQL</h3>
          <pre>{response.sql}</pre>

          <h3>Query Results</h3>
          <pre>{JSON.stringify(response.rows, null, 2)}</pre>

          <h3>AI Answer</h3>
          <p>{response.answer}</p>
        </div>
      )}
    </div>
  );
}