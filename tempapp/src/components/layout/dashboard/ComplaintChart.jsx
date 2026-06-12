import { useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Sector,
} from "recharts";

import { complaintData } from "../../../mock/dashboardData";

const COLORS = [
  "#0056A6",
  "#F58220",
  "#0D6EFD",
  "#FF9F43",
];

const renderActiveShape = (props) => {
  const {
    cx,
    cy,
    innerRadius,
    outerRadius,
    startAngle,
    endAngle,
    fill,
  } = props;

  return (
    <g>
      <Sector
        cx={cx}
        cy={cy}
        innerRadius={innerRadius}
        outerRadius={outerRadius + 10}
        startAngle={startAngle}
        endAngle={endAngle}
        fill={fill}
        stroke="#F58220"
        strokeWidth={4}
      />
    </g>
  );
};

export default function ComplaintChart() {
  const [activeIndex, setActiveIndex] = useState(null);

  const handleClick = (_, index) => {
    setActiveIndex(index);
  };

  return (
    <div className="chart-card">
      <h3>Complaint Categories</h3>

      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={complaintData}
            dataKey="value"
            outerRadius={100}
            activeIndex={activeIndex}
            activeShape={renderActiveShape}
            onClick={handleClick}
            label
          >
            {complaintData.map((entry, index) => (
              <Cell
                key={index}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>

          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}