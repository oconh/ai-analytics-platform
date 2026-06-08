import random
import time
import json
import uuid
from datetime import datetime

from config import PRODUCTS, EVENT_TYPES


def generate_event():
    event = {
        "event_id": str(uuid.uuid4()),
        "user_id": random.randint(1, 1000),
        "product": random.choice(PRODUCTS),
        "event_type": random.choice(EVENT_TYPES),
        "price": round(random.uniform(10, 2000), 2),
        "timestamp": datetime.utcnow().isoformat()
    }
    return event


def run_stream(delay=0.5):
    print("Starting event stream...\n")

    while True:
        event = generate_event()
        print(json.dumps(event))
        time.sleep(delay)


if __name__ == "__main__":
    run_stream()