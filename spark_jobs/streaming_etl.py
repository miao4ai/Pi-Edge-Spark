#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
streaming_etl.py
--------------------------------------
Example Spark Structured Streaming ETL job:
1. Reads JSON data continuously from a directory (simulating IoT / sensor stream)
2. Cleans malformed records
3. Transforms columns
4. Performs windowed aggregation
5. Writes processed data to parquet output

Run with:
spark-submit --master spark://10.0.0.6:7077 spark_jobs/streaming_etl.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, window, avg
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

def main():
    # --- 1️⃣ Create Spark session ---
    spark = (
        SparkSession.builder
        .appName("StreamingETL")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    # --- 2️⃣ Define input schema ---
    schema = StructType([
        StructField("device_id", StringType(), True),
        StructField("temperature", DoubleType(), True),
        StructField("humidity", DoubleType(), True),
        StructField("timestamp", TimestampType(), True),
    ])

    # --- 3️⃣ Define streaming source (simulated folder) ---
    input_dir = "data/stream_input"
    print(f"📡 Watching folder: {input_dir}")
    raw_stream = (
        spark.readStream
        .format("json")
        .schema(schema)
        .option("maxFilesPerTrigger", 1)
        .load(input_dir)
    )

    # --- 4️⃣ Basic cleaning: remove null or invalid temperature ---
    clean_stream = raw_stream.filter(
        (col("temperature").isNotNull()) &
        (col("humidity").isNotNull()) &
        (col("temperature") > -30) &
        (col("temperature") < 60)
    )

    # --- 5️⃣ Transformation: average temperature per 1-minute window ---
    agg_stream = (
        clean_stream
        .withWatermark("timestamp", "2 minutes")
        .groupBy(
            window(col("timestamp"), "1 minute"),
            col("device_id")
        )
        .agg(
            avg("temperature").alias("avg_temp"),
            avg("humidity").alias("avg_humidity")
        )
        .orderBy(col("window"))
    )

    # --- 6️⃣ Define streaming sink ---
    query = (
        agg_stream
        .writeStream
        .format("console")               # or "parquet", "csv", "memory"
        .outputMode("complete")
        .option("truncate", "false")
        .trigger(processingTime="10 seconds")
        .start()
    )

    # --- 7️⃣ Keep stream running ---
    query.awaitTermination()

if __name__ == "__main__":
    main()