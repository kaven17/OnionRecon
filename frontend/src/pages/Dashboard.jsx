import React, { useState, useEffect } from "react";
import {
  collectNodes,
  uploadPCAP,
  runCorrelation,
  generateReport,
  fetchDashboardStats,
} from "../api";

export default function Dashboard() {
  const [status, setStatus] = useState("Idle");

  const [stats, setStats] = useState({
    active_nodes: 0,
    pcap_events: 0,
    correlations: 0,
    avg_confidence: 0,
  });

  const [activity, setActivity] = useState([
    "[System] Initialized dashboard…",
  ]);

  // --------------------------------------------------
  // LOAD BACKEND STATS ON PAGE LOAD
  // --------------------------------------------------
  useEffect(() => {
    loadStats();
  }, []);

  async function loadStats() {
    try {
      const res = await fetchDashboardStats();
      const data = res.data;

      const confidence =
        data.pcap_events === 0
          ? 0
          : Math.min(
              100,
              Math.round((data.correlations / data.pcap_events) * 100)
            );

      setStats({
        active_nodes: data.total_relays,
        pcap_events: data.pcap_events,
        correlations: data.correlations,
        avg_confidence: confidence,
      });

      addActivity("Dashboard stats synced.");
    } catch (err) {
      console.error(err);
      setStatus("Failed loading dashboard stats");
      addActivity("Failed to load stats.");
    }
  }

  // --------------------------------------------------
  // ACTIVITY LOGGER
  // --------------------------------------------------
  function addActivity(msg) {
    const ts = new Date().toLocaleTimeString();
    setActivity((prev) => [`[${ts}] ${msg}`, ...prev]);
  }

  // --------------------------------------------------
  // BUTTON HANDLERS
  // --------------------------------------------------

  async function handleCollect() {
    try {
      setStatus("Collecting TOR relays…");
      addActivity("Collecting TOR relays…");
      await collectNodes();
      await loadStats();
      setStatus("Relay list updated ✓");
      addActivity("Relay list updated.");
    } catch (e) {
      console.error(e);
      setStatus("Collect failed");
      addActivity("Node collection failed.");
    }
  }

  async function handleUpload(e) {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      setStatus("Uploading PCAP…");
      addActivity(`Uploading PCAP file: ${file.name}`);
      await uploadPCAP(file);
      await loadStats();
      setStatus("PCAP processed ✓");
      addActivity("PCAP processed.");
    } catch (e) {
      console.error(e);
      setStatus("Upload failed");
      addActivity("PCAP upload failed.");
    }
  }

  async function handleCorr() {
    try {
      setStatus("Running correlation…");
      addActivity("Running correlation engine…");
      await runCorrelation();
      await loadStats();
      setStatus("Correlation complete ✓");
      addActivity("Correlation completed.");
    } catch (e) {
      console.error(e);
      setStatus("Correlation failed");
      addActivity("Correlation failed.");
    }
  }

  async function downloadReport() {
    try {
      setStatus("Generating report…");
      addActivity("Generating forensic report…");
  
      // Fetch PDF from backend
      const response = await generateReport({
        responseType: "blob", // important for binary files
      });
  
      // Create a blob and temporary URL
      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);
  
      // Create a temporary link to download
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        `tor_correlation_report_${new Date().toISOString()}.pdf`
      );
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
  
      setStatus("Report downloaded ✓");
      addActivity("Report downloaded.");
  
    } catch (e) {
      console.error(e);
      setStatus("Report failed");
      addActivity("Report download failed.");
    }
  }
  

  // --------------------------------------------------
  // UI (FULL LAYOUT)
  // --------------------------------------------------
  return (
    <div className="grid grid-cols-12 gap-6">

      {/* TOP STAT CARDS */}
      <div className="col-span-8 grid grid-cols-4 gap-4">

        <div className="bg-[#1a1a1a] p-4 rounded-xl border border-gray-700">
          <div className="text-xs text-gray-400">ACTIVE NODES</div>
          <div className="text-2xl text-white font-semibold">
            {stats.active_nodes}
          </div>
        </div>

        <div className="bg-[#1a1a1a] p-4 rounded-xl border border-gray-700">
          <div className="text-xs text-gray-400">PCAP EVENTS</div>
          <div className="text-2xl text-white font-semibold">
            {stats.pcap_events}
          </div>
        </div>

        <div className="bg-[#1a1a1a] p-4 rounded-xl border border-gray-700">
          <div className="text-xs text-gray-400">CORRELATIONS</div>
          <div className="text-2xl text-white font-semibold">
            {stats.correlations}
          </div>
        </div>

        <div className="bg-[#1a1a1a] p-4 rounded-xl border border-gray-700">
          <div className="text-xs text-gray-400">AVG CONFIDENCE</div>
          <div className="text-2xl text-white font-semibold">
            {stats.avg_confidence}%
          </div>
        </div>
      </div>

      {/* TACTICAL MAP */}
      <div className="col-span-8">
        <div className="bg-[#1a1a1a] rounded-xl p-4 h-[520px] border border-gray-700">
          <div className="flex justify-between items-center">
            <h2 className="text-white font-semibold text-lg">
              Tactical Network Map
            </h2>

            <div className="flex gap-2">
              <button
                onClick={() => (window.location.href = "/map")}
                className="px-3 py-1 bg-[#2a2a2a] text-white rounded border border-gray-600"
              >
                Open Map
              </button>

              <button
                onClick={() => (window.location.href = "/timeline")}
                className="px-3 py-1 bg-[#2a2a2a] text-white rounded border border-gray-600"
              >
                Open Timeline
              </button>
            </div>
          </div>

          <div className="mt-4 h-[440px] bg-[#0f0f0f] rounded-md flex items-center justify-center text-gray-500 border border-gray-700">
            <div>
              <div className="text-3xl text-gray-300 font-semibold">
                Holographic Tactical Map
              </div>
              <div className="text-sm mt-2">
                Open full map for interactive view
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* RIGHT CONTROL PANEL */}
      <div className="col-span-4 space-y-4">

        {/* COMMAND PANEL */}
        <div className="bg-[#1a1a1a] p-4 rounded-xl border border-gray-700">
          <div className="text-xs text-gray-400">COMMAND PANEL</div>

          <div className="mt-2 flex flex-col gap-2">
            <button
              onClick={handleCollect}
              className="py-2 bg-[#2a2a2a] text-white rounded border border-gray-600"
            >
              Update Nodes
            </button>

            <label className="block">
              <input type="file" onChange={handleUpload} className="hidden" />
              <div className="py-2 text-center bg-[#2a2a2a] text-white rounded border border-gray-600 cursor-pointer">
                Upload PCAP
              </div>
            </label>

            <button
              onClick={handleCorr}
              className="py-2 bg-[#2a2a2a] text-white rounded border border-gray-600"
            >
              Run Correlation
            </button>

            <button
              onClick={downloadReport}
              className="py-2 bg-[#2a2a2a] text-white rounded border border-gray-600"
            >
              Download Report
            </button>
          </div>
        </div>

        {/* ACTIVITY TICKER */}
        <div className="bg-[#1a1a1a] p-4 rounded-xl border border-gray-700">
          <div className="text-xs text-gray-400">ACTIVITY TICKER</div>

          <div className="mt-2 h-40 overflow-auto text-sm text-gray-300 space-y-2">
            {activity.map((a, idx) => (
              <div key={idx}>{a}</div>
            ))}
          </div>
        </div>

        {/* STATUS PANEL */}
        <div className="bg-[#1a1a1a] p-4 rounded-xl border border-gray-700">
          <div className="text-xs text-gray-400">STATUS</div>
          <div className="mt-2 text-white font-semibold">{status}</div>
        </div>
      </div>
    </div>
  );
}
