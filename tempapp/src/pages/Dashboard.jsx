import { useEffect, useState } from "react";

import SummaryCard from "../components/layout/dashboard/SummaryCard";
import ComplaintChart from "../components/layout/dashboard/ComplaintChart";
import RevenueChart from "../components/layout/dashboard/RevenueChart";
import BranchRatingsChart from "../components/layout/dashboard/BranchRatingsChart";

import { getDashboardData } from "../services/dashboardService";

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("complaints");

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const data = await getDashboardData();

        console.log("Dashboard Data:", data);

        if (data) {
          setDashboardData(data);
        }
      } catch (error) {
        console.error("Dashboard Error:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (!dashboardData || !dashboardData.summary) {
    return (
      <div style={{ padding: "30px" }}>
        <h2>Failed to load dashboard data.</h2>
        <p>
          Check whether the backend is running and
          returning dashboard data.
        </p>
      </div>
    );
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

      <div className="dashboard-tabs">
        <button
          className={
            activeTab === "complaints"
              ? "active-tab"
              : ""
          }
          onClick={() => setActiveTab("complaints")}
        >
          Complaints
        </button>

        <button
          className={
            activeTab === "revenue"
              ? "active-tab"
              : ""
          }
          onClick={() => setActiveTab("revenue")}
        >
          Revenue
        </button>

        <button
          className={
            activeTab === "ratings"
              ? "active-tab"
              : ""
          }
          onClick={() => setActiveTab("ratings")}
        >
          Ratings
        </button>
      </div>

      <div className="charts-grid">
        {activeTab === "complaints" && (
          <ComplaintChart
            data={dashboardData.complaints}
          />
        )}

        {activeTab === "revenue" && (
          <RevenueChart
            data={dashboardData.revenue}
          />
        )}

        {activeTab === "ratings" && (
          <BranchRatingsChart
            data={dashboardData.ratings}
          />
        )}
      </div>
    </>
  );
}