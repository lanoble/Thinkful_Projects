import datetime as dt
import sqlite3 as lite
import requests
import collections
import pandas as pd
import numpy as np

cities = {"Atlanta": '33.762909,-84.422675',
          "Philadelphia": '40.009376,-75.133346',
          "Seattle": '47.620499,-122.350876',
          "Miami": '25.775163,-80.208615',
          "Denver": '39.761850,-104.881105'
          }

apiKey = 'ff9c353cf28bc05ed6810113fb389c60'
request_url = 'https://api.forecast.io/forecast/' + apiKey + '/'
end_date = dt.datetime.now()

con = lite.connect('weather.db')
cur = con.cursor()

#with con:
#    cur.execute("CREATE TABLE daily_temp (queried_date TEXT, Atlanta REAL, Philadelphia REAL, Seattle REAL, Miami REAL, Denver REAL);")

query_date = end_date - dt.timedelta(days=30)

with con:
	while query_date < end_date:
		cur.execute("INSERT INTO daily_temp (queried_date) VALUES (?)", (query_date.strftime('%Y-%m-%dT12:00:00'),))
		
		query_date += dt.datetime(days=1)

for k,v in cities.iteritems():
	query_date = end_date - dt.timedelta(days=30)
	while query_date < end_date:
		r = requests.get(request_url + v + ',' + query_date.strftime('%Y-%m-%dT12:00:00'))
		with con:
			cur.execute("UPDATE daily_temp SET " + k + " = ? WHERE queried_date = ?", (str(r.json()['daily']['data'][0]['temperatureMax']), query_date.strftime('%Y-%m-%dT12:00:00'),))
	
		query_date += dt.timedelta(days=1)
		
df = pd.read_sql("SELECT * FROM daily_temp ORDER BY queried_date", con, index_col='queried_date')

diffs = {}
columns = df.columns

for col in columns[1:]:
    diffs[col] = np.diff(df[col])   