#!/usr/bin/python
import numpy as np
import rospy
import time
import random
import math
import std_msgs.msg
import matplotlib.pyplot as plt
import actionlib
import matplotlib.pyplot as plt
import wall_follower.msg
import gp
import mavros
import pickle
#import update_transition_class
from mavros.utils import *
from mavros_msgs.msg import State
from mavros_msgs.srv import SetMode, StreamRate, StreamRateRequest, CommandBool, CommandTOL
from geometry_msgs.msg import *
from sensor_msgs.msg import Joy, LaserScan

record = []
gp_obj = gp.update_gp_class()
np.random.seed(1)
counter = 0
def agent_client():
	global record
	global counter
	joyAction = [0,0,0,0]
	action_client = actionlib.SimpleActionClient('perception',wall_follower.msg.agentAction)
	action_client.wait_for_server()
	print "Connected"

	#while not rospy.is_shutdown():
	while counter < 1000:
		
		joy = rospy.wait_for_message("joy",Joy)
		#if joy.axes[0] != 0 or joy.axes[1] != 0 or joy.axes[2] != 0 or joy.axes[3] != 0:
		joyList = []
		joyList.append(abs(joy.axes[0]))
		joyList.append(abs(joy.axes[1]))
		joyList.append(abs(joy.axes[2]))
		joyList.append(abs(joy.axes[3]))

		maxjoy = max(joyList)

		if maxjoy == abs(joy.axes[0]):
			joyAction[0] = joy.axes[0] #YAW #lh
			joyAction[1] = 0 #Z  #lv
			joyAction[2] = 0 #x #rh
			joyAction[3] = 0 #y #rv
		elif maxjoy == abs(joy.axes[1]):
			joyAction[0] = 0 #YAW #lh
			joyAction[1] = joy.axes[1] #Z  #lv
			joyAction[2] = 0 #x #rh
			joyAction[3] = 0 #y #rv
		elif maxjoy == abs(joy.axes[2]):
			joyAction[0] = 0 #YAW #lh
			joyAction[1] = 0 #Z  #lv
			joyAction[2] = joy.axes[2] #x #rh
			joyAction[3] = 0 #y #rv
		elif maxjoy == abs(joy.axes[3]):
			joyAction[0] = 0 #YAW #lh
			joyAction[1] = 0 #Z  #lv
			joyAction[2] = 0 #x #rh
			joyAction[3] = joy.axes[3] #y #rv
			'''
		else:
			choose = random.randint(1,3)
			
			if choose == 0:
				joyAction[0] = float(random.sample([-1,1],1)[0]) #YAW #lh
				joyAction[1] = 0.0 #Z  #lv
				joyAction[2] = 0.0 #x #rh
				joyAction[3] = 0.0 #y #rv
			
			if choose == 1:
				joyAction[0] = 0.0 #YAW #lh
				joyAction[1] = float(random.sample([-1,1],1)[0]) #Z  #lv
				joyAction[2] = 0.0 #x #rh
				joyAction[3] = 0.0 #y #rv
			elif choose == 2:
				joyAction[0] = 0.0 #YAW #lh
				joyAction[1] = 0.0 #Z  #lv
				joyAction[2] = float(random.sample([-1,1],1)[0]) #x #rh
				joyAction[3] = 0.0 #y #rv
			elif choose == 3:
				joyAction[0] = 0.0 #YAW #lh
				joyAction[1] = 0.0 #Z  #lv
				joyAction[2] = 0.0 #x #rh
				joyAction[3] =float(random.sample([-1,1],1)[0]) #y #rv
		'''
		goal = wall_follower.msg.agentGoal(action= joyAction)
		#print goal
		action_client.send_goal(goal,done_cb= done)
		action_client.wait_for_result()
	
	print "---------- DONE ----------"
	print record
	print "=================="
	print "                  "
	'''
	trainingX = []
	targetX = []
	for elements in record:
		trainingX.append(elements[0])
		targetX.append( elements[1] )


	DX , tX = np.array( trainingX ), np.array( targetX )
	gp_obj.update_gp(record)
	'''
	#gp_obj.update_gp(record)
	'''
	output = open('training_set', 'w')
	output.write(str(record))
	output.flush()
	output.close()
	'''
	timestr = time.strftime("%Y%m%d-%H%M%S")
	with open(timestr, 'wb') as fp:
		pickle.dump(record, fp)
	fp.close()

def done(returnCode,result): 
	global record  
	global counter
	rawLaserDataList = []
	if returnCode == 3:
		print "Successful"
		rawLaserDataList = list(result.state)
		for index, value in enumerate(rawLaserDataList):
			if value == float('inf'):
				rawLaserDataList[index] = 9999
			#	value = 9999
		
		print result.reward
		print min(rawLaserDataList)
		print counter
		record.append([rawLaserDataList, result.reward])
		counter = counter + 1 
if __name__ == '__main__':
    try:
        rospy.init_node('agent', anonymous=True)
        agent_client()
        #rospy.spin()
    except rospy.ROSInterruptException:
        print "program interrupted before completion"