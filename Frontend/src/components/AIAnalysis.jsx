import { useEffect, useState } from "react";
import { analyzeNetwork } from "../api/ai";
import { getDashboardData } from "../api/api";

export default function AIAnalysis() {
  const [text, setText] = useState("Analizando...");

  useEffect(() => {
    (async () => {
      const data = getDashboardData();
      const res = await analyzeNetwork(data);
      setText(res);
    })();
  }, []);

  return (
    <div className="panel">
      <div className="panel-header">Análisis IA</div>
      <div className="panel-body">{text}</div>
    </div>
  );
}