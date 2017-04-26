#!/usr/bin/python

import numpy as np
import math
import random
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from scipy.stats import multivariate_normal
from scipy.integrate import dblquad
import matplotlib.pyplot as plt

np.random.seed(1)

class update_gp_class:

	def update_gp(self,record):
		recordTraining = record
		trainingX = []
		targetX = []
		tempList = []
		for elements in recordTraining:
			val =  min(elements[0])
			#print "----------"
			trainingX.append(val)
			#trainingX.append(elements[0])
			targetX.append(elements[1])
		print "IN UPDATE GP"
		binsHist = np.arange(0,6,0.01)
		plt.figure(1)
		plt.subplot(211)
		plt.hist(trainingX,bins=binsHist,color='r')
		
		DX , tX = np.matrix(trainingX), np.matrix(targetX)	
		#For 2D case
		#DX , tX = np.array(trainingX), np.array(targetX)	
		errorList = []
		varList = []
		print DX.shape
		print tX.shape
		
		kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
		
		gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9,alpha=1e-2)	

		print "DOING GP FIT"
		gp.fit(DX.transpose(), tX.transpose())
		
		#For 2D case
		#gp.fit(DX, tX) 
		
		print "DONE GP FIT"
		
		testX = []
		testTargetX = []
		testRecord = np.arange(0,6,0.01)
		for elements in testRecord:
			testX.append(elements)

		predictRecord = np.matrix( testX )

		#predictRecord = np.array( testX )
		#print predictRecord
		i = 0
		#for element in predictRecord:
		for element in predictRecord.transpose():
			#print element
			mu,sigma  = gp.predict( element, return_std=True, return_cov=False)
			#print i
			#print mu[0]			
			#print testTargetX[i]
			#print sigma
			#error =  abs(testTargetX[i] - mu[0])
			#print error
			#print "----------"
			errorList.append(mu[0])
			varList.append(sigma[0])
			i+=1	
		plt.subplot(212)
		for i in range(0,len(errorList)):

			if testX[i] < 50:
				#plt.scatter(testX[i],errorList[i])
				plt.errorbar(testX[i], errorList[i], varList[i], linestyle='None', marker='^',ecolor='g')
		
		plt.xlim(0,7)
		plt.xlabel('Minimum Distance to obstacle')
		plt.ylabel('Predicted reward')
		
		iterator = np.arange(0,6,0.01)
		for i in iterator:
			if i > 3 and i < 4:
				plt.plot(i,1,'.b')
			else:
				plt.plot(i,-1,'.b')

		plt.show()
		