from sentence_transformers import SentenceTransformer
import psycopg2

model = SentenceTransformer("all-MiniLM-L6-v2")

connection = psycopg2.connect(
    host="localhost",
    port=5433,
    database="reviewstream",
    user="reviewuser",
    password="reviewpass"
)

cursor = connection.cursor()

print("Connected to PostgreSQL + pgvector!")

search_text = "fast delivery"

query_embedding = model.encode(search_text)

print("Search:", search_text)
print("Query dimensions:", len(query_embedding))
query_vector = "[" + ",".join(map(str, query_embedding)) + "]"

cursor.execute(
    """
    SELECT
        review_id,
        rating,
        review_text,
        embedding <=> %s::vector AS distance
    FROM reviews
    ORDER BY embedding <=> %s::vector
    LIMIT 3
    """,
    (query_vector, query_vector)
)

results = cursor.fetchall()

print("\nTop 3 semantic matches:")

for review_id, rating, review_text, distance in results:
    print(f"\nReview ID: {review_id}")
    print(f"Rating: {rating}")
    print(f"Review: {review_text}")
    print(f"Distance: {distance:.4f}")

cursor.close()
connection.close()
