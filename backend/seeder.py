import sqlite3

DB_PATH = "onionrecon.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tor_nodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fingerprint TEXT,
    nickname TEXT,
    address TEXT,
    or_port INTEGER,
    exit_policy BOOLEAN,
    last_seen TEXT,
    type TEXT
)
""")

conn.commit()
conn.close()
print("tor_nodes table created or already exists.")
