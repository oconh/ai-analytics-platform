from fastapi import FastAPI
import psycopg2

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="analytics",
        user="admin",
        password="admin",
        port=5432
    )

@app.get("/events/count")
def get_event_count():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM events;")
    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {"total_events": result}

@app.get("/analytics/top-products")
def top_products():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT product, COUNT(*) as count
        FROM events
        GROUP BY product
        ORDER BY count DESC;
    """)

    result = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {"product": row[0], "count": row[1]}
        for row in result
    ]

@app.get("/analytics/revenue")
def revenue():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT SUM(price)
        FROM events
        WHERE event_type = 'purchase';
    """)

    result = cur.fetchone()[0] or 0

    cur.close()
    conn.close()

    return {"total_revenue": result}

    