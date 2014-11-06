#Stock Swing
Developed by Feni Chawla

StockSwing is a webapp which enables any user to query stock price fluctuations for multiple companies very quickly and easily. 

Stock Swing was implemented as a pat of a three week project for Insight Data Engineering fellowship program. I used historical and real time stock data from Yahoo finance for over 6000 companies listed on NASDAQ, NYSE and AMEX exchanges.  


##Data pipeline for StockSwing

The following data pipeline was used.



![Alt Text](https://github.com/fenichawla/InsightDataProject_StockSwing/blob/master/images/datapipeline.png "Data Pipeline for StockSwing")



  
  2 Main components of the data pipeline:
  1. Batch processing: <br>
  This is a one time operation performed on the historical data set. For batch processing, I first clean and normalize the data using several scripts written in shell and python, and then store the data in HDFS. A hive mapreduce job is then run to pre-calculate stock price fluctuation and the results are stored into HBase for quick querying.<br>
  2. Real time processing:<br>
  To provide access to real time price fluctuation, real time data processing is done on live data streamed from the cloud. This is implemented in Python using Kafka. The producer pulls data from the cloud at 15 minute intervals. There are 2 consumers at the end of the kafka queue - 1 which does the price fluctuation calculation and pushes the result to HBase, and the other which aggregates data into HDFS. 


The web application server pulls data from HBase using happybase thrift API, and pushes the results to the client. The web user interface is implemented using flask API in Python. The client displays the fluctuation results as a plot, which is implemeted using Canvas.js.


##User interface

The user interface for StockSwing is implemented using flask API on Python. Here is a snapshot of the interface


![Alt Text](https://github.com/fenichawla/InsightDataProject_StockSwing/blob/master/images/WebUI.png)



##Results of running a query on StockSwing

For easy comparison of the price fluctuations, Canvas.js is used to display the results in a line graph. An example result is shown below.


![Alt Text](https://github.com/fenichawla/InsightDataProject_StockSwing/blob/master/images/QueryResult.png)


##How to run

Please note that the AWS cluster hosting this project has now been taken off so it can not be run anymore. Before the server was disconnected it could be run using the following instructions.

To run the web application server, the following could be run on the command line:
./runwebapp.sh

The webapp could be found and run on any client by using the following URL: http://feni.mitalfamily.com/
