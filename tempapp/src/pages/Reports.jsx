import { useState } from "react";
import { generateReport } from "../services/reportService";

export default function Reports() {
  const [type, setType] = useState("complaint");
  const [report, setReport] = useState("");

  const handleGenerate = async () => {
    const data = await generateReport(type);
    setReport(data.report);
  };

  return (
    <div>
      <h2>Reports</h2>

      <select
        value={type}
        onChange={(e) => setType(e.target.value)}
      >
        <option value="complaint">Complaint Report</option>
        <option value="revenue">Revenue Report</option>
        <option value="branch">Branch Report</option>
        <option value="customer_satisfaction">
          Customer Satisfaction Report
        </option>
      </select>

      <button onClick={handleGenerate}>
        Generate Report
      </button>

      <button disabled>
        Download PDF
      </button>

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