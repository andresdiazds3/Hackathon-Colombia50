import { useState } from "react";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const [screen, setScreen] = useState("dashboard");
  return (
    <>
      <Navbar setScreen={setScreen} />
      {screen === "dashboard" && <Dashboard />}
    </>
  );
}
