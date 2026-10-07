from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("TestSparkPostgres")
    .getOrCreate()
)

data = [
    (100, 5, "Spark connected to PostgreSQL!", "Positive")
]

columns = [
    "review_id",
    "rating",
    "review_text",
    "rating_category"
]

df = spark.createDataFrame(data, columns)

df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://reviewstream-postgres:5432/reviewstream") \
    .option("dbtable", "reviews") \
    .option("user", "reviewuser") \
    .option("password", "reviewpass") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()

print("Spark successfully wrote to PostgreSQL!")

spark.stop()