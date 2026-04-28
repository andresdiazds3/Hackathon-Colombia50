export default function Navbar({ setScreen }) {
  return (
    <div className="topbar">
      <div className="logo">COL50·NOC</div>
      <div className="nav">
        <button onClick={() => setScreen("dashboard")}>Dashboard</button>
      </div>
    </div>
  );
}