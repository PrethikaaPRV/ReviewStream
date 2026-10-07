import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="reviewstream",
    user="reviewuser",
    password="reviewpass"
)

print("Connected to PostgreSQL successfully!")

connection.close()