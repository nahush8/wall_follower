#!/usr/bin/python
import gpq
import pickle 

gpq_obj = gpq.gpq_class()
with open ('20170506-150632', 'rb') as fp:
	record = pickle.load(fp)
#print record[0]
#recordTraining = record[0:80]
#print recordTraining
gpq_obj.gpq_algorithm(record)
