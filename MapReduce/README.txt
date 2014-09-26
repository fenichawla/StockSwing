This folder contains files needed to run the Hive query for generating daily volatility and storing the result in a HBase table.

Here is the order in which the files should be run:
1. Load all the raw tables into HDFS and run a hive query to generate a table which can be loaded into HBase for fast querying - hive -f create_result_table_for_hbase.q

2. Create HBase table
   hcat -f createhbasetable.ddl

3. Copy over result of hive query onto local machine
   hdfs dfs -get /user/ubuntu/feni/data/hbase_resultdata

4. Merge all the result tables together into one file using cat

5. Write the merged table back to HDFS
   hdfs dfs -put /user/ubuntu/feni/data/hbase_table

6. Run the script for writing this result to HBase table
   pig moveresultstohbase.pig --> Does not work, so use step 7

7. Use importTsv tool to import result table into HBase
   hbase org.apache.hadoop.hbase.mapreduce.ImportTsv '-Dimporttsv.separator=,'
            -Dimporttsv.columns=HBASE_ROW_KEY,cf1:high,cf1:low,
            cf1:volatility hbase_result_table /user/ubuntu/feni/HBaseResult/HBaseResult.csv
