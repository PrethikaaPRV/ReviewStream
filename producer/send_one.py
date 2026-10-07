from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

review = {
    "review_id": 108,
    "rating": 5,
    "review_text": "Excellent quality and very fast delivery!"
}

producer.send("reviews", value=review)
producer.flush()

print("Sent review 108 successfully!")

producer.close()