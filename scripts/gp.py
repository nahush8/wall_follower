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
		recordTraining = record[0:100]
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
		testRecord = record[0:100]
		for elements in testRecord:
			testX.append(min(elements[0]))
			testTargetX.append(elements[1])

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
		'''
		for i in range(0,len(errorList)):

			if testX[i] < 50:
				#plt.scatter(testX[i],errorList[i])
				plt.errorbar(testX[i], errorList[i], varList[i], linestyle='None', marker='^')
		'''
		plt.ylim(-2,2)
		plt.xlabel('Minimum Distance to obstacle')
		plt.ylabel('Predicted reward')
		
		for i in range(0,len(errorList)):
			if testX[i] < 50:
				if testX[i] > 3 and testX[i] < 4:
					plt.plot(testX[i],1,'.r')
				else:
					plt.plot(testX[i],-1,'.r')

		plt.show()
		