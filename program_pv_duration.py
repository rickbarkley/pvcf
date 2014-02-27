import pandas as pd
import numpy as np
from pandas import DataFrame, Series
import math

records = pd.read_csv('call_report.SDF', sep=';')
#create the DataFrame
frame = DataFrame(records)

cFrame = frame[frame.Value.notnull()]

value = cFrame['Value']

rcbValue = value.where(cFrame['Call Schedule'].str.contains('RCB'))
bondThree = value.where(cFrame['MDRM #'].str.contains('RCONA551'))
bondFive = value.where(cFrame['MDRM #'].str.contains('RCONA552'))
bondTen = value.where(cFrame['MDRM #'].str.contains('RCONA553'))
mortgageTen = value.where(cFrame['MDRM #'].str.contains('RCONA559'))
mortgageThirty = value.where(cFrame['MDRM #'].str.contains('RCONA560'))

bondThreeNan = bondThree.dropna()
bondFiveNan = bondFive.dropna()
bondTenNan = bondTen.dropna()
mortgageTenNan = mortgageTen.dropna()
mortgageThirtyNan = mortgageThirty.dropna()

bond3 = bondThreeNan.astype(int)
bond5 = bondFiveNan.astype(int)
bond10 = bondTenNan.astype(int)
mortgage10 = mortgageTenNan.astype(int)
mortgage30 = mortgageThirtyNan.astype(int)

#get rid of NaN values
rcbValue2 = rcbValue.dropna()
#change string values to integers
rcbValue3 = rcbValue2.astype(int)

#output RCB integers to CSV file.
#rcbvalue3.to_csv('Documents/BarkleyMorrisonInc/rcbvaluesinteger2.csv')
#strip out 0's
rcb4s = rcbValue3[rcbValue3 > 0]
#print rcb4
#assuming rate and yield are 5.5% n(number of payments per period) = 1, and t(term of the security) = 15
# Cashflow = bond * coupon

r = .09
n = 2

secPrice = rcb4s.sum()
print "sumed value of all RCB Data:"
print secPrice
rawCashFlow = np.asarray(rcb4s * (r/n)).sum()
print "Total Cashflow coming in per period:"
print rawCashFlow

print "******PVCF, Duration, and Convexity of combined Securities Cash Flows******"

def pvcfFunc(time):
	pvcf = 0
	for t in range(1,time):
	    pvcf = np.asarray(rawCashFlow / (1 + (r/n)) ** t) + pvcf
	pvcfFinal = np.asarray(rawCashFlow + secPrice / (1 + (r/n)) ** time)
	print "Present Value of combined future cashflow is:"
	pvcfComplete = pvcfFinal + pvcf
	print pvcfComplete
pvcfFunc(10)

#***Duration***

print "***Duration***"
#PV * time - needed for Duration Equation
 

print "Running Total of Discounted cashflows from period 1 - 9 (* t):"

def pvcfTimeFunc(time):
	pvcfTime = 0
	for t in range(1,time):
	    pvcfTime = np.asarray((rawCashFlow / (1 + (r/n)) ** t) * t) + pvcfTime
	pvcfTimeFinal = np.asarray((rawCashFlow + secPrice / (1 + (r/n)) ** time) * time)
	pvcfCompleteTime = pvcfTimeFinal + pvcfTime
	duration = (pvcfCompleteTime /(n*secPrice))
	print "Duration equals"
	print duration
pvcfTimeFunc(10)

#***Convexity***

print "***Convexity***"

print "Running Total of Discounted cashflows from period 1 - 9 (* t * (1+t)):"
def convexityFunc(time):
	pvcfConvexity = 0
	for t in range(1,time):
	    pvcfConvexity = np.asarray(((rawCashFlow / (1 + (r/n)) ** t) * t * (1+t)) + pvcfConvexity)
	pvcfConvexityFinal = np.asarray((((rawCashFlow + secPrice) / (1 + (r/n)) ** time) * time) * (1+time))
	pvcfCompleteConvexity = pvcfConvexityFinal + pvcfConvexity
	convexityDenominator = ((1 + (r/n))**2) * ((n**2) * secPrice)
	convexity = pvcfCompleteConvexity / convexityDenominator
	print "Convexity equals:"
	print convexity
convexityFunc(10)

print "******PVCF, Duration, and Convexity of combined 3 Year securities non-mortgate backed******"

r = .09
n = 1
rawCashFlow = (bond3 * (r/n))
secPrice = bond3

def presentValueFunction(x):
	def pvcfFunc(time):
		pvcf = 0
		for t in range(1,time):
		    pvcf = np.asarray(rawCashFlow / (1 + (r/n)) ** t) + pvcf
		pvcfFinal = np.asarray(rawCashFlow + secPrice / (1 + (r/n)) ** time)
		pvcfComplete = pvcfFinal + pvcf
		print "Present Value of combined future cashflows is:"
		print pvcfComplete
	pvcfFunc(x)

	#***Duration***

	print "***Duration***"

	def pvcfTimeFunc(time):
		pvcfTime = 0
		for t in range(1,time):
		    pvcfTime = np.asarray((rawCashFlow / (1 + (r/n)) ** t) * t) + pvcfTime
		pvcfTimeFinal = np.asarray((rawCashFlow + secPrice / (1 + (r/n)) ** time) * time)
		pvcfCompleteTime = pvcfTimeFinal + pvcfTime
		duration = (pvcfCompleteTime /(n*secPrice))
		print "Duration equals"
		print duration
	pvcfTimeFunc(x)

	#***Convexity***

	print "***Convexity***"

	def convexityFunc(time):
		pvcfConvexity = 0
		for t in range(1,time):
		    pvcfConvexity = np.asarray(((rawCashFlow / (1 + (r/n)) ** t) * t * (1+t)) + pvcfConvexity)
		pvcfConvexityFinal = np.asarray((((rawCashFlow + secPrice) / (1 + (r/n)) ** time) * time) * (1+time))
		pvcfCompleteConvexity = pvcfConvexityFinal + pvcfConvexity
		convexityDenominator = ((1 + (r/n))**2) * ((n**2) * secPrice)
		convexity = pvcfCompleteConvexity / convexityDenominator
		print "Convexity equals:"
		print convexity
	convexityFunc(x)
presentValueFunction(3)

print "******PVCF, Duration, and Convexity of combined 5 Year securities non-mortgate backed******"
r = .09
n = 1
rawCashFlow = (bond5 * (r/n))
secPrice = bond5
presentValueFunction(5)

print "******PVCF, Duration, and Convexity of combined 10 Year securities non-mortgate backed******"
r = .09
n = 1
rawCashFlow = (bond10 * (r/n))
secPrice = bond10
presentValueFunction(10)

print "******PVCF, Duration, and Convexity of combined 10 Year securities *mortgate backed******"
r = .055
n = 12
rawCashFlow = (mortgage10 * (r/n))
secPrice = mortgage10
presentValueFunction(10)

print "******PVCF, Duration, and Convexity of combined 30 Year securities *mortgate backed******"
r = .055
n = 12
rawCashFlow = (mortgage30 * (r/n))
secPrice = mortgage30
presentValueFunction(30)




