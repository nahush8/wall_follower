#!/usr/bin/python

import rospy
import time
import random
import math
import std_msgs.msg
import matplotlib.pyplot as plt
import actionlib
import matplotlib.pyplot as plt
import wall_follower.msg
import mavros
#import update_transition_class
from mavros.utils import *
from mavros_msgs.msg import State
from mavros_msgs.srv import SetMode, StreamRate, StreamRateRequest, CommandBool, CommandTOL
from geometry_msgs.msg import *
from sensor_msgs.msg import Joy, LaserScan


def agent_client():
	joyAction = [0,0,0,0]
	action_client = actionlib.SimpleActionClient('perception',wall_follower.msg.agentAction)
	action_client.wait_for_server()
	print "Connected"

	while not rospy.is_shutdown():
		joy = rospy.wait_for_message("joy",Joy)

		joyAction[0] = joy.axes[0] #YAW #lh
		joyAction[1] = joy.axes[1] #Z  #lv
		joyAction[2] = joy.axes[2] #x #rh
		joyAction[3] = joy.axes[3] #y #rv

		goal = wall_follower.msg.agentGoal(action= joyAction)
		#print goal
		action_client.send_goal(goal,done_cb= done)
		action_client.wait_for_result()


def done(returnCode,result):  
	if returnCode == 3:
		print "Successful"
		print result.reward
		print result.state

if __name__ == '__main__':
    try:
        rospy.init_node('agent', anonymous=True)
        agent_client()
        rospy.spin()
    except rospy.ROSInterruptException:
        print "program interrupted before completion"