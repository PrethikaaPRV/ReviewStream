# ReviewStream

## Real-Time Review Analytics & Semantic Search Pipeline

ReviewStream is an end-to-end data engineering project that processes customer reviews in real time, stores structured review data, generates text embeddings, and provides semantic search and analytics through a web dashboard.

## Architecture

```text
Python Producer
      ↓
    Kafka
      ↓
PySpark Structured Streaming
      ↓
 PostgreSQL
      ↓
Sentence Transformers
      ↓
   pgvector
      ↓
   FastAPI
      ↓
Streamlit Dashboard
```

## Key Features

- Real-time customer review ingestion using Apache Kafka
- Stream processing using PySpark Structured Streaming
- Review categorization into Positive, Neutral, and Negative
- PostgreSQL storage for structured review data
- Text embeddings using Sentence Transformers
- Vector similarity search using PostgreSQL + pgvector
- Semantic search using natural-language queries
- REST API using FastAPI
- Interactive analytics dashboard using Streamlit
- Docker-based infrastructure

## Technology Stack

| Technology            | Purpose                         |
|-----------------------|---------------------------------|
| Python                | Application and data processing |
| Apache Kafka          | Real-time message streaming     |
| PySpark               | Stream processing               |
| PostgreSQL            | Relational data storage         |
| pgvector              | Vector similarity search        |
| Sentence Transformers | Text embeddings                 |
| FastAPI               | REST API                        |
| Streamlit             | Interactive dashboard           |
| Docker                | Containerization                |
| Git/GitHub            | Version control                 |

## Data Flow

### 1. Review Producer

Customer reviews are generated as JSON messages and published to the Kafka `reviews` topic.

Example:

```json
{
  "review_id": 1,
  "rating": 5,
  "review_text": "Amazing product! Really happy with the quality."
}
```

### 2. Kafka

Kafka acts as the event streaming layer between the producer and the processing pipeline.

### 3. PySpark Structured Streaming

PySpark consumes reviews from Kafka, parses the JSON data, and categorizes reviews based on their ratings.

- Rating 1–2 → Negative
- Rating 3 → Neutral
- Rating 4–5 → Positive

The processed reviews are written to PostgreSQL.

### 4. PostgreSQL

PostgreSQL stores the structured review information:

- Review ID
- Rating
- Review text
- Rating category
- Event time

### 5. Embeddings

Sentence Transformers converts each review into a numerical vector representation.

The project uses:

`all-MiniLM-L6-v2`

Each review is represented using a 384-dimensional embedding.

### 6. pgvector

The embeddings are stored inside PostgreSQL using the pgvector extension.

Semantic similarity is calculated using vector distance to retrieve reviews that are conceptually similar to a user's query.

### 7. FastAPI

FastAPI exposes the processed data through REST endpoints.

Available endpoints:

- `GET /`
- `GET /analytics`
- `GET /reviews`
- `POST /search`

### 8. Streamlit Dashboard

The Streamlit dashboard provides:

- Total review count
- Average rating
- Positive/neutral/negative review counts
- Sentiment distribution
- Recent reviews
- Semantic review search

## Semantic Search Example

A user can search:

`fast delivery`

Instead of searching for exact words, ReviewStream converts the query into an embedding and finds semantically similar reviews.

Example results include:

- Good product and quick delivery.
- Amazing quality and super fast delivery!
- Excellent quality and very fast delivery!

## Project Structure

```text
ReviewStream/
│
├── api/
│   └── main.py
│
├── consumer/
│   └── consumer.py
│
├── dashboard/
│   └── app.py
│
├── database/
│   ├── stream_to_postgres.py
│   ├── test_connection.py
│   └── test_spark_postgres.py
│
├── embeddings/
│   ├── generate_embeddings.py
│   └── semantic_search.py
│
├── producer/
│   ├── producer.py
│   └── send_one.py
│
├── spark/
│   ├── streaming_job.py
│   └── check_parquet.py
│
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/Pr3thikaa/ReviewStream.git
cd ReviewStream
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Docker services

```bash
docker compose up -d
```

### 4. Start FastAPI

```bash
python -m uvicorn api.main:app --port 8001
```

### 5. Start Streamlit

Open another terminal:

```bash
python -m streamlit run dashboard/app.py
```

The dashboard will be available at:

`http://localhost:8501`

## Future Improvements

- Deploy the pipeline to AWS
- Add automated tests
- Add API authentication
- Add advanced sentiment analysis
- Add real-time monitoring and alerts
- Add CI/CD using GitHub Actions
- Scale Kafka and Spark processing for larger datasets

## Author

**Prethikaa PRV**

Computer Science & Engineering