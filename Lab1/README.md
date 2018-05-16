# Lab 1: Analysis of data in Amazon S3 using Amazon Athena

* [Creating Amazon Athena Database and Table](#creating-amazon-athena-database-and-table)
    * [Create Athena Database](#create-database)
    * [Create Athena Table](#create-a-table)  
* [Querying data from Amazon S3 using Amazon Athena](#querying-data-from-amazon-s3-using-amazon-athena)
* [Querying partitioned data using Amazon Athena](#querying-partitioned-data-using-amazon-athena)
    * [Create Athena Table with Partitions](#create-a-table-with-partitions)
    * [Adding partition metadata to Amazon Athena](#adding-partition-metadata-to-amazon-athena)
    * [Querying partitioned data set](#querying-partitioned-data-set)
* [Summary](#summary)
    
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
    CREATE DATABASE <username>
````
>__Note:__ Where `username` is the AIM user you are logged into the console as.

6.	Ensure `<username>`appears in the DATABASE list on the **Catalog** dashboard.

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
2. Ensure the `<username>` database is selected from the **DATABASE** list and then choose **New Query**.
3. In the query pane, copy the following statement to create TaxiDataYellow table, and then choose **Run Query**:

````sql
CREATE EXTERNAL TABLE IF NOT EXISTS taxi_csv(
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
SELECT * FROM taxi_csv limit 10
````

Results for the above query look like the following:
![athenaselectquery-yellowtaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenaselectquery-yellowtaxi.png)

2.	Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to get the total number of taxi rides for yellow cabs. 

````sql
SELECT COUNT(1) as TotalCount FROM taxi_csv
````
Results for the above query look like the following:
![athenacountquery-yelllowtaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenacountquery-yelllowtaxi.png)

>**Note:** The current data format is CSV and this query is scanning **~207GB** of data and takes **~14.6** seconds to execute the query.

3. Make a note of query execution time for later comparison while querying the data set in Apache Parquet format in Lab 4. 

4. Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to query for the number of rides per vendor, along with the average fair amount for yellow taxi rides

````sql
SELECT 
CASE vendorid 
    WHEN '1' THEN 'Creative Mobile Technologies'
    WHEN '2' THEN 'VeriFone Inc'
    ELSE vendorid END AS Vendor,
COUNT(1) as RideCount, 
avg(total_amount) as AverageAmount
FROM taxi_csv
WHERE total_amount > 0
GROUP BY (1)
````
Results for the above query should look similar the following:
![athenacasequery-yelllowtaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenacasequery-yelllowtaxi.png)

>**Note:** The current data format is CSV and this query is scanning **~207GB** of data and takes **~17.1** seconds to execute the query.

## Querying partitioned data using Amazon Athena

By partitioning your data, you can restrict the amount of data scanned by each query, thus improving performance and reducing cost. Athena leverages Hive for [partitioning](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-AlterPartition) data. You can partition your data by any key. A common practice is to partition the data based on time, often leading to a multi-level partitioning scheme. For example, a customer who has data coming in every hour might decide to partition by year, month, date, and hour. Another customer, who has data coming from many different sources but loaded one time per day, may partition by a data source identifier and date.

### Create a Table with Partitions

1. Ensure that current AWS region is **US West (Oregon)** region

2. Ensure `<username>` is selected from the DATABASE list and then choose **New Query**.

3. In the query pane, copy the following statement to create a the NYTaxiRides table, and then choose **Run Query**:

````sql
CREATE EXTERNAL TABLE taxi_parquet (
    vendorid STRING,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    ratecode INT,
    passenger_count INT,
    trip_distance DOUBLE,
    fare_amount DOUBLE,
    total_amount DOUBLE,
    payment_type INT
    )
  PARTITIONED BY (YEAR INT, MONTH INT, TYPE string)
  STORED AS PARQUET
  LOCATION 's3://us-west-2.serverless-analytics/canonical/NY-Pub'
````

4.Ensure the table you just created appears on the Catalog dashboard for the selected database.

![athenatablecreatequery-nytaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenatablecreatequery-nytaxi.png)

>**Note:** Running the following sample query on the `TaxiData_parquet` table you just created will not return any result as no metadata about the partition is added to the Amazon Athena table catalog.  
>```sql 
>SELECT * FROM taxi_parquet limit 10
>``` 

### Adding partition metadata to Amazon Athena

Now that you have created the table you need to add the partition metadata to the Amazon Athena Catalog.

1. Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to add partition metadata.

```sql
MSCK REPAIR TABLE taxi_parquet
```
The returned result will contain information for the partitions that are added to NYTaxiRides for each taxi type (yellow, green, fhv) for every month for the year from 2009 to 2016

>**Note:**
> The MSCK REPAIR TABLE automatically adds partition data based on the New York taxi ride data to in the Amazon S3 bucket is because the data is already converted to Apache Parquet format partitioned by year, month and type, where type is the taxi type (yellow, green or fhv). If the data layout does not confirm with the requirements of MSCK REPAIR TABLE the alternate approach is to add each partition manually using ALTER TABLE ADD PARTITION. You can also automate adding partitions by using the JDBC driver.

### Querying partitioned data set

Now that you have added the partition metadata to the Athena data catalog you can now run your query.

1. Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to get the total number of taxi rides

```sql
SELECT count(1) as TotalCount from taxi_parquet
```
Results for the above query look like the following:

![athenacountquery-nytaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenacountquery-nytaxi.png)

<!--**Note:**
> This query executes much faster because the data set is partitioned and it in optimal format - Apache Parquet (an open source columnar). Following is a comparison of the execution time and amount of data scanned between the data formats:
>
>>**CSV Format:**
>>```sql
>>SELECT count(*) as count FROM TaxiData_csv
>>```
>>Run time: **~21.74 seconds**, Data scanned: **~207.54GB**, Count: **1,310,911,060**
>>```sql
>>SELECT * FROM TaxiData_csv limit 1000
>>```
>>Run time: **~1.013 seconds**, Data scanned: **~479.7MB**
>
>>**Parquet Format:**
>>```sql
>>SELECT count(*) as count FROM TaxiData_parquet
>>```
>>Run time: **~4.79 seconds**, Data scanned: **0KB**, Count: **2,870,781,820**
>>```sql
>>SELECT * FROM TaxiData_parquet limit 1000
>>```
>>Run time: **~1.1 seconds**, Data scanned: **5.6MB**
-->

2. Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to get the total number of taxi rides by year

```sql
SELECT YEAR, count(1) as TotalCount from taxi_parquet GROUP BY YEAR
```

Results for the above query look like the following:

![athenagroupbyyearquery-nytaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenagroupbyyearquery-nytaxi.png)

3. Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to get the top 12 months by total number of rides across all the years

```sql
SELECT YEAR, MONTH, COUNT(1) as TotalCount 
FROM taxi_parquet
GROUP BY (1), (2) 
ORDER BY (3) DESC LIMIT 12
```
Results for the above query look like the following:

![athenacountbyyearquery-nytaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenacountbyyearquery-nytaxi.png)

4. Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to get the monthly ride counts per taxi time for the year 2016.

```sql
SELECT MONTH, TYPE, COUNT(1) as TotalCount 
FROM taxi_parquet
WHERE YEAR = 2016 
GROUP BY (1), (2)
ORDER BY (1), (2)
```
Results for the above query look like the following:

![athenagroupbymonthtypequery-nytaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenagroupbymonthtypequery-nytaxi.png)

>**Note:** Now the execution time is ~ 4 seconds, as the amount of data scanned by the query is restricted thus improving performance. This is because the data set is partitioned and it in optimal format – Apache Parquet, an open source columnar format.

5. Choose **New Query**, copy the following statement anywhere into the query pane, and then choose **Run Query**.

```sql
SELECT MONTH,
TYPE,
    avg(trip_distance) as  avgDistance,
    avg(total_amount/trip_distance) as avgCostPerMile,
    avg(total_amount) as avgCost, 
    approx_percentile(total_amount, .99) percentile99
FROM taxi_parquet
WHERE YEAR = 2016 AND (TYPE = 'yellow' OR TYPE = 'green') AND trip_distance > 0 AND total_amount > 0
GROUP BY MONTH, TYPE
ORDER BY MONTH
```

Results for the above query look like the following:

![athenapercentilequery-nytaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenapercentilequery-nytaxi.png)

## Summary

This lab has highlighted the following key points:
1. Creating Databases and Tables using Athena cn be done using either the console wizard or SQL commands.
2. Partitioning the data improved query significantly as the following table shows:

|             |                    **Query**                   |   **Run Time**   | **Data Scanned** |   **Results**   |
|-------------|:----------------------------------------------:|:----------------:|:----------------:|:---------------:|
| **CSV**     | SELECT count(*) as count FROM TaxiData_csv     | ~21.74 seconds | ~207.54GB       | 1,310,911,060 |
| **Parquet** | SELECT count(*) as count FROM TaxiData_parquet | ~4.79 seconds  | 0KB            | 2,870,781,820 |
| **CSV**     | SELECT * FROM TaxiData_csv limit 1000          | ~1.013 seconds | ~479.7MB       | -               |
| **Parquet** | SELECT * FROM TaxiData_parquet limit 1000      | ~1.1 seconds   | ~5.6MB         | -               |

---

## License

This library is licensed under the Apache 2.0 License. 
