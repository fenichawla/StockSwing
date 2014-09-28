#!/bin/bash

hdfs dfs -rm /user/ubuntu/feni/rt_data/*

hdfs dfs -put /home/ubuntu/feni/data/rt/hdfs_sync.txt /user/ubuntu/feni/rt_data/