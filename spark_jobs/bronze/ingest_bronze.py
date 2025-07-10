import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp

def ingest_bronze():
    spark = SparkSession.builder \
        .appName("Ingest Bronze") \
        .getOrCreate()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    data_path = os.path.join(project_root, "data/")
    bronze_path = "data/bronze/"

    products_df = spark.read.csv(f"{data_path}olist_products_dataset.csv", header=True, inferSchema=True)
    products_df.withColumn("ingestion_timestamp", current_timestamp()) \
        .write.mode("overwrite").parquet(f"{bronze_path}products")

    customers_df = spark.read.csv(f"{data_path}olist_customers_dataset.csv", header=True, inferSchema=True)
    customers_df.withColumn("ingestion_timestamp", current_timestamp()) \
        .write.mode("overwrite").parquet(f"{bronze_path}customers")

    geolocation_df = spark.read.csv(f"{data_path}olist_geolocation_dataset.csv", header=True, inferSchema=True)
    geolocation_df.withColumn("ingestion_timestamp", current_timestamp()) \
        .write.mode("overwrite").parquet(f"{bronze_path}geolocation")

    orders_df = spark.read.csv(f"{data_path}olist_orders_dataset.csv", header=True, inferSchema=True)
    orders_df.withColumn("ingestion_timestamp", current_timestamp()) \
        .write.mode("overwrite").parquet(f"{bronze_path}orders")

    order_items_df = spark.read.csv(f"{data_path}olist_order_items_dataset.csv", header=True, inferSchema=True)
    order_items_df.withColumn("ingestion_timestamp", current_timestamp()) \
        .write.mode("overwrite").parquet(f"{bronze_path}order_items")

    spark.stop()

if __name__ == "__main__":
    ingest_bronze()
