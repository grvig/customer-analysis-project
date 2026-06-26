import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { logout } from "../../services/authService";
import api from "../../services/api";

export default function Header() {
  const [darkMode, setDarkMode] = useState(false);
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user"));
  const [showMenu, setShowMenu] = useState(false);
  const [showChangePassword, setShowChangePassword] = useState(false);
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [pwError, setPwError] = useState("");
  const [pwSuccess, setPwSuccess] = useState("");
  const [pwLoading, setPwLoading] = useState(false);
  const menuRef = useRef(null);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const openChangePassword = () => {
    setShowMenu(false);
    setCurrentPassword("");
    setNewPassword("");
    setConfirmPassword("");
    setPwError("");
    setPwSuccess("");
    setShowChangePassword(true);
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setPwError("");
    setPwSuccess("");

    if (newPassword !== confirmPassword) {
      setPwError("New passwords do not match.");
      return;
    }

    if (newPassword.length < 6) {
      setPwError("New password must be at least 6 characters.");
      return;
    }

    try {
      setPwLoading(true);
      await api.post("/change-password", {
        current_password: currentPassword,
        new_password: newPassword,
      });
      setPwSuccess("Password changed successfully.");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err) {
      setPwError(err?.response?.data?.detail || "Failed to change password.");
    } finally {
      setPwLoading(false);
    }
  };

  useEffect(() => {
    const savedMode = localStorage.getItem("theme") === "dark";
    setDarkMode(savedMode);
    if (savedMode) document.body.classList.add("dark-mode");
  }, []);

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setShowMenu(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const toggleTheme = () => {
    const newMode = !darkMode;
    setDarkMode(newMode);
    if (newMode) {
      document.body.classList.add("dark-mode");
      localStorage.setItem("theme", "dark");
    } else {
      document.body.classList.remove("dark-mode");
      localStorage.setItem("theme", "light");
    }
  };

  return (
    <>
      <div className="header">
        <div>
          <h1 className="header-title">Customer Analysis Dashboard</h1>
          <p className="header-subtitle">Customer Analytics & Business Insights</p>
        </div>

        <div className="header-actions">
          <button className="theme-toggle" onClick={toggleTheme} title={darkMode ? "Switch to light mode" : "Switch to dark mode"}>
            {darkMode ? (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="5"/>
                <line x1="12" y1="1" x2="12" y2="3"/>
                <line x1="12" y1="21" x2="12" y2="23"/>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                <line x1="1" y1="12" x2="3" y2="12"/>
                <line x1="21" y1="12" x2="23" y2="12"/>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
              </svg>
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
              </svg>
            )}
          </button>

          <div className="user-menu" ref={menuRef}>
            <button className="user-button" onClick={() => setShowMenu(!showMenu)}>
              {user?.username} ▼
            </button>

            {showMenu && (
              <div className="dropdown-menu">
                <button className="dropdown-item" onClick={openChangePassword}>
                  Change Password
                </button>
                <button className="logout-dropdown-btn" onClick={handleLogout}>
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {showChangePassword && (
        <div className="modal-overlay" onClick={() => setShowChangePassword(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <h2>Change Password</h2>

            <form onSubmit={handleChangePassword}>
              <input
                type="password"
                placeholder="Current password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="New password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="Confirm new password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />

              {pwError && <p className="login-error">{pwError}</p>}
              {pwSuccess && <p className="login-success">{pwSuccess}</p>}

              <div className="modal-actions">
                <button type="submit" disabled={pwLoading}>
                  {pwLoading ? "Saving..." : "Change Password"}
                </button>
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => setShowChangePassword(false)}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
