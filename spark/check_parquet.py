from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("CheckParquet")
    .getOrCreate()
)

df = spark.read.parquet("/opt/spark/work-dir/data/processed")

df.printSchema()
df.show(truncate=False)

spark.stop()