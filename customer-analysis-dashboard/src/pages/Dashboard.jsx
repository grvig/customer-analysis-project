import SummaryCard from "../components/layout/dashboard/SummaryCard";
import ComplaintChart from "../components/layout/dashboard/ComplaintChart";
import RevenueChart from "../components/layout/dashboard/RevenueChart";
import BranchRatingsChart from "../components/layout/dashboard/BranchRatingsChart";

import { summaryData } from "../mock/dashboardData";

export default function Dashboard() {
  return (
    <>
      <div className="summary-grid">
        <SummaryCard title="Total Customers" value={summaryData.customers} />
        <SummaryCard title="Total Calls" value={summaryData.calls} />
        <SummaryCard title="Total Services" value={summaryData.services} />
        <SummaryCard title="Total Surveys" value={summaryData.surveys} />
      </div>

      <div className="charts-grid">
        <ComplaintChart />
        <RevenueChart />
        <BranchRatingsChart />
      </div>
    </>
  );
}