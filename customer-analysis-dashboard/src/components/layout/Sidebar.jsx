import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="sidebar">
      <h2>Customer Analytics</h2>

      <nav>
        <NavLink to="/">Dashboard</NavLink>
        <NavLink to="/ai">AI Assistant</NavLink>
        <NavLink to="/reports">Reports</NavLink>
      </nav>
    </div>
  );
}