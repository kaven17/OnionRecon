# app/correlator.py

import sqlite3
from datetime import datetime

DB_PATH = "onionrecon.db"


def get_connection():
    """Create DB connection and ensure correlations table exists."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Ensure correlations table has the required columns
    cur.execute("""
        CREATE TABLE IF NOT EXISTS correlations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event TEXT,
            entry_ip TEXT,
            exit_ip TEXT,
            confidence INTEGER
        )
    """)
    conn.commit()
    return conn


def compute_confidence(time_gap, ip_match):
    """
    Compute correlation confidence score.
    - time_gap: difference between packet timestamp and current time
    - ip_match: boolean if source/dest IP resembles TOR relay IP ranges
    """
    # Time decay – fresher packets = higher confidence
    time_score = max(0, 100 - (time_gap * 5))
    # IP-based heuristic
    ip_score = 40 if ip_match else 10
    final_score = min(100, int((time_score * 0.6) + (ip_score * 0.4)))
    return final_score


def correlate():
    conn = get_connection()
    cur = conn.cursor()

    # Get latest PCAP event
    cur.execute("""
        SELECT id, timestamp, source_ip, dest_ip, protocol
        FROM pcap_logs ORDER BY id DESC LIMIT 1
    """)
    pcap = cur.fetchone()

    if not pcap:
        return []

    pcap_ts = datetime.fromisoformat(pcap["timestamp"])
    now = datetime.now()
    time_gap = abs((now - pcap_ts).total_seconds())

    # Fetch TOR relays
    cur.execute("SELECT id, fingerprint, ip, or_port, dir_port FROM relays")
    nodes = cur.fetchall()

    results = []

    for n in nodes:
        relay_ip = n["ip"]
        ip_match = (relay_ip == pcap["source_ip"] or relay_ip == pcap["dest_ip"])
        score = compute_confidence(time_gap, ip_match)

        if score >= 20:
            results.append({
                "relay_id": n["id"],
                "fingerprint": n["fingerprint"],
                "relay_ip": relay_ip,
                "confidence": score,
                "pcap_source": pcap["source_ip"],
                "pcap_dest": pcap["dest_ip"],
                "timestamp": pcap["timestamp"]
            })

            # Insert into correlations table with proper columns
            cur.execute("""
                INSERT INTO correlations (timestamp, event, entry_ip, exit_ip, confidence)
                VALUES (?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                f"Correlation: relay {relay_ip} scored {score}%",
                pcap["source_ip"],
                pcap["dest_ip"],
                score
            ))

    conn.commit()
    conn.close()

    # Sort results by confidence descending
    results = sorted(results, key=lambda x: x["confidence"], reverse=True)
    return results
