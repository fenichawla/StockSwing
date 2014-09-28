#!/usr/bin/env python                                                                             
# copyright: (c) 2014 by Feni Chawla.                                        

import urllib2
import datetime
from kafka import KafkaClient, SimpleProducer

# To send messages synchronously
kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)

# Write to file as a proof that this script was called                         
wr_file = open('/home/ubuntu/feni/data/kafka_logs/producer_logfile.txt','a')

currentdatetime = str(datetime.datetime.now())
wr_file.write(currentdatetime + ": Called from cron: starting to get data\n")

# Get all the ticker symbols whose stock data has to be collected
#companyname = "AAPL"
symbol_file=open('/home/ubuntu/feni/corpus/ticksyms','r')
symbols = symbol_file.readlines()
symbol_file.close()

for symbol in symbols:
    urlstring = ""
    urlstring += "http://download.finance.yahoo.com/d/quotes.csv?s="
    urlstring += symbol.rstrip() 
    urlstring += "&f=so0l1&e=.csv"

    response = urllib2.urlopen(urlstring)
    readlines = str(response.read().replace("\"","")).split("\n")

    for line in readlines:
        #line.rstrip("\n")
        if line == "":
            continue

        wr_file.write(currentdatetime + ": Writing message to consumer: " + line + "\n")
#        print line
        producer.send_messages("feni", line)
        wr_file.write(currentdatetime + ": Done writing to consumer\n")

kafka.close()
