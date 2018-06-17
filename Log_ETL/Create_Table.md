```sql
CREATE EXTERNAL TABLE IF NOT EXISTS gopro.etl_test (
  `contianer` string,
  `method` string,
  `format` string,
  `controller` string,
  `action` string,
  `status` int,
  `duration` double,
  `view` double,
  `db` double,
  `timestamp` string,
  `hostname` string,
  `tag` string 
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
WITH SERDEPROPERTIES (
  'serialization.format' = '1'
) LOCATION 's3://athena-hol-722812380636-us-west-2/etl-output'
TBLPROPERTIES ('has_encrypted_data'='false');
```