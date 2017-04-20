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
		recordTraining = record[0:799]
		trainingX = []
		targetX = []
		for elements in recordTraining:
			trainingX.append(elements[0])
			targetX.append( elements[1] )
		print "IN UPDATE GP"

		DX , tX = np.array( trainingX ), np.array( targetX )
		errorList = []
		#print DX
		#print tX
		kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
		
		gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9,alpha=1e-2)		
		print "DOING GP FIT"
		gp.fit(DX, tX)
		print "DONE GP FIT"

		testX = []
		testTargetX = []
		testRecord = record[800:1000]
		for elements in testRecord:
			testX.append(elements[0])
			testTargetX.append(elements[1])

		predictRecord = np.array( testX )
		#print predictRecord
		i = 0
		for element in predictRecord:
			#print element
			mu,sigma  = gp.predict( element, return_std=True, return_cov=False)
			print i
			print mu[0]
			print testTargetX[i]
			#print sigma
			error =  testTargetX[i] - mu[0]
			print error
			print "----------"
			errorList.append(error)
			i+=1
		print errorList
		plt.plot(errorList)
		plt.show()
		