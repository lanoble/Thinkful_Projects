import requests
import collections
from dateutil.parser import parse
import sqlite3 as lite
from pandas.io.json import json_normalize
import pandas as pd
import matplotlib.pyplot as plt

r = requests.get('http://www.citibikenyc.com/stations/json')

df = json_normalize(r.json()['stationBeanList'])

con = lite.connect('citi_bike.db')
cur = con.cursor()

#a prepared SQL statement to execute over and over again
sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

#for loop to populate values in the database
with con:
    cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY,totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT)')
    for station in r.json()['stationBeanList']:
        cur.execute(sql,(station['id'],station['totalDocks'],station['city'], station['altitude'], station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

#extract from the DataFrame and put them into a list
station_ids = df['id'].tolist()
#add the '_' to the station name and also add the data type for SQLite
station_ids = ('_' + str(x) + ' INT' for x in station_ids)

#create the table
#in this case, we're concatenating the string and joining all the station ids, now with '_' and 'INT' added
with con:
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " + ", ".join(station_ids) + ");")

#pull data from citibike every minute for an hour
for i in range(60):
	exec_time = parse(r.json()['executionTime'])

	cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%Y-%m-%dT%H:%M:%S'),)) #use %s if running on a mac
	con.commit()

	id_bikes = collections.defaultdict(int)
	for station in r.json()['stationBeanList']:
		id_bikes[station['id']] = station['availableBikes']

	for k, v in id_bikes.iteritems():
		cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE (execution_time) = (?);", (exec_time.strftime('%Y-%m-%dT%H:%M:%S'),)) #use %s if running on a mac
	con.commit()

	time.sleep(60)

#analyze citibike data
hour_change = collections.defaultdict(int)
for col in df.columns:
    station_vals = df[col].tolist()
    station_id = col[1:]
    station_change = 0
    for k,v in enumerate(station_vals):
        if k < len(station_vals) - 1:
            station_change += abs(station_vals[k] - station_vals[k+1])
    hour_change[int(station_id)] = station_change

def keywithmaxval(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]

max_station = keywithmaxval(hour_change)

cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print "The most active station is station id %s at %s latitude: %s longitude: %s " %data
print "With " + str(hour_change[379]) + " bicycles coming and going in the hour between " + str(df.index[0])) + " and " + str(df.index[-1]))

con.close() #close the database connection when done