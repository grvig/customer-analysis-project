export default function Header() {
  const today = new Date().toLocaleDateString("en-IN", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <div className="header">
      <div>
        <h1>Customer Analytics Dashboard</h1>

        <p
          style={{
            color: "#777",
            marginTop: "8px",
            fontSize: "14px",
          }}
        >
          Business Intelligence & Service Insights
        </p>
      </div>

      <div
        style={{
          color: "#777",
          fontWeight: "600",
        }}
      >
        {today}
      </div>
    </div>
  );
}