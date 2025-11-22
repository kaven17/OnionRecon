# OnionRecon

**OnionRecon** is a forensic and investigative tool for monitoring, mapping, and analyzing TOR network traffic. It combines automated TOR topology mapping, correlation analysis, a real-time visualization dashboard, and exportable forensic reports.

---

## Features

### 1. Automated TOR Topology Mapping
- Collects TOR relay nodes and builds a dynamic network map.
- Detects and correlates PCAP events with TOR relay nodes.
- Computes confidence scores for origin identification.

### 2. Visualization Dashboard
- Real-time dashboard showing:
  - Active nodes
  - PCAP events
  - Correlations
  - Average confidence metrics
- Tactical network map for visual inspection of traffic flows.
- Activity ticker logs all system events.

### 3. Forensic Report Generation
- Exportable PDF reports containing:
  - Traced node data
  - Event timestamps
  - Correlation confidence
- Historical record for auditing and investigative purposes.

### 4. PCAP Analysis
- Upload PCAP files directly.
- Correlates network traffic with TOR relay nodes.
- Highlights suspicious flows using IP heuristics and timing analysis.

---

## Screenshots

*(Add your screenshots here to demonstrate working prototype)*

1. Dashboard overview  
2. Tactical network map  
3. Exported PDF forensic report  

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/kaven17/OnionRecon.git
cd OnionRecon
