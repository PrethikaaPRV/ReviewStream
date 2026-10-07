from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

reviews = [
    {
        "review_id": 1,
        "rating": 5,
        "review_text": "Amazing product! Really happy with the quality."
    },
    {
        "review_id": 2,
        "rating": 2,
        "review_text": "The product is okay, but delivery was very late."
    },
    {
        "review_id": 3,
        "rating": 4,
        "review_text": "Good quality and fast delivery."
    },
    {
        "review_id": 4,
        "rating": 1,
        "review_text": "Very disappointed. The product arrived damaged."
    },
    {
        "review_id": 5,
        "rating": 5,
        "review_text": "Excellent experience. I would buy this again."
    }
]

for review in reviews:
    producer.send("reviews", value=review)
    producer.flush()

    print(f"Sent review {review['review_id']}")
    time.sleep(2)

producer.close()