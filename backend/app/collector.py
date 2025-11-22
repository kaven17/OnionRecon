import requests
from datetime import datetime
from .db import get_db_connection  # Use the shared connection

ONIONOO_URL = "https://onionoo.torproject.org/details?type=relay"

def fetch_tor_relays():
    try:
        response = requests.get(ONIONOO_URL, timeout=10)
        response.raise_for_status()
        return response.json().get("relays", [])
    except Exception as e:
        print("[Collector] Error:", e)
        return []

def save_relays_to_db():
    relays = fetch_tor_relays()
    if not relays:
        return False

    conn = get_db_connection()
    cur = conn.cursor()

    for r in relays:
        cur.execute("""
            INSERT OR REPLACE INTO tor_nodes
            (fingerprint, nickname, address, or_port, exit_policy, last_seen, type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            r.get("fingerprint"),
            r.get("nickname", "Unknown"),
            r.get("or_addresses", ["0.0.0.0"])[0],
            r.get("or_port", 0),
            str(r.get("exit_policy", "")),
            r.get("last_seen", ""),
            "exit" if r.get("exit_policy") else "relay"
        ))

    conn.commit()
    conn.close()
    print(f"[Collector] Saved {len(relays)} relays at {datetime.now()}")
    return True
