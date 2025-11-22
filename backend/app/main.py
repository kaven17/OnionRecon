# app/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

from app.collector import save_relays_to_db
from app.pcap_ingest import ingest_pcap
from app.correlator import correlate
from app.report import generate_report
from app.db import init_db, get_db_connection
from fastapi.responses import StreamingResponse

# =========================================================
#   FASTAPI INSTANCE
# =========================================================
app = FastAPI(
    title="TOR – Unveil: Peel The Onion | Backend API",
    description="Analytical system for tracing TOR-based traffic using node correlation and PCAP analysis.",
    version="1.0"
)

# =========================================================
#   CORS (Frontend ↔ Backend Communication)
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Update to your production domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

origins = [
    "http://localhost:5173",
    # you can also add other allowed origins if needed
]


# =========================================================
#   DATABASE INITIALIZATION
# =========================================================
init_db()


@app.get("/")
def home():
    return {
        "msg": "OnionRecon API Running",
        "service": "TOR – Unveil: Peel The Onion",
        "status": "OK",
        "endpoints": ["/collect", "/stats", "/upload_pcap", "/correlate", "/report", "/graph"]
    }


# =========================================================
#   1. TOR NODE COLLECTION
# =========================================================
@app.get("/collect")
def collect():
    """
    Fetch latest TOR relay nodes from the network and store in DB.
    """
    ok = save_relays_to_db()
    return {
        "status": ok,
        "message": "Relay list updated successfully"
    }


# =========================================================
#   2. DASHBOARD STATISTICS (USED FOR CARDS + CHARTS)
# =========================================================
@app.get("/stats")
def stats():
    """
    Returns dashboard metrics:
    - Total TOR nodes
    - Total PCAP log entries
    - Total correlation events
    """
    db = get_db_connection()
    cur = db.cursor()

    data = {
        "total_relays": cur.execute("SELECT COUNT(*) FROM tor_nodes").fetchone()[0],
        "pcap_events": cur.execute("SELECT COUNT(*) FROM pcap_logs").fetchone()[0],
        "correlations": cur.execute("SELECT COUNT(*) FROM correlations").fetchone()[0],
    }

    db.close()
    return data


# =========================================================
#   3. PCAP UPLOAD & PROCESSING
# =========================================================
@app.post("/upload_pcap")
async def upload_pcap(file: UploadFile = File(...)):
    """
    Upload PCAP → Extract packets → Push metadata to DB.
    """
    path = f"uploaded_{datetime.utcnow().timestamp()}.pcap"

    with open(path, "wb") as f:
        f.write(await file.read())

    ok = ingest_pcap(path)

    return {
        "status": ok,
        "message": "PCAP processed successfully",
        "file": file.filename
    }


# =========================================================
#   4. CORRELATION ENGINE
# =========================================================
@app.get("/correlate")
def correlation():
    """
    Run TOR correlation algorithm between:
    - Entry nodes
    - Exit nodes
    - PCAP flows

    Returns probable origin fingerprints + confidence scores.
    """
    results = correlate()
    return {
        "status": True,
        "count": len(results),
        "results": results
    }


# =========================================================
#   5. REPORT GENERATION
# =========================================================
@app.get("/report")
def report():
    pdf_buffer = generate_report()
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=tor_correlation_report.pdf"}
    )
# =========================================================
#   6. NETWORK GRAPH DATA
# =========================================================
@app.get("/graph")
def graph():
    """
    Return node/link data for 3D network visualization.
    """
    db = get_db_connection()
    cur = db.cursor()

    # Use tor_nodes table for graph visualization
    rows = cur.execute("SELECT id, nickname, address, or_port, type FROM tor_nodes LIMIT 200").fetchall()
    nodes = []
    links = []

    for r in rows:
        nodes.append({
            "id": r["id"],
            "label": r["nickname"],
            "group": 0 if r["type"] == "relay" else 1
        })

    # generate random links between nodes for visualization
    for i in range(len(nodes) - 1):
        if random.random() > 0.7:
            links.append({
                "source": nodes[i]["id"],
                "target": nodes[(i + 1) % len(nodes)]["id"]
            })

    db.close()
    return {"nodes": nodes, "links": links}
