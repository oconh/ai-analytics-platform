import random
import time
import uuid
from datetime import datetime

from services.generator.config import EVENT_TYPES, PRODUCTS
from services.generator.db import get_conn, init_db


def generate_event():
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": random.randint(1, 1000),
        "product": random.choice(PRODUCTS),
        "event_type": random.choice(EVENT_TYPES),
        "price": round(random.uniform(10, 2000), 2),
        "timestamp": datetime.utcnow(),
    }


def insert_event(event):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO events (
                    event_id, user_id, product,
                    event_type, price, timestamp
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                event["event_id"],
                event["user_id"],
                event["product"],
                event["event_type"],
                event["price"],
                event["timestamp"],
            ))
            conn.commit()


def run():
    init_db()
    print("Streaming events to PostgreSQL...")

    while True:
        event = generate_event()
        insert_event(event)
        print("Inserted:", event["event_id"])
        time.sleep(0.5)


if __name__ == "__main__":
    run()
