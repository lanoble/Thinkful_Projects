import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import collections

x = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]

c = collections.Counter(x)
count_sum = sum(c.values())

for k,v in c.iteritems():
	print "The frequency of number " + str(k) + " is " + str(float(v) / count_sum)

plt.boxplot(x)
plt.title("X Box Plot")
plt.show()

plt.hist(x, histtype='bar')
plt.title("X Histogram")
plt.show()

plt.figure()
graph = stats.probplot(x, dist="norm", plot=plt)
plt.title("X QQ Plot")
plt.show()

