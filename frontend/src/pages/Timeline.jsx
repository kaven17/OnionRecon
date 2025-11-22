import React, { useEffect, useState } from "react";
import axios from "axios";

export default function Timeline() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    async function fetchTimeline() {
      try {
        // Replace `/timeline` with your actual backend endpoint
        const res = await axios.get("http://127.0.0.1:8000/correlate");
        const data = res.data.results || [];
        // map backend data into timeline entries
        const timelineEvents = data.map((item, index) => ({
          id: index,
          time: new Date().toLocaleTimeString(),
          title: item.nickname || "Unknown Node",
          subtitle: `Confidence: ${item.confidence.toFixed(2)}%`,
        }));
        setEvents(timelineEvents);
      } catch (err) {
        console.error("Failed to fetch timeline:", err);
        // fallback demo events
        setEvents([
          { id: 1, time: "12:03:01", title: "Exit Node observed", subtitle: "Packets: 234" },
          { id: 2, time: "12:02:10", title: "Guard candidate", subtitle: "Score: 0.72" },
          { id: 3, time: "12:01:00", title: "PCAP uploaded", subtitle: "Packets: 2412" },
        ]);
      }
    }

    fetchTimeline();
  }, []);

  return (
    <div className="glass p-6 rounded-xl">
      <div className="flex items-center justify-between">
        <h2 className="neon-title">Chrono-Flow Analyzer</h2>
        <div className="text-xs text-slate-400">Replay available</div>
      </div>

      <div className="mt-4 overflow-auto h-80 space-y-3">
        {events.map((ev) => (
          <div key={ev.id} className="glass p-3 rounded w-full border border-gray-700">
            <div className="text-xs text-slate-400">{ev.time}</div>
            <div className="neon-title">{ev.title}</div>
            <div className="text-sm mt-1 text-slate-300">{ev.subtitle}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
