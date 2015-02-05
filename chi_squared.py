from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import collections

loansData = pd.read_csv('loansData.csv')
loansData.dropna(inplace=True)

freq = collections.Counter(loansData['Open.CREDIT.Lines'])

chi, p = stats.chisquare(freq.values())

print 'chi = ' + str(chi)
print 'p = ' + str(p)