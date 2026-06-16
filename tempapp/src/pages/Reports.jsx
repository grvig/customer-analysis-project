import { useState } from "react";
import {
  generateReport,
  generateCustomReport,
  downloadPdfReport,
} from "../services/reportService";

export default function Reports() {
  const [type, setType] = useState("complaint");
  const [report, setReport] = useState("");
  const [customQuestion, setCustomQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    try {
      setLoading(true);

      const data = await generateReport(type);

      setReport(data.report);
    } catch (error) {
      console.error(error);

      setReport(
        "Failed to generate report. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleCustomReport = async () => {
    try {
      setLoading(true);

      const data = await generateCustomReport(customQuestion);
      setReport(data.report);
    } catch (error) {
      console.error(error);
      setReport("Failed to generate custom report. Please try again.");
    } finally {
      setLoading(false);
    }
  };
  const handleDownloadPdf = async () => {
    try {
      const data = await downloadPdfReport(type);

      window.open(
        `http://localhost:8000${data.download_url}`,
        "_blank"
      );
    } catch (error) {
      console.error(error);
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

      <div className="result-box">
        <h3>Custom Report</h3>

        <input
          type="text"
          value={customQuestion}
          onChange={(e) => setCustomQuestion(e.target.value)}
          placeholder="Enter custom report request..."
        />

        <button
          onClick={handleCustomReport}
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate Custom Report"}
        </button>
      </div>

      <textarea
        value={report}
        readOnly
        rows={20}
        style={{
          width: "100%",
          marginTop: "20px",
        }}
      />
    </div>
  );
}