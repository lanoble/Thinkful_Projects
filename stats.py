import pandas as pd
from scipy import stats

data = '''Region, Alcohol, Tobacco
North, 6.47, 4.03
Yorkshire, 6.13, 3.76
Northeast, 6.19, 3.77
East Midlands, 4.89, 3.34
West Midlands, 5.63, 3.47
East Anglia, 4.52, 2.92
Southeast, 5.89, 3.20
Southwest, 4.79, 2.71
Wales, 5.27, 3.53
Scotland, 6.08, 4.51
Northern Ireland, 4.02, 4.56'''

data = data.splitlines()
data = [i.split(', ') for i in data]

column_names = data[0]
data_rows = data[1::]
df = pd.DataFrame(data_rows, columns=column_names)

df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)

alc_mean = df['Alcohol'].mean()
alc_median = df['Alcohol'].median()
alc_mode = stats.mode(df['Alcohol'])
alc_range = max(df['Alcohol']) - min(df['Alcohol'])
alc_var = df['Alcohol'].var()
alc_stdev = df['Alcohol'].std()

tob_mean = df['Tobacco'].mean()
tob_median = df['Tobacco'].median()
tob_mode = stats.mode(df['Tobacco'])
tob_range = max(df['Tobacco']) - min(df['Tobacco'])
tob_var = df['Tobacco'].var()
tob_stdev = df['Tobacco'].std()

ans_string = "The {0} for the Alcohol and Tobacco dataset is {1} and {2}, respectively."

print ans_string.format('mean',str(alc_mean),str(tob_mean))
print ans_string.format('median',str(alc_median),str(tob_median))
print ans_string.format('mode',str(alc_mode[0][0]),str(tob_mode[0][0]))
print ans_string.format('range',str(alc_range),str(tob_range))
print ans_string.format('variance',str(alc_var),str(tob_var))
print ans_string.format('standard deviation',str(alc_stdev),str(tob_stdev))





