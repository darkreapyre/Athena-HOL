# Lab 4: Athena Query Optmization

* TOC

## Querying partitioned data using Amazon Athena (Continuation from Lab 1)

By partitioning your data, you can restrict the amount of data scanned by each query, thus improving performance and reducing cost. Athena leverages Hive for [partitioning](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-AlterPartition) data. You can partition your data by any key. A common practice is to partition the data based on time, often leading to a multi-level partitioning scheme. For example, a customer who has data coming in every hour might decide to partition by year, month, date, and hour. Another customer, who has data coming from many different sources but loaded one time per day, may partition by a data source identifier and date.

### Create a Table with Partitions

1. Ensure that current AWS region is **US West (Oregon)** region

2. Ensure **mydatabase** is selected from the DATABASE list and then choose **New Query**.

3. In the query pane, copy the following statement to create a the NYTaxiRides table, and then choose **Run Query**:

````sql
  CREATE EXTERNAL TABLE NYTaxiRides (
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

>**Note:**
>	Running the following sample query on the NYTaxiRides table you just created will not return any result as no metadata about the partition is added to the Amazon Athena table catalog.  
>```sql 
>   SELECT * FROM NYTaxiRides limit 10
>``` 

### Adding partition metadata to Amazon Athena

Now that you have created the table you need to add the partition metadata to the Amazon Athena Catalog.

1. Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to add partition metadata.

```sql
    MSCK REPAIR TABLE NYTaxiRides
```
The returned result will contain information for the partitions that are added to NYTaxiRides for each taxi type (yellow, green, fhv) for every month for the year from 2009 to 2016

>**Note:**
> The MSCK REPAIR TABLE automatically adds partition data based on the New York taxi ride data to in the Amazon S3 bucket is because the data is already converted to Apache Parquet format partitioned by year, month and type, where type is the taxi type (yellow, green or fhv). If the data layout does not confirm with the requirements of MSCK REPAIR TABLE the alternate approach is to add each partition manually using ALTER TABLE ADD PARTITION. You can also automate adding partitions by using the JDBC driver.

### Querying partitioned data set

Now that you have added the partition metadata to the Athena data catalog you can now run your query.

1. Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to get the total number of taxi rides

```sql
    SELECT count(1) as TotalCount from NYTaxiRides
```
Results for the above query look like the following:

![athenacountquery-nytaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenacountquery-nytaxi.png)

>**Note:**
> This query executes much faster because the data set is partitioned and it in optimal format - Apache Parquet (an open source columnar). Following is a comparison of the execution time and amount of data scanned between the data formats:
>
>>**CSV Format:**
>>```sql
>>  SELECT count(*) as count FROM TaxiDataYellow 
>>```
>>Run time: **~20.06 seconds**, Data scanned: **~207.54GB**, Count: **1,310,911,060**
>>```sql
>>SELECT * FROM TaxiDataYellow limit 1000
>>```
>>Run time: **~3.13 seconds**, Data scanned: **~328.82MB**
>
>>**Parquet Format:**
>>```sql
>>SELECT count(*) as count FROM NYTaxiRides
>>```
>>Run time: **~5.76 seconds**, Data scanned: **0KB**, Count: **2,870,781,820**
>>```sql
>>SELECT * FROM NYTaxiRides limit 1000
>>```
>>Run time: **~1.13 seconds**, Data scanned: **5.2MB**


2. Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to get the total number of taxi rides by year

```sql
    SELECT YEAR, count(1) as TotalCount from NYTaxiRides GROUP BY YEAR
```

Results for the above query look like the following:
![athenagroupbyyearquery-nytaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenagroupbyyearquery-nytaxi.png)

3. Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to get the top 12 months by total number of rides across all the years

```sql
    SELECT YEAR, MONTH, COUNT(1) as TotalCount 
    FROM NYTaxiRides 
    GROUP BY (1), (2) 
    ORDER BY (3) DESC LIMIT 12
```
Results for the above query look like the following:

![athenacountbyyearquery-nytaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenacountbyyearquery-nytaxi.png)

4. Choose **New Query**, copy the following statement into the query pane, and then choose **Run Query** to get the monthly ride counts per taxi time for the year 2016.

```sql
    SELECT MONTH, TYPE, COUNT(1) as TotalCount 
    FROM NYTaxiRides 
    WHERE YEAR = 2016 
    GROUP BY (1), (2)
    ORDER BY (1), (2)
```
Results for the above query look like the following:

![athenagroupbymonthtypequery-nytaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenagroupbymonthtypequery-nytaxi.png)

>**Note:**
Now the execution time is ~ 3 second, as the amount of data scanned by the query is restricted thus improving performance. This is because the data set is partitioned and it in optimal format – Apache Parquet, an open source columnar format.

5. Choose **New Query**, copy the following statement anywhere into the query pane, and then choose **Run Query**.

```sql
    SELECT MONTH,
      TYPE,
      avg(trip_distance) as  avgDistance,
      avg(total_amount/trip_distance) as avgCostPerMile,
      avg(total_amount) as avgCost, 
      approx_percentile(total_amount, .99) percentile99
    FROM NYTaxiRides
    WHERE YEAR = 2016 AND (TYPE = 'yellow' OR TYPE = 'green') AND trip_distance > 0 AND total_amount > 0
    GROUP BY MONTH, TYPE
    ORDER BY MONTH
```
Results for the above query look like the following:

![athenapercentilequery-nytaxi.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/athenapercentilequery-nytaxi.png)

## Query the Columnar Data using Amazon Athena (Continuation from Lab 2)

In regions where AWS Glue is supported, Athena uses the AWS Glue Data Catalog as a central location to store and retrieve table metadata throughout an AWS account. The Athena execution engine requires table metadata that instructs it where to read data, how to read it, and other information necessary to process the data. The AWS Glue Data Catalog provides a unified metadata repository across a variety of data sources and data formats, integrating not only with Athena, but with Amazon S3, Amazon RDS, Amazon Redshift, Amazon Redshift Spectrum, Amazon EMR, and any application compatible with the Apache Hive metastore.

1. Open the [AWS Management console for Amazon Athena](https://us-west-2.console.aws.amazon.com/athena/home?force&region=us-west-2). 

   > Ensure you are in the **US West (Oregon)** region. 

2. Under Database, you should see the database **nycitytaxianalysis-reinv17** which was created during the previous section. 

3. Click on **Create Table** right below the drop-down for Database and click on **Automatically (AWS Glue Crawler)**.

4. You will now be re-directed to the AWS Glue console to set up a crawler. The crawler connects to your data store and automatically determines its structure to create the metadata for your table. Click on **Continue**.

5. Enter Crawler name as **nycitytaxianalysis-crawlerparquet-reinv17** and Click **Next**.

6. Select Data store as **S3**.

7. Choose Crawl data in **Specified path in my account**.

8. For Include path, click on the folder Icon and choose the **target** folder previously made which contains the parquet data and click on **Next**.

![glue18](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_18.PNG)

9. In Add another data store, choose **No** and click on **Next**.

10. For Choose an IAM role, select Choose an existing IAM role, and in the drop-down pick the role made in the previous section and click on **Next**.

11. In Create a schedule for this crawler, pick frequency as **Run on demand** and click on **Next**.

12. For Configure the crawler's output, Click **Add Database** and enter **nycitytaxianalysis-reinv17-parquet** as the database name and click **create**. For Prefix added to tables, you can enter a prefix **parq_** and click **Next**.

13. Review the Crawler Info and click **Finish**. Click on **Run it Now?**. 

14. Click on **Tables** on the left, and for database nycitytaxianalysis-reinv17-parquet you should see the table parq_target. Click on the table name and you will see the MetaData for this converted table. 

15. Open the [AWS Management console for Amazon Athena](https://us-west-2.console.aws.amazon.com/athena/home?force&region=us-west-2). 

    > Ensure you are in the **US West (Oregon)** region. 

16. Under Database, you should see the database **nycitytaxianalysis-reinv17-parquet** which was just created. Select this database and you should see under Tables **parq_target**.

17. In the query editor on the right, type

    ```
    select count(*) from parq_target;
    ```

    and take note the Run Time and Data scanned numbers here. 

    ![glue19](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_comp_scanresult.PNG)

    What we see is the Run time and Data scanned numbers for Amazon Athena to **query and scan the parquet data**.

18. Under Database, you should see the earlier made database **nycitytaxianalysis-reinv17** which was created in a previous section. Select this database and you should see under Tables **reinv17_yellow**. 

19. In the query editor on the right, type

    ```
    select count(*) from reinv17_yellow;
    ```

    and take note the Run Time and Data scanned numbers here. 

    ![glue20](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_uncomp_scanresult.PNG)

20. What we see is the Run time and Data scanned numbers for Amazon Athena to query and scan the uncompressed data from the previous section.


> Note: Athena charges you by the amount of data scanned per query. You can save on costs and get better performance if you partition the data, compress data, or convert it to columnar formats such as Apache Parquet.

## Deleting the Glue database, crawlers and ETL Jobs created for this Lab

Now that you have successfully discovered and analyzed the dataset using Amazon Glue and Amazon Athena, you need to delete the resources created as part of this lab. 

1. Open the [AWS Management console for Amazon Glue](https://us-west-2.console.aws.amazon.com/glue/home?region=us-west-2#). Ensure you are in the Oregon region (as part of this lab).
2. Click on **Databases** under Data Catalog column on the left. 
3. Check the box for the Database that were created as part of this lab. Click on **Action** and select **Delete Database**. And click on **Delete**. This will also delete the tables under this database. 
4. Click on **Crawlers** under Data Catalog column on the left. 
5. Check the box for the crawler that were created as part of this lab. Click on **Action** and select **Delete Crawler**. And click on **Delete**. 
6. Click on **Jobs** under ETL column on the left. 
7. Check the box for the jobs that were created as part of this lab. Click on **Action** and select **Delete**. And click on **Delete**. 
8. Open the [AWS Management console for Amazon S3](https://s3.console.aws.amazon.com/s3/home).
9. Click on the S3 bucket that was created as part of this lab. You need to click on its corresponding **Bucket icon** to select the bucket instead of opening the bucket. Click on **Delete bucket** button on the top, to delete the S3 bucket. In the pop-up window, Type the name of the bucket (that was created as part of this lab), and click **Confirm**. 

## Summary

In the lab, you went from data discovery to analyzing a canonical dataset, without starting and setting up a single server. You started by crawling a dataset you didn’t know anything about and the crawler told you the structure, columns, and counts of records.

From there, you saw the datasets were in different formats, but represented the same thing: NY City Taxi rides. You then converted them into a canonical (or normalized) form that is easily queried through Athena and possible in QuickSight, in addition to a wide number of different tools not covered in this post.

---
## License

This library is licensed under the Apache 2.0 License. 