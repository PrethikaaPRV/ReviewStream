from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "reviews",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

print("Waiting for reviews...")

for message in consumer:
    print(message.value)