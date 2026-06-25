import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/layout/Layout";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/login";
import Dashboard from "./pages/Dashboard";
import AIAssistant from "./pages/AIAssistant";
import Reports from "./pages/Reports";
import CreateUser from "./pages/CreateUser";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/login"
          element={<Login />}
        />
        <Route
          path="/create-user"
          element={<CreateUser />}
        />

        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <Layout>
                <Routes>
                  <Route
                    path="/"
                    element={<Dashboard />}
                  />

                  <Route
                    path="/ai"
                    element={<AIAssistant />}
                  />

                  <Route
                    path="/reports"
                    element={<Reports />}
                  />
                </Routes>
              </Layout>
            </ProtectedRoute>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}