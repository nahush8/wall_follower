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
import time

class gp_predict_class:		
	def choose_action(self,state):
		with open ('8', 'rb') as fp:
			gp = pickle.load(fp)

		tempMu = 0
		arrayList = []
		X = np.arange(-1,1,0.1)
		Y = np.arange(-1,1,0.1)
		Z = np.arange(-1,1,0.1)
		for x in X:
			for y in Y:
				for z in Z:
					#print np.array((nextState,[x,y,z]))
					vector = [x,y,z]
					test = state + vector
					#print test

					arrayList.append(test)
		#print arrayList
		arrayListArray = np.array(arrayList)
		tempMu,sigma = gp.predict(arrayListArray, return_std=True, return_cov=False) 

		listmu =  list(tempMu)
		maxIndex  = listmu.index(max(listmu))
		tempList = arrayList[maxIndex]
		actionVector = tempList[-3:]
		return actionVector
