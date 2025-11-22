import sqlite3
import threading
from datetime import datetime
import random

DB_PATH = "onionrecon.db"

# Thread-safe lock for concurrent FastAPI queries
_db_lock = threading.Lock()


def get_db_connection():
    """
    Returns a SQLite database connection.
    Ensures foreign keys are enabled and rows return dict-like objects.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    with _db_lock:
        conn = get_db_connection()
        cur = conn.cursor()

        # relays table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS relays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fingerprint TEXT,
            ip TEXT,
            or_port INTEGER,
            dir_port INTEGER
        )
        """)

        # tor_nodes table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tor_nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fingerprint TEXT,
            nickname TEXT,
            address TEXT,
            or_port INTEGER,
            exit_policy TEXT,
            last_seen TEXT,
            type TEXT
        )
        """)

        # pcap_logs table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pcap_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source_ip TEXT,
            dest_ip TEXT,
            protocol TEXT
        )
        """)

        # pcap_flows table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS pcap_flows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            avg_delta REAL,
            avg_size REAL,
            packet_count INTEGER
        )
        """)

        # correlations table
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
        conn.close()


def seed_dummy_data():
    """
    Populates the database with some initial dummy data
    to make the dashboard not empty on first load.
    """
    with _db_lock:
        conn = get_db_connection()
        cur = conn.cursor()

        # Add some TOR nodes if table is empty
        cur.execute("SELECT COUNT(*) as cnt FROM tor_nodes")
        if cur.fetchone()["cnt"] == 0:
            for i in range(10):
                cur.execute("""
                INSERT INTO tor_nodes (fingerprint, nickname, address, or_port, exit_policy, last_seen, type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    f"FP{i:04}",
                    f"Node{i}",
                    f"192.168.0.{i+1}",
                    9001 + i,
                    random.choice([0, 1]),
                    datetime.utcnow().isoformat(),
                    random.choice(["relay", "exit"])
                ))

        # Add some PCAP logs if table is empty
        cur.execute("SELECT COUNT(*) as cnt FROM pcap_logs")
        if cur.fetchone()["cnt"] == 0:
            protocols = ["TCP", "UDP", "ICMP"]
            for i in range(15):
                cur.execute("""
                INSERT INTO pcap_logs (timestamp, source_ip, dest_ip, protocol)
                VALUES (?, ?, ?, ?)
                """, (
                    datetime.utcnow().isoformat(),
                    f"10.0.0.{i+1}",
                    f"10.0.1.{i+1}",
                    random.choice(protocols)
                ))

        # Add some correlations if table is empty
        cur.execute("SELECT COUNT(*) as cnt FROM correlations")
        if cur.fetchone()["cnt"] == 0:
            for i in range(5):
                cur.execute("""
                INSERT INTO correlations (timestamp, event)
                VALUES (?, ?)
                """, (
                    datetime.utcnow().isoformat(),
                    f"Correlation Event {i+1}"
                ))

        conn.commit()
        conn.close()


# Legacy compatibility for older modules
def get_connection():
    return get_db_connection()


if __name__ == "__main__":
    # Initialize DB and optionally seed data when running directly
    init_db()
    seed_dummy_data()
    print("Database initialized and dummy data seeded!")
