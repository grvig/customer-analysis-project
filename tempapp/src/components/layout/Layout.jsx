import Sidebar from "./sidebar";
import Header from "./header";

export default function Layout({ children }) {
  return (
    <div className="app-layout">
      <Sidebar />

      <div className="main-content">
        <Header />
        {children}
      </div>
    </div>
  );
}