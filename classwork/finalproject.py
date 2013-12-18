import math
import matplotlib.pyplot as plt
import numpy as np
from operator import sub
import random as random

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

diff_deltay = map(sub, lower_yerror, upper_yerror) #difference between upper and lower y errors. Sign doesn't matter because we're going to square it in the next step.

#print x
#print y
#print lower_yerror
#print upper_yerror
#print asymmetric_error

w = [float(1.0/z**2.0) for z in diff_deltay]   #weight per datapoint (y terms only) for the WLLS
#print w

xsq = [i**2.0 for i in x]
sumwxsq = sum(i*j for i,j in zip(w,xsq))
sumwy = sum(i*j for i,j in zip(w,y))
sumwx = sum(i*j for i,j in zip(w,x))
sumwxy = sum(i*j*k for i,j,k in zip(w,x,y))

delta=(sum(w)*sumwxsq)-((sumwx)**2.0)
#print delta

b = ((sumwxsq*sumwy)-(sumwx*sumwxy))/delta
m = ((sum(w)*sumwxy)-(sumwx*sumwy))/delta
#print m
#print b
linear = [m*i+b for i in x]
uncb = math.sqrt(sumwxsq/delta)
uncm = math.sqrt(sum(w)/delta)


ylower = [i-j for i,j in zip(y,lower_yerror)]
yupper = [i+j for i,j in zip(y,upper_yerror)]
ywitherror = [ylower,yupper]
#print ywitherror


success = 0   #define success as getting a m & b value that give a y value within known y uncertainty
trials = 0   # define failure as an m & b value that do not give a y value within known y uncertainty

calcm=[]
calcb=[]
xout=[]
mcy=[]
yout=[]

xindex = 0

for i in range (1,100):
	for i in x:
		xindex = int(i)
		trials +=1.0

		mcm = random.random()
		mcb = random.random()

		mcy = i*mcm+mcb

		if mcy <= yupper[xindex] and mcy >= ylower[xindex]:
			success +=1.0
			calcm.append(float(mcm))
			calcb.append(float(mcb))
			xout.append(float(i))
			yout.append(float(mcy))

ratio = success/trials

MCslopeavg = np.mean(calcm)
MCinteravg = np.mean(calcb)

#print "# of successes %s " % success
#print "# of trials %s " % trials
#print "Ratio of successes to trials %s " % ratio
print "Monte Carlo m = %s " % MCslopeavg
print "Monte Carlo b = %s" % MCinteravg

#mclinear = [i*j+k for i,j,k in zip(xout,calcm,calcb)]
avgmclinear = [i*MCslopeavg+MCinteravg for i in x]

stdev_m = (((1.0/(len(calcm)-1.0))*sum([(i-MCslopeavg)**2.0 for i in calcm]))**0.5)/(len(calcm)**0.5)

stdev_b = (((1.0/(len(calcb)-1.0))*sum([(i-MCinteravg)**2.0 for i in calcb]))**0.5)/(len(calcb)**0.5)

print "The weighted linear least-squares fit line follows the format y = mx+b"
print "Analytically derived values for the slope and intercept are: m = %s +/- %s and b = %s +/- %s" % (m, uncm, b, uncb)
print "Computed values for the slope and intercept are: m = %s =/- %s and b = %s =/- %s" % (MCslopeavg,stdev_m,MCinteravg,stdev_b)


plt.figure(1)
plt.scatter(x,y)
plt.errorbar(x, y, xerr=None, yerr=asymmetric_error,linestyle='None')
plt.plot(x, linear)
plt.plot(x, avgmclinear)
plt.ylim(ymax=max(y)+10,ymin=min(y)-5)
plt.xlabel('x')
plt.ylabel('y')
plt.show()
