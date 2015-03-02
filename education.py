from bs4 import BeautifulSoup
import numpy as np
import collections
import requests
import re
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3 as lite
import csv
import math

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

response = requests.get(url)
soup = BeautifulSoup(response.content)

#get table with un data and strip html tags as well as white space from the table
table = soup('table')[8]
data = table.stripped_strings

#filter to only the elements of the data table desired, removing legend letters
unData = []
for line in data:
    if re.match(r"\S{2,}[ \S\w+]*$|\d",line):
        unData.append(line)

#remove un-needed header information        
unData = unData[4:]

#create list of lists for easy pandas transfer
dataFrameList = []
while len(unData) > 0:
    countryList = [unData[0], unData[1], unData[2], unData[3], unData[4]]
    dataFrameList.append(countryList)
    unData = unData[5:]

# create and clean pandas table
df_UN = pd.DataFrame(dataFrameList[1:], columns=dataFrameList[0])
df_UN.drop('Total', axis=1, inplace=True)
df_UN.rename(columns={"Country or area":"Country"}, inplace=True)
df_UN['Women'] = df_UN['Women'].astype(float)
df_UN['Men'] = df_UN['Men'].astype(float)
df_UN['Year'] = df_UN['Year'].astype(int)

#retrieve descriptive statistics for un data
df_UN['Women'].describe()
df_UN['Men'].describe()

#plot un data to see distribution
plt.hist(df_UN['Women'],histtype='bar')
plt.show()

plt.hist(df_UN['Men'],histtype='bar')
plt.show()

#create database and un data table
con = lite.connect('gdpToEducation.db')
cur = con.cursor()
df_UN.to_sql('unData', con)

#create table in database for gdp data
with con:
	cur.execute('CREATE TABLE gdp (country_name TEXT, _1999 REAL, _2000 REAL, _2001 REAL, _2002 REAL, _2003 REAL, _2004 REAL, _2005 REAL, _2006 REAL, _2007 REAL, _2008 REAL, _2009 REAL, _2010 REAL)')

#insert data into gdp table
with open('ny.gdp.mktp.cd_Indicator_en_csv_v2.csv', 'rU') as inputFile:
    next(inputFile)
    next(inputFile)
    header = next(inputFile)
    inputReader = csv.reader(inputFile)
    for line in inputReader:
        cur.execute('INSERT INTO gdp (country_name, _1999, _2000, _2001, _2002, _2003, _2004, _2005, _2006, _2007, _2008, _2009, _2010) VALUES ("' + line[0] + '","' + '","'.join(line[43:-5]) + '");')

#create pandas dataframe with gdp information
with con:
    cur.execute('SELECT * FROM gdp')
    gdp_data = cur.fetchall()
    df_GDP = pd.DataFrame(gdp_data)

#set gdp index and clean up pandas table
df_GDP.columns = ['Country','1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010']
df_GDP.set_index('Country', inplace=True)
df_GDP.replace('', np.nan, inplace=True)

#set un index and add column for gdp information for specific year
df_UN.set_index('Country', inplace=True)
df_UN['gdp'] = np.nan 

#find and add gdp information for specific year
for country in df_UN.index:
    if country in df_GDP.index:
        year = df_UN['Year'].loc[country]
        df_UN['gdp'].loc[country] = df_GDP[str(year)].loc[country]
    continue

#drop rows without gdp information
df_UN.dropna(how='any', inplace=True)

#log transformation on gdp information
df_UN['gdp'] = df_UN['gdp'].map(lambda x: math.log(x, 10))

#correlation between Women education and GDP
df_UN['Women'].corr(df_UN['gdp'])

#correlaiton between Men education and GDP
df_UN['Men'].corr(df_UN['gdp'])