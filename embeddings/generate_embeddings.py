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

cursor.execute("""
    SELECT review_id, review_text
    FROM reviews
    WHERE embedding IS NULL
""")

reviews = cursor.fetchall()

print("Reviews waiting for embeddings:")

for review_id, review_text in reviews:
    embedding = model.encode(review_text)

    embedding_string = "[" + ",".join(map(str, embedding)) + "]"

    cursor.execute(
        """
        UPDATE reviews
        SET embedding = %s
        WHERE review_id = %s
        """,
        (embedding_string, review_id)
    )

    print(f"Embedded review {review_id}")

connection.commit()
print("All embeddings saved to PostgreSQL!")

cursor.close()
connection.close()