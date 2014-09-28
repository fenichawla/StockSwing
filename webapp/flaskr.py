# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2014 by Feni Chawla.
    :license: BSD, see LICENSE for more details.
"""

import os
import re
import happybase
import datetime

from subprocess import Popen, PIPE
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create our little application :)
app = Flask(__name__)
hbase = happybase.Connection('localhost')
hbase.open()

qs = []

@app.route("/history")
def history():
    return render_template('history.html', hist=qs)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/qindex")
def query_index():
    return render_template('qindex.html')

# Function called to build query string
def buildquery(maincomp, sdate, edate, comps, gran):
    sdate_str = sdate.strftime('%Y-%m-%d')
    edate_str = edate.strftime('%Y-%m-%d')
    qry="Date range : " + sdate_str + " to " + edate_str + " ( " + gran + " ) "
    val = 1

    # Feni: what is qs and val?
    if (qs == []):
        val = 1
    else:
        val = 1 - (qs[0][4])
    elem = [ sdate_str, edate_str, maincomp + ";" + comps, gran, val ]
    qs.insert(0, elem)
    return qry

def processdailyquery(sdate, edate, maincomp, comps):
    print "############DAILY QUERY##############"
    klist = []
    # process the data from daily table, build the key list
###    hbase_table_seeded = hbase.table("hbase_date_result_table")
#    hbase_table_seeded = hbase.table("hbase_daily_vol_table")
    hbase_table_seeded = hbase.table("hbase_daily_table3")
    clist=re.findall(r"[\w']+", comps)

    d = sdate
    delta = datetime.timedelta(days=1)
    while d <= edate:
###        key = maincomp + " " + d.strftime('%Y-%m-%d')
        
        key = maincomp + d.strftime('%Y-%m-%d')
        klist.append(key)
        d += delta
    sklist = [] #this is a list of lists
    for c in clist:
        d=sdate
        sklistc = []
        while d <= edate:
###            key = c + " " + d.strftime('%Y-%m-%d')
            key = c + d.strftime('%Y-%m-%d')
            sklistc.append(key)
            d += delta
        sklist.append(sklistc)

    # retrieve results from Hbase
    hresults = hbase_table_seeded.rows(klist)
    results = [dict(date=re.sub('[A-Z ]','',i), val=float(j['cf1:volatility_daily'])) for i, j in hresults]

    # build list of all results
    clist.insert(0, maincomp)
    result_lists = []
    result_lists.append(results)
    for l in sklist:
        hresults = hbase_table_seeded.rows(l)
###        results = [dict(date=re.sub('[A-Z ]', '',i), val=float(j['cf1:vol_daily'])) for i, j in hresults]
        results = [dict(date=re.sub('[A-Z ]', '',i), val=float(j['cf1:volatility_daily'])) for i, j in hresults]
        result_lists.append(results)
    resmap = {}
    i=0
    resmap = [dict(sym=a, res=b) for a, b in zip(clist, result_lists)]
    for a,b in resmap:
        print "####"
        print "SYM:"+a
        print "RESULT:"+b
    return resmap

def processintradayquery(sdate, edate, maincomp, comps):
    # Connect to the HBase table for intraday table
    hbase_intra = hbase.table("hbase_intraday_table2")
    print "#################################################"
    print "NEW INTRADAY QUERY"
    print "#################################################"

    # create list of companies whose fluctuation has to be plotted
    complist = []
    complist = list(comps.split(";"))
    complist.insert(0,maincomp)
    complist = filter(lambda a: a != "", complist)
#    complist.append("")
    print complist

    # Initialize result dict
    resdict = []

    for company in complist:
        klist = []
        d = sdate
        delta = datetime.timedelta(days=1)

        while d <= edate:
            k = company + "_" + d.strftime('%Y-%m-%d')
            klist.append(k)
            d += delta

        print klist

        # Initialize dict containing date:result
        dateresult = []

        for each in klist:
            print "key = " 
            print each
            #varlist = hbase_intra.scan(row_prefix=each)
            #print varlist
            for key, data in hbase_intra.scan(row_prefix = each):
                print "After table scan"
                #print each
                # create dict containing (date+time, variance) for each company
                date_time = str(key.split("_")[1] + "_" + key.split("_")[2])
                #print date_time
                ##dateresult[date_time] = data['cf1:variance']
                dateresult.append(dict(date=date_time, val=data['cf1:variance']));
                #print data['cf1:variance']
            print "############Date time dict############\n"
            print dateresult
        ##resdict[company] = dateresult
        resdict.append(dict(sym=company,res=dateresult))
    
    print "######Final dict with company: date,value pairs######\n"
    print resdict

    return resdict

@app.route("/query", methods=['POST', 'GET'])
def query():
    #klist = [] # used for storing all keys 
    errmsg=''

    # read the form data
    maincomp=request.form['maincomp']
    sdate=datetime.datetime.strptime(request.form['sdate'], '%Y-%m-%d')
    edate=datetime.datetime.strptime(request.form['edate'], '%Y-%m-%d')
    comps=request.form['comps']
    gran=request.form['granularity']

    print comps
    print gran

    # Error check
    if sdate > edate :
        return render_template('query_page.html', errmsg="**Invalide date range")

    # Build out strings used for passing messages to HTML
    qry = buildquery(maincomp, sdate, edate, comps, gran)
    
    print qry

    # TODO: Add separate function for daily query
    if gran == "daily":
        resmap = processdailyquery(sdate, edate, maincomp, comps)
    else:
        resmap = processintradayquery(sdate, edate, maincomp, comps) 

    return render_template('graph.html', prevq=qry, results=resmap)

@app.route("/")
def index():
    return render_template('query_page.html', prevq='')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

    hbase.close()
