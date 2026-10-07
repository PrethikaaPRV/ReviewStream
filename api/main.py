from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import psycopg2


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="ReviewStream Semantic Search",
    version="1.0.0"
)


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------------
# PostgreSQL connection
# --------------------------------------------------

connection = psycopg2.connect(
    host="localhost",
    port=5433,
    database="reviewstream",
    user="reviewuser",
    password="reviewpass"
)

cursor = connection.cursor()


# --------------------------------------------------
# Request model for semantic search
# --------------------------------------------------

class SearchRequest(BaseModel):
    query: str


# --------------------------------------------------
# Home endpoint
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "ReviewStream API is running!"
    }


# --------------------------------------------------
# Semantic search endpoint
# --------------------------------------------------

@app.post("/search")
def semantic_search(request: SearchRequest):

    # Convert user's search text into an embedding
    query_embedding = model.encode(request.query)

    # Convert embedding into pgvector format
    query_vector = "[" + ",".join(map(str, query_embedding)) + "]"

    # Search PostgreSQL using cosine distance
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

    return {
        "query": request.query,
        "results": [
            {
                "review_id": review_id,
                "rating": rating,
                "review_text": review_text,
                "distance": round(float(distance), 4)
            }
            for review_id, rating, review_text, distance in results
        ]
    }


# --------------------------------------------------
# Review analytics endpoint
# --------------------------------------------------

@app.get("/analytics")
def analytics():

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_reviews,

            ROUND(
                AVG(rating),
                2
            ) AS average_rating,

            COUNT(*) FILTER (
                WHERE rating_category = 'Positive'
            ) AS positive_reviews,

            COUNT(*) FILTER (
                WHERE rating_category = 'Neutral'
            ) AS neutral_reviews,

            COUNT(*) FILTER (
                WHERE rating_category = 'Negative'
            ) AS negative_reviews

        FROM reviews
        """
    )

    result = cursor.fetchone()

    return {
        "total_reviews": result[0],
        "average_rating": float(result[1]),
        "positive_reviews": result[2],
        "neutral_reviews": result[3],
        "negative_reviews": result[4]
    }

# --------------------------------------------------
# Recent reviews endpoint
# --------------------------------------------------

@app.get("/reviews")
def recent_reviews():

    cursor.execute(
        """
        SELECT
            review_id,
            rating,
            review_text,
            rating_category
        FROM reviews
        ORDER BY review_id DESC
        LIMIT 10
        """
    )

    results = cursor.fetchall()

    return {
        "reviews": [
            {
                "review_id": review_id,
                "rating": rating,
                "review_text": review_text,
                "rating_category": rating_category
            }
            for review_id, rating, review_text, rating_category in results
        ]
    }