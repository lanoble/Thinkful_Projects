import pandas as pd
import math 
import matplotlib.pyplot as plt
import statsmodels.api as sm 

loansData = pd.read_csv('loansData_clean.csv')

#creation of under 12 true/false
loansData['IR.under12'] = map((lambda x: x < 12.0), loansData['Interest.Rate'])

#creation of Intercept Constant
loansData['Intercept.Constant'] = 1.0

#list of independent variables
ind_vars = ['Intercept.Constant','FICO.Score','Amount.Requested']

#define the logistic regression model
logit = sm.Logit(loansData['IR.under12'], loansData[ind_vars])

#fit the model
result = logit.fit()

#get the fitted coefficients from the results
coeff = result.params

def logistic_function(FicoScore, LoanAmount):
	p = 1 / (1 + math.e**(coeff['Intercept.Constant'] + coeff['FICO.Score']*(FicoScore) - coeff['Amount.Requested']*(LoanAmount))
	return p


