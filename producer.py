from kafka import KafkaProducer
import csv
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

files = {
    "orders": "sample_data/orders.csv",
    "inventory": "sample_data/inventory.csv",
    "payments": "sample_data/payments.csv",
    "deliveries": "sample_data/deliveries.csv"
}

for topic, filepath in files.items():
    with open(filepath, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            producer.send(topic, row)

producer.flush()
producer.close()

print("All CSV data sent to Kafka successfully.")
