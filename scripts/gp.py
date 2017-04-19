#!/usr/bin/python

import numpy as np
import math
import random
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from scipy.stats import multivariate_normal
from scipy.integrate import dblquad
import matplotlib.pyplot as plt
import pickle
np.random.seed(1)

class update_gp_class:

	def update_gp(self,record):
		trainingX = []
		targetX = []
		for elements in record:
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
		i = 0

		with open ('training_set', 'rb') as fp:
			content = pickle.load(fp)


		for elements in content:
			trainingX.append(elements[0])

		predictRecord = trainingX[80:100]
		#print predictRecord
		
		for element in predictRecord:
			#print element
			mu,sigma  = gp.predict( element, return_std=True, return_cov=False)
			#print mu
			#print sigma
			error =  tX[i] - mu
			errorList.append(error[0])
			i+=1
		print errorList
		plt.plot(errorList)
		plt.show()
		