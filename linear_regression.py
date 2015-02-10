import numpy as np
import pandas as pd
import statsmodels.api as sm 

loansData = pd.read_csv('loansData.csv')

#clean the data
loansData['Interest.Rate'] = map((lambda x: x[:len(x)-1]),loansData['Interest.Rate'])
loansData['Loan.Length'] = map((lambda x: x[:2]),loansData['Loan.Length'])
loansData['FICO.Range'] = map((lambda x: str(x).split('-')),loansData['FICO.Range'])
loansData['FICO.Score'] = map((lambda x: x[0]),loansData['FICO.Range'])

loansData['Interest.Rate'] = loansData['Interest.Rate'].astype(float)
loansData['Loan.Length'] = loansData['Loan.Length'].astype(float)
loansData['FICO.Score'] = loansData['FICO.Score'].astype(float)

#load the data to csv
loansData.to_csv('loansData_clean.csv', header=True, index=False)

#extract columns
intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

#reshape depent variable data
y = np.matrix(intrate).transpose()

#reshape indepent variables shaped as columns
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()

#put two columns together to create an input matrix
x = np.column_stack([x1,x2])

#create a linear model
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

print 'Coefficients: ', f.params[1:3]
print 'Intercept: ', f.params[0]
print 'P-Values: ', f.pvalues 
print 'R-Squared : ', f.rsquared 

