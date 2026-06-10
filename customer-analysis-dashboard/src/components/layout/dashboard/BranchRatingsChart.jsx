import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import { branchRatings } from "../../../mock/dashboardData";

export default function BranchRatingsChart() {
  return (
    <div className="chart-card">
      <h3>Branch Ratings</h3>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={branchRatings}>
          <XAxis dataKey="branch" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="rating" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}