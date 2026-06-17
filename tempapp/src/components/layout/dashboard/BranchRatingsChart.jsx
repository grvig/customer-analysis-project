import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function BranchRatingsChart({ data }) {
  const minRating = Math.floor(
    Math.min(...data.map(item => item.rating))
  );

  const maxRating = Math.ceil(
    Math.max(...data.map(item => item.rating))
  );

  return (
    <div className="chart-card">
      <h3>Branch Ratings</h3>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis dataKey="branch" />
          <YAxis
            domain={[minRating, maxRating]}
          />
          <Tooltip />
          <Line type="monotone" dataKey="rating" strokeWidth={3} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}