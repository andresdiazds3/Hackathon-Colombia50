import { getDashboardData } from "../api/api";
import Charts from "../components/Charts";
import MapView from "../components/MapView";
import Chat from "../components/Chat";
import AIAnalysis from "../components/AIAnalysis";

export default function Dashboard() {
  const data = getDashboardData();

  return (
    <div className="content">
      <h1>Red WiFi Rural — Cali</h1>

      <Charts data={data.charts} />
      <MapView aps={data.aps} />

      <div className="grid">
        <Chat />
        <AIAnalysis />
      </div>
    </div>
  );
}