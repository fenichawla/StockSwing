-- Create stock table

CREATE EXTERNAL TABLE IF NOT EXISTS stock_data (
    ticker STRING,
    daydate STRING,
    open DOUBLE,
    high DOUBLE,
    low DOUBLE,
    close DOUBLE,
    volume DOUBLE,
    adjclose DOUBLE,
    extra STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
stored as textfile
LOCATION '/user/ubuntu/feni/data/StockData'  ;

-- Create company info table

CREATE EXTERNAL TABLE IF NOT EXISTS company_info (
    ticker STRING,
    companyname STRING,
    lastsale DOUBLE,
    marketcap DOUBLE,
    adrtso INT,
    ipoyear INT,
    sector STRING,
    industry STRING,
    summaryquote STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
stored as textfile
LOCATION '/user/ubuntu/feni/data/CompanyInfo'  ;

-- create hive table that has the result table
CREATE EXTERNAL TABLE IF NOT EXISTS hbase_table (
       ticker_date STRING,
       volatility_daily STRING,
       high_daily STRING,
       low_daily STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
stored as textfile
LOCATION '/user/ubuntu/feni/data/hbase_resultdata/'  ;

-- Insert result values into hive table 
INSERT INTO TABLE hbase_table
SELECT CONCAT(ticker, daydate),
CAST((((high - low)/low) * 100) AS STRING),
CAST (high AS STRING),
CAST (low AS STRING)
FROM stock_data;

-- Create HBase table
--CREATE TABLE IF NOT EXISTS hbase_result_table(ticker_date STRING, volatility_daily STRING)
--STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
--WITH SERDEPROPERTIES ("hbase.columns.mapping" = ":key,cf1:vol_daily");

-- Insert values into the HBase table from Hive -> Not working for huge table, so plan to use pig instead
-- INSERT OVERWRITE TABLE hbase_result_table SELECT * FROM hbase_table;