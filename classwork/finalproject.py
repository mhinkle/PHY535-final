import math
import matplotlib.pyplot as plt
import numpy as np
from operator import sub
import random as random


### Read in data from file ###
#inputname = raw_input('Please enter the filepath of your input file: ')
inputname = "/home/mlh/classwork/finaldata.dat"
f = open(inputname,'r')
x = []
y = []
lower_yerror = []
upper_yerror = []

for line in f:
	if line.split()[0][0] != '#':
		x.append(float(line.split()[0]))
		y.append(float(line.split()[1]))
		lower_yerror.append(float(line.split()[2]))
		upper_yerror.append(float(line.split()[3]))

asymmetric_error = [lower_yerror, upper_yerror] #y errors for later use in plotting error bars

### Calculate linear least-squares fit ###

diff_deltay = map(sub, lower_yerror, upper_yerror) #difference between upper and lower y errors. Sign doesn't matter because we're going to square it in the next step.

w = [float(1.0/z**2.0) for z in diff_deltay]   #weight per datapoint (y terms only) for the WLLS

xsq = [i**2.0 for i in x]
sumwxsq = sum(i*j for i,j in zip(w,xsq))
sumwy = sum(i*j for i,j in zip(w,y))
sumwx = sum(i*j for i,j in zip(w,x))
sumwxy = sum(i*j*k for i,j,k in zip(w,x,y))

delta=(sum(w)*sumwxsq)-((sumwx)**2.0)

b = round(((sumwxsq*sumwy)-(sumwx*sumwxy))/delta,5) # intercept
m = round(((sum(w)*sumwxy)-(sumwx*sumwy))/delta,5) # slope

linear = [m*i+b for i in x] # linear fit line
uncb = round(math.sqrt(sumwxsq/delta),5) # uncertainty in intercept
uncm = round(math.sqrt(sum(w)/delta),5) # uncertainty in slope

### Calculate the magnitude of the y uncertainty on each data point ###

ylower = [i-j for i,j in zip(y,lower_yerror)]  # Known y value - lower error
yupper = [i+j for i,j in zip(y,upper_yerror)]  # Known y value + upper error
ywitherror = [ylower,yupper]  # List of the possible lower and upper y bounds on each data point


### Compute linear fit line via Monte Carlo simulation ###

success = 0   # define success as getting a m & b value that give a y value within known y uncertainty
trials = 0   # number of trials performed (this is a counter, not a limiting parameter)

simulations = 500000

calcm=[]
calcb=[]
xout=[]
mcy=[]
yout=[]

xindex = 0

### Use random numbers for the slope m and intercept b. If the y value computed with these numbers lies within the known uncertainty of y, record the m, b, x, and y values for that simulation and classify it as a successful simulation. ###

for i in range (1,simulations):
	#for i in x:
	#	xindex = int(i)
	trials +=1.0

	mcm = random.random()
	mcb = random.random()

	for i in x:
		xindex = int(i)
		mcy = i*mcm+mcb

		if mcy <= yupper[xindex] and mcy >= ylower[xindex]:
			success +=1.0
			calcm.append(float(mcm)) 
			calcb.append(float(mcb))
			xout.append(float(i))
			yout.append(float(mcy))

ratio = success/trials

MCslopeavg = np.mean(calcm) # Average of all "successful" slope values
MCinteravg = np.mean(calcb) # Average of all "successful" intercept values


avgmclinear = [i*MCslopeavg+MCinteravg for i in x]

stdev_m = round((((1.0/(len(calcm)-1.0))*sum([(i-MCslopeavg)**2.0 for i in calcm]))**0.5)/(len(calcm)**0.5),5) # Stdev of the mean of the computed slope
stdev_b = round((((1.0/(len(calcb)-1.0))*sum([(i-MCinteravg)**2.0 for i in calcb]))**0.5)/(len(calcb)**0.5),5) # Stdev of the mean of the computed intercept
MCslopeavg = round(MCslopeavg,5)
MCinteravg = round(MCinteravg,5)

### Display results ###

print "The weighted linear least-squares fit line follows the format y = mx+b"
print "Analytically derived values for the slope and intercept are: m = %s +/- %s and b = %s +/- %s" % (m, uncm, b, uncb)
print "Computed values for the slope and intercept are: m = %s +/- %s and b = %s +/- %s" % (MCslopeavg,stdev_m,MCinteravg,stdev_b)


plt.figure(1)
plt.scatter(x,y)
plt.errorbar(x, y, xerr=None, yerr=asymmetric_error,linestyle='None')
plt.plot(x, linear)
plt.plot(x, avgmclinear)
plt.ylim(ymax=max(y)+10,ymin=min(y)-5)
plt.xlabel('x')
plt.ylabel('y')
plt.show()
