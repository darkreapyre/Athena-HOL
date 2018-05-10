# Lab 4: Athena Query Optmization

* TOC



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