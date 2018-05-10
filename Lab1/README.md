# Lab 1: Analysis of data in Amazon S3 using Amazon Athena

* [Creating Amazon Athena Database and Table](#creating-amazon-athena-database-and-table)
    * [Create Athena Database](#create-database)
    * [Create Athena Table](#create-a-table)  
* [Querying data from Amazon S3 using Amazon Athena](#querying-data-from-amazon-s3-using-amazon-athena)
* [Querying partitioned data using Amazon Athena](#querying-partitioned-data-using-amazon-athena)
    * [Create Athena Table with Partitions](#create-a-table-with-partitions)
    * [Adding partition metadata to Amazon Athena](#adding-partition-metadata-to-amazon-athena)
    * [Querying partitioned data set](#querying-partitioned-data-set)
    
## Architectural Diagram
![architecture-overview-lab1.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/Screen+Shot+2017-11-17+at+1.11.18+AM.png)


## Creating Amazon Athena Database and Table 

Amazon Athena uses Apache Hive to define tables and create databases. Databases are a logical grouping of tables. When you create a database and table in Athena, you are simply describing the schema and location of the table data in Amazon S3\. In case of Hive, databases and tables don’t store the data along with the schema definition unlike traditional relational database systems. The data is read from Amazon S3 only when you query the table. The other benefit of using Hive is that the metastore found in Hive can be used in many other big data applications such as Spark, Hadoop, and Presto. With Athena catalog, you can now have Hive-compatible metastore in the cloud without the need for provisioning a Hadoop cluster or RDS instance. For guidance on databases and tables creation refer [Apache Hive documentation](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL). The following steps provides guidance specifically for Amazon Athena.

### Create Database

1. Open the [AWS Management Console for Athena](https://console.aws.amazon.com/athena/home).
2. If this is your first time visiting the AWS Management Console for Athena, you will get a Getting Started page. Choose **Get Started** to open the Query Editor. If this isn't your first time, the Athena **Query Editor** opens.
3. Make a note of the AWS region name, for example, for this lab you will need to choose the **US West (Oregon)** region.
4. In the Athena **Query Editor**, you will see a query pane with an example query. Now you can start entering your query in the query pane.
5. To create a database named *mydatabase*, copy the following statement, and then choose **Run Query**:

````sql
    CREATE DATABASE mydatabase
````

6.	Ensure *mydatabase* appears in the DATABASE list on the **Catalog** dashboard

![athenacatalog.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenacatalog.png)

### Create a Table
Now that you have a database, you are ready to create a table that is based on the New York taxi sample data. You define columns that map to the data, specify how the data is delimited, and provide the location in Amazon S3 for the file. 

>**Note:** 
>When creating the table, you need to consider the following:
>-	You must have the appropriate permissions to work with data in the Amazon S3 location. For more information, refer [Setting User and Amazon S3 Bucket Permissions](http://docs.aws.amazon.com/athena/latest/ug/access.html).
>-	The data can be in a different region from the primary region where you run Athena as long as the data is not encrypted in Amazon S3. Standard inter-region data transfer rates for Amazon S3 apply in addition to standard Athena charges.
>-	If the data is encrypted in Amazon S3, it must be in the same region, and the user or principal who creates the table must have the appropriate permissions to decrypt the data. For more information, refer [Configuring Encryption Options](http://docs.aws.amazon.com/athena/latest/ug/encryption.html).
>-	Athena does not support different storage classes within the bucket specified by the LOCATION clause, does not support the GLACIER storage class, and does not support Requester Pays buckets. For more information, see [Storage Classes](http://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html),[Changing the Storage Class of an Object in Amazon S3](http://docs.aws.amazon.com/AmazonS3/latest/dev/ChgStoClsOfObj.html), and [Requester Pays Buckets](http://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html) in the Amazon Simple Storage Service Developer Guide.

1. Ensure that current AWS region is **US West (Oregon)** region
2. Ensure **mydatabase** is selected from the **DATABASE** list and then choose **New Query**.
3. In the query pane, copy the following statement to create TaxiDataYellow table, and then choose **Run Query**:

````sql
    CREATE EXTERNAL TABLE IF NOT EXISTS TaxiDataYellow (
      VendorID STRING,
      tpep_pickup_datetime TIMESTAMP,
      tpep_dropoff_datetime TIMESTAMP,
      passenger_count INT,
      trip_distance DOUBLE,
      pickup_longitude DOUBLE,
      pickup_latitude DOUBLE,
      RatecodeID INT,
      store_and_fwd_flag STRING,
      dropoff_longitude DOUBLE,
      dropoff_latitude DOUBLE,
      payment_type INT,
      fare_amount DOUBLE,
      extra DOUBLE,
      mta_tax DOUBLE,
      tip_amount DOUBLE,
      tolls_amount DOUBLE,
      improvement_surcharge DOUBLE,
      total_amount DOUBLE
    )
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    STORED AS TEXTFILE
    LOCATION 's3://us-west-2.serverless-analytics/NYC-Pub/yellow/'
````

>**Note:** 
>-	If you use CREATE TABLE without the EXTERNAL keyword, you will get an error as only tables with the EXTERNAL keyword can be created in Amazon Athena. We recommend that you always use the EXTERNAL keyword. When you drop a table, only the table metadata is removed and the data remains in Amazon S3.
>-	You can also query data in regions other than the region where you are running Amazon Athena. Standard inter-region data transfer rates for Amazon S3 apply in addition to standard Amazon Athena charges. 
>-	Ensure the table you just created appears on the Catalog dashboard for the selected database.

![athenatablecreatequery-yellowtaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenatablecreatequery-yellowtaxi.png)

## Querying data from Amazon S3 using Amazon Athena

Now that you have created the table, you can run queries on the data set and see the results in AWS Management Console for Amazon Athena.

1. Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query**.

````sql
    SELECT * FROM TaxiDataYellow limit 10
````

Results for the above query look like the following:
![athenaselectquery-yellowtaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenaselectquery-yellowtaxi.png)

2.	Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to get the total number of taxi rides for yellow cabs. 

````sql
    SELECT COUNT(1) as TotalCount FROM TaxiDataYellow
````
Results for the above query look like the following:
![athenacountquery-yelllowtaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenacountquery-yelllowtaxi.png)

>**Note:** 
The current data format is CSV and this query is scanning **~207GB** of data and takes **~20.06** seconds to execute the query.

3. Make a note of query execution time for later comparison while querying the data set in Apache Parquet format. 

4. Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to query for the number of rides per vendor, along with the average fair amount for yellow taxi rides

````sql
    SELECT 
    CASE vendorid 
         WHEN '1' THEN 'Creative Mobile Technologies'
         WHEN '2' THEN 'VeriFone Inc'
         ELSE vendorid END AS Vendor,
    COUNT(1) as RideCount, 
    avg(total_amount) as AverageAmount
    FROM TaxiDataYellow
    WHERE total_amount > 0
    GROUP BY (1)
````
Results for the above query look like the following:
![athenacasequery-yelllowtaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenacasequery-yelllowtaxi.png)

---

## License

This library is licensed under the Apache 2.0 License. 
