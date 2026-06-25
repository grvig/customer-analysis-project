import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { logout } from "../../services/authService";

export default function Header() {
  const [darkMode, setDarkMode] = useState(false);

  const navigate = useNavigate();

  const user = JSON.parse(localStorage.getItem("user"));

  const [showMenu, setShowMenu] = useState(false);

  const menuRef = useRef(null);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  useEffect(() => {
    const savedMode =
      localStorage.getItem("theme") === "dark";

    setDarkMode(savedMode);

    if (savedMode) {
      document.body.classList.add("dark-mode");
    }
  }, []);

  useEffect(() => {
    function handleClickOutside(event) {
      if (
        menuRef.current &&
        !menuRef.current.contains(event.target)
      ) {
        setShowMenu(false);
      }
    }

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    return () =>
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );
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
    <div className="header">
      <div>
        <h1 className="header-title">
          Customer Analysis Dashboard
        </h1>

        <p className="header-subtitle">
          Customer Analytics & Business Insights
        </p>
      </div>

      <div className="header-actions">
        <button
          className="theme-toggle"
          onClick={toggleTheme}
        >
          {darkMode ? "☀️" : "🌙"}
        </button>

        <div
          className="user-menu"
          ref={menuRef}
        >
          <button
            className="user-button"
            onClick={() =>
              setShowMenu(!showMenu)
            }
          >
            {user?.username} ▼
          </button>

          {showMenu && (
            <div className="dropdown-menu">
              <button
                className="logout-dropdown-btn"
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}