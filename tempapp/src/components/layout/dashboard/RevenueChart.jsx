import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function RevenueChart({ data }) {
  return (
    <div className="chart-card">
      <h3>Revenue by Service Type</h3>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <XAxis dataKey="service" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="revenue" fill="#F36F21" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}