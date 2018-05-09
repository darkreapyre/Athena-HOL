# This script will listen to a Kinesis stream and process the messages by writing them into a PARQUET file stored on S3

from __future__ import print_function
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream
from pyspark.sql import HiveContext
import logging
import json

logger = logging.getLogger('py4j')

targetPath="s3://srfrnk-doit/parquet/"
kinesisStreamName='srfrnk_doit'

def write_lines(rdd):
    # Since messages may not always be sent we may receive empty RDDs which must be ignored to prevent exceptions.
    if not rdd.isEmpty():
        # Transform the JSON strings inside the RDD into JSON content
        json_rdd=rdd.map(lambda x:json.loads(x))

        # Create DataFrames from the RDD - this add a schema to the data.
        # We use the schema of the table we initialized at the beginning.
        rows=sqlContext.createDataFrame(json_rdd, table.schema)

        # Insert the DataFrames content into a temp hive table (in-memory) before they can persisted into external storage
        rows.registerTempTable('temp_rdd')

        # Save the DataFrames into a PARQUET file set at the S3 path
        rows.write.mode("append").parquet(targetPath)


if __name__ == "__main__":
    appName='KinesisStream2PARQUET'

    sc = SparkContext()

    # Connect to the hive context of our spark context.
    sqlContext = HiveContext(sc)

    # Define an external hive table from the PARQUET files stored in S3 to be used to retrieve the schema of the data.
    # The schema will be used to parse the messages coming from the Kinesis stream and thus must match it.
    sqlContext.sql("CREATE EXTERNAL TABLE IF NOT EXISTS yellow_trips_schema(" +
                   "pickup_timestamp BIGINT, dropoff_timestamp BIGINT, vendor_id STRING, pickup_datetime TIMESTAMP, dropoff_datetime TIMESTAMP, pickup_longitude FLOAT, pickup_latitude FLOAT, dropoff_longitude FLOAT, dropoff_latitude FLOAT, rate_code STRING, passenger_count INT, trip_distance FLOAT, payment_type STRING, fare_amount FLOAT, extra FLOAT, mta_tax FLOAT, imp_surcharge FLOAT, tip_amount FLOAT, tolls_amount FLOAT, total_amount FLOAT, store_and_fwd_flag STRING) " +
                   "STORED AS parquet " +
                   "LOCATION 's3://nyc-yellow-trips/parquet/'")

    ssc = StreamingContext(sc, 1)

    # Create an RDD of a single row just to get the schema. No data will be actually read except for the schema.
    table=sqlContext.sql("select * from yellow_trips_schema limit 1");

    # Connect to the Kinesis stream - create an RDD of stream messages
    lines = KinesisUtils.createStream(ssc, appName, kinesisStreamName,
                                      'https://kinesis.us-east-1.amazonaws.com', 'us-east-1',
                                      InitialPositionInStream.LATEST, 2)
    # Iterate over messages as they arrive.
    lines.foreachRDD(write_lines)

    # Since we are using a streaming context we need tell the streaming context to start polling for new stream events.
    ssc.start()

    # The line below will keep the job running until it is explicitly stopped.
    ssc.awaitTermination()

