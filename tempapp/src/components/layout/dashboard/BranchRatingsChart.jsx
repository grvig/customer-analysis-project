import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function BranchRatingsChart({ data }) {
  return (
    <div className="chart-card">
      <h3>Branch Ratings</h3>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis dataKey="branch" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="rating" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}