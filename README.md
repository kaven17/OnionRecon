# OnionRecon

**OnionRecon** is a forensic tool for monitoring, mapping, and analyzing TOR network traffic. It combines automated TOR topology mapping, correlation analysis, a real-time visualization dashboard, and exportable forensic reports.

---

## Features

* **Automated TOR Topology Mapping**

  * Collects TOR relay nodes and builds a dynamic network map.
  * Detects and correlates PCAP events with TOR relay nodes.
  * Computes confidence scores for origin identification.

* **Visualization Dashboard**

  * Real-time dashboard showing:

    * Active nodes
    * PCAP events
    * Correlations
    * Average confidence metrics
  * Tactical network map for visual inspection of traffic flows.
  * Activity ticker logs all system events.

* **Forensic Report Generation**

  * Exportable PDF reports containing:

    * Traced node data
    * Event timestamps
    * Correlation confidence
  * Historical record for auditing and investigative purposes.

* **PCAP Analysis**

  * Upload PCAP files directly.
  * Correlates network traffic with TOR relay nodes.
  * Highlights suspicious flows using IP heuristics and timing analysis.

---

## Demo / Screenshots

*(Add your screenshots here)*

1. Dashboard overview
2. Tactical network map
3. Exported PDF forensic report

---

## Full Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/kaven17/OnionRecon.git
cd OnionRecon
```

### 2. Set up Python virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the backend server

```bash
uvicorn app.main:app --reload
```

The backend will be running at `http://127.0.0.1:8000`.

### 5. Start the frontend (React/Vite)

```bash
cd frontend
npm install
npm run dev
```

The frontend dashboard will open at `http://localhost:5173`.

---

## Usage Instructions

1. **Update Nodes** – Fetch the latest TOR relay list.
2. **Upload PCAP** – Select a `.pcap` file for analysis.
3. **Run Correlation** – Correlate PCAP events with TOR nodes and compute confidence.
4. **Download Report** – Generate a PDF forensic report of all correlations.

> Tip: Upload a sample PCAP file and run correlation to see the dashboard metrics update and download a working report.

---

## Technology Stack

* **Backend:** FastAPI, Python, SQLite, ReportLab
* **Frontend:** React, Tailwind CSS, Axios
* **Network Analysis:** PCAP parsing and TOR relay correlation
* **Visualization:** Dynamic dashboard with tactical network map

---

## License

MIT License © 2025 [KAVEN](https://github.com/kaven17)

---

## Acknowledgements

* TOR Project for relay data and network information.
* ReportLab for PDF generation.
* FastAPI and React communities for tooling support.

---

## Notes

* Ensure CORS is enabled if accessing the backend from a different origin.
* For testing, sample PCAP files can be uploaded to demonstrate correlation and report generation.
