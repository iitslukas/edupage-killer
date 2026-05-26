import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import Header from "./Header";
import DemoBanner from "@/components/DemoBanner";

const DEMO_MODE = import.meta.env.VITE_DEMO_MODE === "true";

export default function AppLayout() {
  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {DEMO_MODE && <DemoBanner />}
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <div className="flex flex-col flex-1 overflow-hidden">
          <Header />
          <main className="flex-1 overflow-auto p-6">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}
