from services.api.db import get_conn


def total_events():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM events;")
            return cur.fetchone()[0]


def events_by_product():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT product, COUNT(*)
                FROM events
                GROUP BY product
                ORDER BY COUNT(*) DESC;
            """)
            return [
                {"product": row[0], "count": row[1]}
                for row in cur.fetchall()
            ]


def revenue_by_product():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT product, SUM(price)
                FROM events
                WHERE event_type = 'purchase'
                GROUP BY product
                ORDER BY SUM(price) DESC;
            """)
            return [
                {"product": row[0], "revenue": float(row[1] or 0)}
                for row in cur.fetchall()
            ]


def event_distribution():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT event_type, COUNT(*)
                FROM events
                GROUP BY event_type;
            """)
            return [
                {"event_type": row[0], "count": row[1]}
                for row in cur.fetchall()
            ]


if __name__ == "__main__":
    print("Total events:", total_events())
    print("Events by product:", events_by_product())
    print("Revenue by product:", revenue_by_product())
    print("Event distribution:", event_distribution())
