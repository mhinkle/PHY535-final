import math
import matplotlib.pyplot as plt
import numpy as np
from operator import sub

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

print "The weighted linear least-squares fit line follows the format y = mx+b, where m = %s +/- %s and b = %s +/- %s" % (m, uncm, b, uncb)

plt.figure(1)
plt.scatter(x,y)
plt.errorbar(x, y, xerr=None, yerr=asymmetric_error,linestyle='None')
plt.plot(x, linear)
plt.ylim(ymax=max(y)+10,ymin=min(y)-5)
plt.xlabel('x')
plt.ylabel('y')
plt.show()

ylower = [i-j for i,j in zip(y,lower_yerror)]
yupper = [i+j for i,j in zip(y,upper_yerror)]
ywitherror = [ylower,yupper]
print ywitherror
