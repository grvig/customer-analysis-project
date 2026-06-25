import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { register } from "../services/authService";

export default function CreateUser() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");

  const [password, setPassword] = useState("");

  const [confirmPassword, setConfirmPassword] =
    useState("");

  const [showPassword, setShowPassword] =
    useState(false);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [success, setSuccess] =
    useState("");

  const getStrength = () => {
    if (password.length < 6)
      return {
        text: "Weak",
        color: "#dc2626",
      };

    if (password.length < 10)
      return {
        text: "Medium",
        color: "#f59e0b",
      };

    return {
      text: "Strong",
      color: "#16a34a",
    };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    if (password !== confirmPassword) {
      setError(
        "Passwords do not match."
      );
      return;
    }

    try {
      setLoading(true);

      await register(
        username,
        password
      );

      setSuccess(
        "User created successfully! Redirecting to Login..."
      );

      setTimeout(() => {
        navigate("/login");
      }, 1800);

    } catch (err) {

      setError(
        err?.response?.data?.detail ||
          "Unable to create user."
      );

    } finally {

      setLoading(false);

    }
  };

  const strength = getStrength();

  return (
    <div className="login-page">
      <div className="login-card">

        <h1>myTVS</h1>

        <h2>Create New User</h2>

        <form onSubmit={handleSubmit}>

          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) =>
              setUsername(e.target.value)
            }
            required
          />

          <input
            type={
              showPassword
                ? "text"
                : "password"
            }
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            required
          />

          <input
            type={
              showPassword
                ? "text"
                : "password"
            }
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) =>
              setConfirmPassword(
                e.target.value
              )
            }
            required
          />

          <label
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              marginBottom: "18px",
              cursor: "pointer",
            }}
          >
            <input
              type="checkbox"
              checked={showPassword}
              onChange={() =>
                setShowPassword(
                  !showPassword
                )
              }
              style={{
                width: "18px",
              }}
            />

            Show Password
          </label>

          <p
            style={{
              color: strength.color,
              fontWeight: 600,
              marginBottom: "18px",
            }}
          >
            Password Strength:{" "}
            {strength.text}
          </p>

          {error && (
            <p className="login-error">
              {error}
            </p>
          )}

          {success && (
            <p className="login-success">
              {success}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
          >
            {loading
              ? "Creating..."
              : "Create User"}
          </button>

        </form>

        <div className="auth-link">

          <p>
            Already have an account?
          </p>

          <Link to="/login">
            Back to Login
          </Link>

        </div>

      </div>
    </div>
  );
}