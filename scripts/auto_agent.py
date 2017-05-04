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
training_record = []
gp_obj = gp.update_gp_class()
np.random.seed(1)
counter = 0
current_state = [8,8,8,8,8,8,8,8]
new_state = [8,8,8,8,8,8,8,8]
action = [0,0,0]

def agent_client():
	global record
	global counter
	global current_state
	global new_state
	joyAction = [0,0,0,0]
	action_client = actionlib.SimpleActionClient('perception',wall_follower.msg.agentAction)
	action_client.wait_for_server()
	print "Connected"

	#while not rospy.is_shutdown():
	while counter < 10:
		
		joy = rospy.wait_for_message("joy",Joy)
		if joy.axes[0] != 0 or joy.axes[1] != 0 or joy.axes[2] != 0 or joy.axes[3] != 0:
			joyAction[0] = joy.axes[0] #YAW #lh

			joyAction[1] = joy.axes[1] #Z  #lv
			joyAction[2] = joy.axes[2] #x #rh
			joyAction[3] = joy.axes[3]#y #rv
			
		else:
			joyAction[0] = 0.0 #YAW #lh
			joyAction[1] = float(random.uniform(-0.1,0.1)) #Z  #lv
			joyAction[2] = float(random.uniform(-0.1,0.1)) #x #rh
			joyAction[3] = float(random.uniform(-0.1,0.1)) #y #rv

		action[0] = joyAction[2]
		action[1] = joyAction[3]
		action[2] = joyAction[1]

		current_state = rospy.wait_for_message("laser/scan",LaserScan)
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
	global current_state
	global new_state
	global action

	rawLaserDataList = []
	if returnCode == 3:
		print "Successful"
		rawLaserDataList = list(result.state)
		for index, value in enumerate(rawLaserDataList):
			if value == float('inf'):
				rawLaserDataList[index] = 8
			#	value = 9999
		new_state = rawLaserDataList
		print result.reward
		print min(rawLaserDataList)
		print counter		
		record.append([current_state,action,result.reward, new_state])
		counter = counter + 1 
if __name__ == '__main__':
    try:
        rospy.init_node('agent', anonymous=True)
        agent_client()
        #rospy.spin()
    except rospy.ROSInterruptException:
