import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="analytics",
    user="admin",
    password="admin",
    port=5432
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    user_id INT,
    product TEXT,
    event_type TEXT,
    price FLOAT,
    timestamp TIMESTAMP
);
""")

conn.commit()
cur.close()
conn.close()