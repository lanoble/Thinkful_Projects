import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd

loansData = pd.read_csv('loansData.csv')

loansData.dropna(inplace=True)

loansData.boxplot(column='Amount.Requested')
plt.title('Amount Requested')
plt.show()

loansData.hist(column='Amount.Requested')
plt.title('Amount Requested')
plt.show()

plt.figure()
graph = stats.probplot(loansData['Amount.Requested'], dist="norm", plot=plt)
plt.title('Amount Requested')
plt.show()
