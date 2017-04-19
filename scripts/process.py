#!/usr/bin/python
import gp
import pickle 

gp_obj = gp.update_gp_class()
with open ('training_set', 'rb') as fp:
	record = pickle.load(fp)
print record
gp_obj.update_gp(record)