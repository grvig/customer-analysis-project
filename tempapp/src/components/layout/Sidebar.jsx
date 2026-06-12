import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="sidebar">
      <div className="sidebar-brand">
        <h2>myTVS</h2>

        <p className="brand-subtitle">
          Customer Analytics Platform
        </p>
      </div>

      <nav>
        <NavLink to="/">Dashboard</NavLink>
        <NavLink to="/ai">AI Assistant</NavLink>
        <NavLink to="/reports">Reports</NavLink>
      </nav>
    </div>
  );
}