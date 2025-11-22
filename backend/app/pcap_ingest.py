import dpkt
from datetime import datetime
from .db import get_db_connection  # shared DB

def ingest_pcap(file_path):
    timestamps = []
    packet_sizes = []

    try:
        with open(file_path, "rb") as f:
            pcap = dpkt.pcap.Reader(f)
            for ts, buf in pcap:
                timestamps.append(ts)
                packet_sizes.append(len(buf))
    except Exception as e:
        print("[PCAP] Error:", e)
        return False

    if len(timestamps) < 2:
        return False

    deltas = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
    avg_delta = sum(deltas) / len(deltas)
    avg_size = sum(packet_sizes) / len(packet_sizes)

    conn = get_db_connection()
    cur = conn.cursor()

    # ensure table exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pcap_flows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            avg_delta REAL,
            avg_size REAL,
            packet_count INTEGER
        )
    """)

    cur.execute("""
        INSERT INTO pcap_flows (timestamp, avg_delta, avg_size, packet_count)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        avg_delta,
        avg_size,
        len(packet_sizes)
    ))

    conn.commit()
    conn.close()
    print("[PCAP] Saved flow metadata")
    return True
