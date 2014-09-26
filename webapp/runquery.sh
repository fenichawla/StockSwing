#!/bin/bash

cd "/home/ubuntu/feni/simplequery/FinalQueries/"
if [ "$1" -eq "1" ]
then
    hive -f get_price_info_on_date.q
else
    hive -f get_daily_variation_for_september.q
fi
