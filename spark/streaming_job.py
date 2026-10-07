from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, when, window, count
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = (
    SparkSession.builder
    .appName("ReviewStream")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Define the structure of one review
review_schema = StructType([
    StructField("review_id", IntegerType(), True),
    StructField("rating", IntegerType(), True),
    StructField("review_text", StringType(), True)
])

# Read streaming data from Kafka
reviews = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:29092")
    .option("subscribe", "reviews")
    .option("startingOffsets", "earliest")
    .load()
)

# Convert Kafka binary value into JSON and keep Kafka timestamp
json_reviews = reviews.select(
    from_json(
        col("value").cast("string"),
        review_schema
    ).alias("review"),
    col("timestamp").alias("event_time")
)

# Extract review fields
parsed_reviews = json_reviews.select(
    col("review.review_id").alias("review_id"),
    col("review.rating").alias("rating"),
    col("review.review_text").alias("review_text"),
    col("event_time")
)

# Categorize reviews based on rating
categorized_reviews = parsed_reviews.withColumn(
    "rating_category",
    when(col("rating") <= 2, "Negative")
    .when(col("rating") == 3, "Neutral")
    .otherwise("Positive")
)

windowed_metrics = (
    categorized_reviews
    .withWatermark("event_time", "10 seconds")
    .groupBy(
        window(col("event_time"), "1 minute"),
        col("rating_category")
    )
    .agg(
        count("*").alias("review_count")
    )
)
print("Connected to Kafka and parsed review schema!")

windowed_metrics.printSchema()

query = (
    windowed_metrics.writeStream
    .format("parquet")
    .option("path", "/opt/spark/work-dir/data/processed")
    .option("checkpointLocation", "/tmp/reviewstream-checkpoint")
    .outputMode("append")
    .start()
)

query.awaitTermination()