# Lab 2: Serverless ETL and Data Discovery using Amazon Glue

* [Create an IAM Role](#create-an-iam-role)
* [Create an Amazon S3 bucket](#create-an-amazon-s3-bucket)
* [Discover the Data](#discover-the-data)
* [Optimize the Queries and convert into Parquet](#optimize-the-queries-and-convert-into-parquet)
* [Query the Partitioned Data using Amazon Athena](#query-the-partitioned-data-using-amazon-athena)
* [Deleting the Glue database, crawlers and ETL Jobs created for this Lab](#deleting-the-glue-database-crawlers-and-etl-jobs-created-for-this-lab)
* [Summary](#summary)

## Architectural Diagram
![architecture-overview-lab3.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/Screen+Shot+2017-11-17+at+1.11.32+AM.png)

## Create an IAM Role

Create an IAM role that has permission to your Amazon S3 sources, targets, temporary directory, scripts, **AWSGlueServiceRole** and any libraries used by the job. You can click [here](https://console.aws.amazon.com/iam/home?region=us-west-2#/roles) to create a new role. For additional documentation to create a role [here](docs.aws.amazon.com/cli/latest/reference/iam/create-role.html).

1. On the IAM Page, click on **Create Role**.
2. Choose the service as **Glue** and click on **Next: Permissions** on the bottom.
3. On the Attach permissions policies, search policies for S3 and check the box for **AmazonS3FullAccess**. 

> Do not click on the policy, you just have to check the corresponding checkbox. 

4. On the same page, now search policies for Glue and check the box for **AWSGlueServiceRole** and **AWSGlueConsoleFullAccess**.

> Do not click on the policy, you just have to check the corresponding checkbox. 

5. Click on **Next: Review**.
6. Enter Role name as 

```
nycitytaxianalysis-reinv
```

​	and click Finish.

## Create an Amazon S3 bucket

1. Open the [AWS Management console for Amazon S3](https://s3.console.aws.amazon.com/s3/home?region=us-west-2)
2. On the S3 Dashboard, Click on **Create Bucket**. 

![createbucket.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/createbucket.png)

1. In the **Create Bucket** pop-up page, input a unique **Bucket name**. So it’s advised to choose a large bucket name, with many random characters and numbers (no spaces). It will be easier to name your bucket

   ```
   aws-glue-scripts-<YOURAWSACCOUNTID>-us-west-2
   ```

   and it would be easier to choose/select this bucket for the remainder of this Lab3. 

   i.Select the region as **Oregon**. 
   ii. Click **Next** to navigate to next tab. 
   iii. In the **Set properties** tab, leave all options as default. 
   iv. In the **Set permissions** tag, leave all options as default.
   v. In the **Review** tab, click on **Create Bucket**

![createbucketpopup.png](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab1/createbucketpopup.png)

2. Now, in this newly created bucket, create two sub-buckets **tmp** and **target** using the same instructions as the above step. We will use these buckets as part of Lab3 later on. 

## Discover the Data

During this workshop, we will focus on one month of the New York City Taxi Records dataset, however you could easily do this for the entire eight years of data. As you crawl this unknown dataset, you discover that the data is in different formats, depending on the type of taxi. You then convert the data to a canonical form, start to analyze it, and build a set of visualizations. All without launching a single server.

> For this lab, you will need to choose the **US West (Oregon)** region. 

1. Open the [AWS Management console for Amazon Glue](https://us-west-2.console.aws.amazon.com/glue/home?region=us-west-2#). 

2. To analyze all the taxi rides for January 2016, you start with a set of data in S3. First, create a database for this workshop within AWS Glue. A database is a set of associated table definitions, organized into a logical group. In Athena, database names are all lowercase, no matter what you type.

   i. Click on **Databases** under Data Catalog column on the left. 

   ![glue1](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_1.PNG)

   ii. Click on the **Add Database** button. 

   iii. Enter the Database name as **nycitytaxianalysis-reinv17**. You can skip the description and location fields and click on **Create**. 

3. Click on **Crawlers** under Data Catalog column on the left. 

   ![glue2](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_2.PNG)

   i. Click on **Add Crawler** button. 

   ii. Under Add information about your crawler, for Crawler name type **nycitytaxianalysis-crawler-reinv17**. You can skip the Description and Classifiers field and click on **Next**. 

   iii. Under Data Store, choose S3. And Ensure the radio button for **Crawl Data in Specified path** is checked. 

   iv. For Include path, enter the following S3 path and click on **Next**.

   ```
   s3://serverless-analytics/glue-blog
   ```

   v. For Add Another data store, choose **No** and click on **Next**.

   vi. For Choose an IAM Role, select **Create an IAM role** and enter the role name as following and click on **Next**.

   ```
   nycitytaxianalysis-reinv17-crawler
   ```

   vii. For Create a schedule for this crawler, choose Frequency as **Run on Demand** and click on **Next**.

   viii. Configure the crawler output database and prefix:

   ​	a. For **Database**, select the database created earlier, **nycitytaxianalysis-reinv17**.

   ​	b. For **Prefix added to tables (optional)**, type **reinv17_** and click on **Next**.

   ​	c. Review configuration and click on **Finish** and on the next page, click on **Run it now** in the green box on the top. 

   ![glue14](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_14.PNG)

   ​	d. The crawler runs and indicates that it found three tables.

4. Click on **Tables**, under Data Catalog on the left column. 

5. If you look under **Tables**, you can see the three new tables that were created under the database nycitytaxianalysis-reinv17.

   ![glue4](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_4.PNG)

6. The crawler used the built-in classifiers and identified the tables as CSV, inferred the columns/data types, and collected a set of properties for each table. If you look in each of those table definitions, you see the number of rows for each dataset found and that the columns don’t match between tables. As an example, clicking on the reinv17_yellow table, you can see the yellow dataset for January 2017 with 8.7 million rows, the location on S3, and the various columns found.

   ![glue5](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_5.PNG)

## Optimize the Queries and convert into Parquet 

Create an ETL job to move this data into a query-optimized form. You convert the data into a column format, changing the storage type to Parquet, and writing the data to a bucket that you own.

1. Open the [AWS Management console for Amazon Glue](https://us-west-2.console.aws.amazon.com/glue/home?region=us-west-2#). 

2. Click on **Jobs** under ETL on the left column and then click on the **Add Job** button. 

3. Under Job properties, input name as **nycitytaxianalysis-reinv17-yellow**. Since we will be working with only the yellow dataset for this workshop.

   i. Under  IAM Role, Choose the IAM role created at the beginning of this lab. 

   x. Under This job runs, choose the radio button for **A proposed script generated by AWS Glue**.

   xi. For Script file name, enter **nycitytaxianalysis-reinv17-yellow**.

   > For this workshop, we are only working on the yellow dataset. Feel free to run through these steps to also convert the green and FHV dataset. 

   xii. For S3 path where script is stored, click on the Folder icon and choose the S3 bucket created at the beginning of this workshop. **Choose the newly created S3 bucket via the Folder icon**. 

   xiii. For Temporary directory, choose the tmp folder created at the beginning of this workshop. **Choose the S3 bucket via the Folder icon** and click **Next**. 

   > Ensure the temporary bucket is already created/available in your S3 bucket. 

   ![glue15](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_15.PNG)

   xiv. Click on Advanced properties, and select **Enable** for Job bookmark.

   xv. Here's a screenshot of a finished job properties window:

   ![glue16](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_16.PNG)

4. Click **Next**.

5. Under Choose your data sources, select **reinv17_yellow** table as the data source and click on **Next**.

   > For this workshop, we are only working on the yellow dataset. Feel free to run through these steps to also convert the green and FHV dataset. 

6. Under Choose your data targets, select the radio button for **Create tables in your data target**.

   i. For Data store, Choose **Amazon S3**.

   ii. For Format, choose **Parquet**.

   iii. For Target path, **click on the folder icon** and choose the target folder previously created. **This S3 Bucket/Folder will contain the transformed Parquet data**.

![glue17](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_17.PNG)

7. Under Map the source columns to target columns page,

   i. Under Target, change the Column name **tpep_pickup_datetime** to **pickup_date**. Click on its respective **data type** field string and change the Column type to **TIMESTAMP** and click on **Update**.

   ii. Under Target, change the Column name **tpep_dropoff_datetime** to **dropoff_date**. Click on its respective **data type** field string and change the Column type to **TIMESTAMP** and click on **Update**.

   iii. Choose **Next**, verify the information and click **Finish**.

![glue9](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_9.PNG)

8. On the auto-generated script page, click on **Save** and **Run Job**.

![glue10](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_10.PNG)

8. In the parameters pop-up, for Job bookmark, ensure its **Enable** and click on **Run Job**. 

9. This job will run for roughly around 30 minutes.

   ![glue11](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_11.PNG)

10. You can view logs on the bottom page of the same page.

  ![glue12](https://s3-us-west-2.amazonaws.com/reinvent2017content-abd313/lab3/glue_12.PNG)

11. The target folder (S3 Bucket) specified above (step 6 iii) will now have the converted parquet data. 
