from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, when
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = (
    SparkSession.builder
    .appName("ReviewStreamPostgres")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

reviews = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:29092")
    .option("subscribe", "reviews")
    .option("startingOffsets", "latest")
    .load()
)

review_schema = StructType([
    StructField("review_id", IntegerType(), True),
    StructField("rating", IntegerType(), True),
    StructField("review_text", StringType(), True)
])

json_reviews = reviews.select(
    from_json(
        col("value").cast("string"),
        review_schema
    ).alias("review"),
    col("timestamp").alias("event_time")
)

parsed_reviews = json_reviews.select(
    col("review.review_id").alias("review_id"),
    col("review.rating").alias("rating"),
    col("review.review_text").alias("review_text"),
    col("event_time")
)

categorized_reviews = parsed_reviews.withColumn(
    "rating_category",
    when(col("rating") <= 2, "Negative")
    .when(col("rating") == 3, "Neutral")
    .otherwise("Positive")
)

postgres_url = "jdbc:postgresql://reviewstream-postgres:5432/reviewstream"

postgres_properties = {
    "user": "reviewuser",
    "password": "reviewpass",
    "driver": "org.postgresql.Driver"
}

def write_to_postgres(batch_df, batch_id):
    (
        batch_df.write
        .jdbc(
            url=postgres_url,
            table="reviews",
            mode="append",
            properties=postgres_properties
        )
    )

query = (
    categorized_reviews.writeStream
    .foreachBatch(write_to_postgres)
    .outputMode("append")
    .option("checkpointLocation", "/tmp/reviewstream-postgres-checkpoint")
    .start()
)

query.awaitTermination()
