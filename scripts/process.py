#!/usr/bin/python
import gp
import pickle 

gp_obj = gp.update_gp_class()
with open ('20170426-151730', 'rb') as fp:
	record = pickle.load(fp)
#print record
#recordTraining = record[0:80]
#print recordTraining
gp_obj.update_gp(record)
