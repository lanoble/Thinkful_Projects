import numpy as np
import pandas as pd
import statsmodels.api as sm

loansData = pd.read_csv('LoanStats3b.csv', header = 1)

loansData = loansData.drop(loansData.index[188122:])
loansData['int_rate'] = loansData['int_rate'].astype(str)
loansData['int_rate'] = map((lambda x: x[:len(x)-1]),loansData['int_rate'])
loansData['int_rate'] = loansData['int_rate'].astype(float)
loansData['annual_inc'] = loansData['annual_inc'].astype(float)

annualinc = loansData['annual_inc']
intrate = loansData['int_rate']

y = np.matrix(intrate).transpose()
x = np.matrix(annualinc).transpose()

X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()
f.summary()

loansData['home_owner'] = map((lambda x: x == 'MORTGAGE' or x == 'OWN'), loansData['home_ownership'])

loansData['intercept_constant'] = 1.0

ind_vars = ['intercept_constant', 'annual_inc']

logit = sm.Logit(loansData['home_owner'],loansData[ind_vars])
results = logit.fit()
results.summary()
