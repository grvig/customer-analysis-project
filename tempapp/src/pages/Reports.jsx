import { useState } from "react";
import {
  generateReport,
  generateCustomReport,
  downloadPdfReport,
} from "../services/reportService";
import { API_BASE_URL } from "../services/api";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function Reports() {
  const [type, setType] = useState("complaint");
  const [report, setReport] = useState("");
  const [customQuestion, setCustomQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    try {
      setLoading(true);
      setError(null);

      const data = await generateReport(type);

      setReport(data.report);
    } catch (err) {
      setError("Failed to generate report. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleCustomReport = async () => {
    if (!customQuestion.trim()) return;

    try {
      setLoading(true);
      setError(null);

      const data = await generateCustomReport(customQuestion);

      setReport(data.report);
    } catch (err) {
      setError("Failed to generate custom report. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPdf = async () => {
    try {
      setError(null);
      const data = await downloadPdfReport(type);

      window.open(
        `${API_BASE_URL}${data.download_url}`,
        "_blank"
      );
    } catch (err) {
      setError("Failed to download PDF. Make sure the backend is running.");
    }
  };

  return (
    <div>
      <div className="ai-banner">
        Business Reports Center
      </div>

      <h2>Reports</h2>

      <p className="assistant-subtitle">
        Generate detailed business reports for
        management review and decision making.
      </p>

      <select
        value={type}
        onChange={(e) => setType(e.target.value)}
      >
        <option value="complaint">
          Complaint Report
        </option>

        <option value="revenue">
          Revenue Report
        </option>

        <option value="branch">
          Branch Report
        </option>

        <option value="customer_satisfaction">
          Customer Satisfaction Report
        </option>
      </select>

      <button
        onClick={handleGenerate}
        disabled={loading}
      >
        {loading
          ? "Generating..."
          : "Generate Report"}
      </button>

      <button
        onClick={handleDownloadPdf}
        disabled={loading}
      >
        Download PDF
      </button>

      {loading && (
        <div className="loading-container">
          <div className="spinner"></div>

          <p>
            Analyzing data and generating report...
          </p>
        </div>
      )}

      {error && (
        <div className="error-box">
          <p>{error}</p>
        </div>
      )}

      <div className="result-box">
        <h3>Custom Report</h3>

        <input
          type="text"
          value={customQuestion}
          onChange={(e) =>
            setCustomQuestion(e.target.value)
          }
          placeholder="Enter custom report request..."
        />

        <button
          onClick={handleCustomReport}
          disabled={
            loading ||
            !customQuestion.trim()
          }
        >
          {loading
            ? "Generating..."
            : "Generate Custom Report"}
        </button>
      </div>

      {report && (
        <div className="report-card">
          <h3 className="report-title">
            Generated Report
          </h3>

          <div className="report-output">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
            >
              {report}
            </ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
}