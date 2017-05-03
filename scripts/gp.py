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
		for element in range (0,len(record)):
			#print recordTraining[element][0]
			for item in range(0,len(record[element][0])):
				if record[element][0][item] == 9999:
					record[element][0][item] = 8

		recordTraining =random.sample(record,800)
		testSet = []
		for item in record:
			#print item
			if item not in recordTraining:
				#print item
				testSet.append(item)
		#recordTraining = record
		print len(testSet)
		trainingX = []
		trainingMinX = []
		targetX = []
		tempList = []
		for elements in recordTraining:
			val =  min(elements[0])
			#if val <= 7:
			#print "----------"
			trainingMinX.append(val)
			trainingX.append(elements[0])
			targetX.append(elements[1])
		print "IN UPDATE GP"
		

		binsHist = np.arange(0,6,0.01)
		plt.figure(1)
		plt.subplot(311)
		plt.xlabel('Minimum Distance to obstacle')
		plt.ylabel('Number of Samples')
		plt.hist(trainingMinX,bins=binsHist,color='r')
		plt.grid()
		plt.subplot(312)
		plt.scatter(trainingMinX,targetX,color='red')
		plt.grid()
		
		#DX , tX = np.matrix(trainingMinX), np.matrix(targetX)	
		#For 2D case
		DX , tX = np.array(trainingX), np.array(targetX)	
		
		errorList = []
		varList = []
		print DX.shape
		print tX.shape
		kernel = C(1.0, (1e-3, 1e3)) * RBF(1, (1e-1, 1e1)) #C is a constant kernel and RBF is the squared exp kernel.
		
		gp = GaussianProcessRegressor(kernel=kernel,optimizer='fmin_l_bfgs_b' ,n_restarts_optimizer=9,alpha=1e-2)
		#gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9,alpha=1e-2)	
		
		print "DOING GP FIT"
		#gp.fit(DX.transpose(), tX.transpose())
		#print gp.get_params()
		
		#For 2D case
		gp.fit(DX, tX) 
		
		print "DONE GP FIT"
		
		testX = []
		testMinX = []
		testTargetX = []
		
		#testRecord = np.arange(0,6,0.01)
		#for elements in testRecord:
		#	testX.append(elements)
		#predictRecord = np.matrix( testX )
		for elements in testSet:
			val =  min(elements[0])
			testMinX.append(val)
			testX.append(elements[0])
			testTargetX.append(elements[1])

		predictRecord = np.array( testX )
		#print predictRecord
		i = 0
		for element in predictRecord:
		#for element in predictRecord.transpose():
			#print element
			mu,sigma  = gp.predict(element, return_std=True, return_cov=False)
			#print i
			#print mu[0]			
			#print testTargetX[i]
			#print sigma
			error =  abs(testTargetX[i] - mu[0])
			print error
			print "----------"
			errorList.append(mu[0])
			varList.append(sigma[0])
			i+=1	
		plt.subplot(313)
		for i in range(0,len(errorList)):

			#if testX[i] < 50:
				#plt.scatter(test[i],errorList[i])
			plt.errorbar(testMinX[i], errorList[i], varList[i], linestyle='None', marker='^',ecolor='g')
		#plt.xlim(0,7)
		plt.xlabel('Minimum Distance to obstacle')
		plt.ylabel('Predicted reward')
		
		iterator = np.arange(0,6,0.001)
		for i in iterator:
			if i > 3 and i < 4:
				plt.plot(i,1,'.b')
			else:
				plt.plot(i,-1,'.b')
		plt.grid()
		plt.show()
		