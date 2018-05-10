--Example of converting to Parquet/columnar formats
ADD JAR /usr/lib/hive-hcatalog/share/hcatalog/hive-hcatalog-core-1.0.0-amzn-5.jar;
CREATE EXTERNAL TABLE impressions (
  requestBeginTime string, 
  adId string, 
  impressionId string, 
  referrer string,
  userAgent string, 
  userCookie string, 
  ip string, 
  number string, 
  processId string, 
  browserCookie string, 
  requestEndTime string, 
  timers struct<modelLookup:string, requestTime:string>, 
  threadId string, 
  hostname string, 
  sessionId string)
PARTITIONED BY (dt string)
ROW FORMAT  serde 'org.apache.hive.hcatalog.data.JsonSerDe'
with serdeproperties ( 'paths'='requestBeginTime, adId, impressionId, referrer, userAgent, userCookie, ip' )
LOCATION 's3://${hiveconf:REGION}.elasticmapreduce/samples/hive-ads/tables/impressions' ;

msck repair table impressions;
 
CREATE EXTERNAL TABLE  parquet_hive (
  requestBeginTime string, 
  adId string, 
  impressionId string, 
  referrer string,
  userAgent string, 
  userCookie string, 
  ip string)
STORED AS PARQUET
LOCATION '${hiveconf:OUTPUT}';

INSERT OVERWRITE TABLE parquet_hive SELECT requestbegintime,adid,impressionid,referrer,useragent,usercookie,ip FROM impressions where dt='2009-04-14-04-05';
