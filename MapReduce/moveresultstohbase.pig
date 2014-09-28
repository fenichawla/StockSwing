-- Copyright: (c) 2014 by Feni Chawla.
-- Load data from HDFS into HBase table
data = LOAD '/user/ubuntu/feni/data/hbase_table/hbase_daily_vol_result.txt' USING PigStorage(',') AS (c1:chararray, c2:chararray, c3:chararray);

STORE data INTO 'hbase://hbase_daily_vol_table' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('cf1:volatility_daily, cf1:high_daily, cf1:low_daily');

