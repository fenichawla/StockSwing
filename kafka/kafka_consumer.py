#!/usr/bin/env python
# Implementation of kafka consumer which writes to HBase intraday table
import datetime
import happybase
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer

# Initialize kafka
kafka = KafkaClient("localhost:9092")

# To consume messages - These will be intra-day stock 
consumer = SimpleConsumer(kafka, "my-group", "feni")

# Initialize HBase 
hbase = happybase.Connection('localhost')
hbase_intraday_table = hbase.table("hbase_intraday_table")

# New intraday table which has clean data - does not include weekends data from sept 20 and 21
hbase_intraday_table2 = hbase.table('hbase_intraday_table2')

# Connect to daily HBase table, to update it in real time as well
hbase_daily = hbase.table('hbase_daily_table3')

# Write to file as a proof that this script was called
wr_file = open('/home/ubuntu/feni/data/kafka_logs/consumer_logfile.txt','a')

# write to log file for daily data
daily_log = open('/home/ubuntu/feni/data/kafka_logs/consumer_daily_data_log.txt','a')

# Write data to a file which will be synced with HDFS repeatedly
#hdfs_file = open('/home/ubuntu/feni/data/rt/hdfs_sync.txt','a')

daily_log.write("Daily data logging started\n")

# Write all the intra-day stock values to HBase table 
for message in consumer:
    # create key for the intraday hbase table
    # Rowkey = ticker symbol + date + time
    now = str(datetime.datetime.now())
    currentdatetime = str(now).split(" ")
    date = currentdatetime[0]
    time = (currentdatetime[1].split("."))[0]

    messagesplit = str(message.message.value).rstrip().split(",")

    # Add to file for debugging and to ensure cron is running
    wr_file.write(now + ": Writing message: " + str(message.message.value) + "\n")

    # Make sure the row that was read has three columns to remove incorrect reads or error messages                                                        
    if len(messagesplit) != 3:
        continue;

    rowkey = messagesplit[0] + "_" + date + "_" + time
    highvalue = messagesplit[1]
    lowvalue = messagesplit[2]

    if highvalue != "N/A" and lowvalue != "N/A" and not highvalue[0].isalpha() and not lowvalue[0].isalpha():
        # Adding to fix bad data obtained from yahoo
        if highvalue < lowvalue:
            temp = highvalue
            highvalue = lowvalue
            lowvalue = temp

        variance = ((float(highvalue) - float(lowvalue))/float(lowvalue)) * 100

        hbase_intraday_table.put(rowkey, {'cf1:variance':str(variance), 'cf1:high_value':str(highvalue), 'cf1:low_value':str(lowvalue)})

        hbase_intraday_table2.put(rowkey, {'cf1:variance':str(variance), 'cf1:high_value':str(highvalue), 'cf1:low_value':str(lowvalue)})

        wr_file.write(now + ": Written to HBase\n") 
        
        # Update daily data in HBase based on this streamed data 
        daily_rowkey = messagesplit[0] + "_" + date

        daily_result = hbase_daily.row(daily_rowkey)
        
        if daily_result == {}: # value does not exist in the daily table
            daily_log.write("No matching data in the table at time: " + now)
            new_high = highvalue 
            new_low = lowvalue 
            new_variance = variance
            #hbase_daily.put(daily_rowkey, {'cf1:variance':str(variance), 'cf1:high_value':str(highvalue), 'cf1:low_value':str(lowvalue)})
        else:
            if highvalue > daily_result['cf1:high_value']:
                new_high = highvalue
            else:
                new_high = daily_result['cf1:high_value']
            if lowvalue < float(daily_result['cf1:low_value']):
                new_low = lowvalue
            else:
                new_low = daily_result['cf1:low_value']
            new_variance = (float(new_high) - float(new_low)) / float(new_low) * 100

        hbase_daily.put(daily_rowkey, {'cf1:variance':str(new_variance), 'cf1:high_value':str(new_high), 'cf1:low_value':str(new_low)})

        daily_log.write("writing to daily table at time: " + now)
        daily_log.write(daily_rowkey + "cf1:variance: " + str(new_variance) + "cf1:high_value:" + str(new_high) + "cf1:low_value:" + str(new_low) + "\n")


        # TODO - Also write this data to a file which will be written to HDFS periodically through a sh script. The sh script will be  run every night using cron 

hbase.close()
wr_file.close()    
daily_log.close()
