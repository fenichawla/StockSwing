-- Copyright: (c) 2014 by Feni Chawla.
-- Create result table in HBase
CREATE TABLE
hbase_daily_vol_table (tickerdate STRING, volatility_daily STRING, high_daily STRING, low_daily STRING)
STORED BY 'org.apache.hcatalog.hbase.HBaseHCatStorageHandler'
TBLPROPERTIES (
  'hbase.table.name' = 'hbase_daily_vol_table',
  'hbase.columns.mapping' = 'cf1:volatility_daily, cf1:high_daily, cf1:low_daily',
  'hcat.hbase.output.bulkMode' = 'true'
);