import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

df = pd.read_csv('LoansStats3B.csv', header=1, low_memory = False)
df = df.drop(df.index[188122:])

df['issue_d_format'] = pd.to_datetime(df['issue_d'])
dfts = df.set_index('issue_d_format')
year_month_summary = dfts.groupby(lambda x: x.year * 100 + x.month).count()
year_month_summary.index = pd.to_datetime(year_month_summary.index, format=%Y%m)

plt.figure()
loan_count_summary.plot()

sm.graphics.tsa.plot_acf(loan_count_summary)
sm.graphics.tsa.plot_pacf(loan_count_summary)
