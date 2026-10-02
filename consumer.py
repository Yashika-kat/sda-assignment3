from kafka import KafkaConsumer
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv(".env", override=True)

# Connect to MongoDB Atlas
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["sda_assignment3"]

TOPICS = ["orders", "inventory", "payments", "deliveries"]

for topic in TOPICS:
    print(f"\n--- Consuming from {topic} ---")

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id=f"sda_assignment3_{topic}",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        consumer_timeout_ms=5000
    )

    collection = db[topic]

    count = 0

    for message in consumer:
        collection.insert_one(message.value)
        print(f"Saved to MongoDB: {message.value}")
        count += 1

        if count >= 20:
            break

    consumer.close()
    print(f"{count} messages saved to MongoDB collection: {topic}")

client.close()

print("\nAll Kafka messages saved to MongoDB successfully.")
