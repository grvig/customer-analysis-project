import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import { complaintData } from "../../../mock/dashboardData";

export default function ComplaintChart() {
  return (
    <div className="chart-card">
      <h3>Complaint Categories</h3>

      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={complaintData}
            dataKey="value"
            outerRadius={100}
            label
          >
            {complaintData.map((entry, index) => (
              <Cell key={index} />
            ))}
          </Pie>

          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}