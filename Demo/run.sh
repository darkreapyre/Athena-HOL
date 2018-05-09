#!/usr/bin/env bash

export AWS_ACCESS_KEY_ID=<your-access-key>
export AWS_SECRET_KEY=<your-secret-key>

scp -i ~/.aws/srfrnk_doit.pem job.py hadoop@ec2-52-203-2-42.compute-1.amazonaws.com:~/job.py
scp -i ~/.aws/srfrnk_doit.pem generate.py hadoop@ec2-54-80-254-179.compute-1.amazonaws.com:~/generate.py

spark-submit --packages org.apache.spark:spark-streaming-kinesis-asl_2.11:2.1.0 job.py
spark-submit --packages org.apache.spark:spark-streaming-kinesis-asl_2.11:2.1.0 generate.py

