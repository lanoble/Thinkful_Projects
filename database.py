import sqlite3 as lite
import pandas as pd

con = lite.connect('getting_started.db')
weather = (('New York City',2013,'July','January',62),
			('Boston',2013,'July','January',59),
			('Chicago',2013,'July','January',59),
			('Miami',2013,'August','January',84),
			('Dallas',2013,'July','January',77),
			('Seattle',2013,'July','January',61),
			('Portland',2013,'July','December',63),
			('San Francisco',2013,'September','December',64),
			('Los Angeles',2013,'September','December',75))
cities = (('New York City','NY'),
			('Boston','MA'),
			('Chicago','IL'),
			('Miami','FL'),
			('Dallas','TX'),
			('Seattle','WA'),
			('Portland','OR'),
			('San Francisco','CA'),
			('Los Angeles','CA'))

with con:
	cur = con.cursor()

	# Removing existing tables and creating new ones
	cur.execute("DROP TABLE IF EXISTS weather")
	cur.execute("DROP TABLE IF EXISTS cities")
	cur.execute("CREATE TABLE weather (city text, year integer,	warm_month text, cold_month text, average_high integer)")
	cur.execute("CREATE TABLE cities (name text, state text)")

	# Insert data into tables
	cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weather)
	cur.executemany("INSERT INTO cities VALUES(?,?)", cities)

	# Join tables together
	cur.execute("SELECT name, state, year, warm_month, cold_month, average_high FROM cities INNER JOIN weather ON name = city")

	# Load data into a pandas Data Frame
	rows = cur.fetchall()
	cols = [desc[0] for desc in cur.description]
	df = pd.DataFrame(rows, columns=cols)

	# Print out resulting city and state
	cur.execute("SELECT name, state FROM cities INNER JOIN weather ON name = city GROUP BY city HAVING warm_month = 'July'")
	locations = cur.fetchall()
	output_sentence = "The cities that are warmest in July are"
	for city in locations:
		output_sentence = output_sentence + ', ' + city[0] + ', ' + city[1]
	print output_sentence + '.'



