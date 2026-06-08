import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="analytics",
    user="admin",
    password="admin",
    port=5432
)

cur = conn.cursor()

def total_events():
    cur.execute("SELECT COUNT(*) FROM events;")
    return cur.fetchone()

def events_by_product():
    cur.execute("""
        SELECT product, COUNT(*) 
        FROM events
        GROUP BY product
        ORDER BY COUNT(*) DESC;
    """)
    return cur.fetchall()

def revenue_by_product():
    cur.execute("""
        SELECT product, SUM(price) 
        FROM events
        WHERE event_type = 'purchase'
        GROUP BY product
        ORDER BY SUM(price) DESC;
    """)
    return cur.fetchall()

def event_distribution():
    cur.execute("""
        SELECT event_type, COUNT(*)
        FROM events
        GROUP BY event_type;
    """)
    return cur.fetchall()

if __name__ == "__main__":
    print("Total events:", total_events())
    print("Events by product:", events_by_product())
    print("Revenue by product:", revenue_by_product())
    print("Event distribution:", event_distribution())