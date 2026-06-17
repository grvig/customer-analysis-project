import { useEffect, useState } from "react";

import SummaryCard from "../components/layout/dashboard/SummaryCard";
import ComplaintChart from "../components/layout/dashboard/ComplaintChart";
import RevenueChart from "../components/layout/dashboard/RevenueChart";
import BranchRatingsChart from "../components/layout/dashboard/BranchRatingsChart";

import { getDashboardData } from "../services/dashboardService";

export default function Dashboard() {

  const [dashboardData, setDashboardData] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {

    const fetchDashboard = async () => {

      try {

        const data =
          await getDashboardData();

        console.log(data);

        setDashboardData(data);

      } catch (error) {

        console.error(error);

      } finally {

        setLoading(false);

      }

    };

    fetchDashboard();

  }, []);

  if (loading) {

    return <h3>Loading dashboard...</h3>;

  }

  return (
    <>
      <div className="summary-grid">

        <SummaryCard
          title="Total Customers"
          value={dashboardData.summary.customers}
        />

        <SummaryCard
          title="Total Calls"
          value={dashboardData.summary.calls}
        />

        <SummaryCard
          title="Total Services"
          value={dashboardData.summary.services}
        />

        <SummaryCard
          title="Total Surveys"
          value={dashboardData.summary.surveys}
        />

      </div>

      <div className="charts-grid">

        <ComplaintChart
          data={dashboardData.complaints}
        />

        <RevenueChart
          data={dashboardData.revenue}
        />

        <BranchRatingsChart
          data={dashboardData.ratings}
        />

      </div>
    </>
  );

}