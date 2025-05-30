import os
import redis
import json
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

r = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    #ssl=True,  # Uncomment if your Redis requires SSL
    decode_responses=True
)

def save_to_memory(key, data):
    r.set(key, json.dumps(data))

def read_from_memory(key):
    value = r.get(key)
    return json.loads(value) if value else None

def export_all_logs(filename="output_logs.json"):
    keys = r.keys()
    all_logs = {}
    for key in keys:
        all_logs[key] = read_from_memory(key)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_logs, f, indent=2, ensure_ascii=False)
    print(f"Logs saved to {filename}")
    return filename  # So UI can show download link
