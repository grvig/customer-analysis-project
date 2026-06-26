import { useEffect, useState } from "react";

import SummaryCard from "../components/layout/dashboard/SummaryCard";
import ComplaintChart from "../components/layout/dashboard/ComplaintChart";
import RevenueChart from "../components/layout/dashboard/RevenueChart";
import BranchRatingsChart from "../components/layout/dashboard/BranchRatingsChart";

import { getDashboardData } from "../services/dashboardService";

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("complaints");

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const data = await getDashboardData();

        if (data) {
          setDashboardData(data);
        }
      } catch (error) {
        setDashboardData(null);
        setError("Failed to load dashboard. Make sure the backend is running.");
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

  if (error || !dashboardData || !dashboardData.summary) {
    return (
      <div style={{ padding: "30px" }}>
        <div className="error-box">
          <p>{error || "Failed to load dashboard data."}</p>
        </div>
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