# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 00:43:00 2015

@author: Kruthika
"""

import pandas as pd
import sqlite3 as lite
import collections
import time
import datetime

con = lite.connect('citi_bike.db')
cur = con.cursor()

df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

hour_change = collections.defaultdict(int)
for col in df.columns:
    station_vals = df[col].tolist()
    station_id = col[1:] #trim the "_"
    station_change = 0
    for k,v in enumerate(station_vals):
        if k < len(station_vals) - 1:
            station_change += abs(station_vals[k] - station_vals[k+1])
    hour_change[int(station_id)] = station_change #convert the station id back to integer
    
def keywithmaxval(d):
    # create a list of the dict's keys and values; 
    v = list(d.values())
    k = list(d.keys())

    # return the key with the max value
    return k[v.index(max(v))]

# assign the max key to max_station
max_station = keywithmaxval(hour_change)

#query sqlite for reference information
cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print "The most active station is station id %s at %s latitude: %s longitude: %s " % data
print "With %d bicycles coming and going in the hour between %s and %s" ( hour_change[max_station],
    datetime.datetime.fromtimestamp(float(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S'),
    datetime.datetime.fromtimestamp(float(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S'),
)

import matplotlib.pyplot as plt

plt.bar(hour_change.keys(), hour_change.values())
plt.show()