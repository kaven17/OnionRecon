import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard.jsx";
import NodeMap from "./pages/NodeMap.jsx";
import Timeline from "./pages/Timeline.jsx";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-sci-bg text-slate-100 scanlines">
        <div className="flex">
          {/* Left nav */}
          <nav className="w-20 h-screen flex flex-col items-center py-6 gap-6 bg-black border-r border-slate-800">
            <div className="w-10 h-10 rounded-xl glass flex items-center border-2 border-white justify-center neon-title text-sm">OR</div>
          </nav>

          {/* Main */}
          <main className="flex-1 p-5">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/map" element={<NodeMap />} />
              <Route path="/timeline" element={<Timeline />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;