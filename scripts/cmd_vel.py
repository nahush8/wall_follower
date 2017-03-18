#!/usr/bin/python

import rospy
import mavros
from mavros.utils import *
from mavros_msgs.msg import State
from mavros_msgs.srv import SetMode, StreamRate, StreamRateRequest, CommandBool
from geometry_msgs.msg import *
from sensor_msgs.msg import Joy, LaserScan
import time
from kb_hit import KBHit

def state_cb(state):
    print state

def flight():
    LINEAR_X_MUL_FACTOR = 2
    LINEAR_Y_MUL_FACTOR = 2
    LINEAR_Z_MUL_FACTOR = 1
    ANGULAR_Z_MUL_FACTOR = 1

    key = '\0'
    kb = KBHit()
    # initialize the subscriber node
    rospy.init_node('flight', anonymous=True)
    # subcribe to the mavros State
    #rospy.Subscriber("mavros/state",State,state_cb)
    state = rospy.wait_for_message("mavros/state",State)
    #state_cb(state)
    local_pos_pub = rospy.Publisher("mavros/setpoint_position/local",PoseStamped,queue_size=10)
    local_vel_pub = rospy.Publisher("mavros/setpoint_velocity/cmd_vel",TwistStamped,queue_size=10)

    rospy.wait_for_service("mavros/cmd/arming");
    print " Arming service available"
    try:
        arming_client = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

    rospy.wait_for_service("mavros/set_mode");
    print " SetMode service available"
    try:
        set_mode_client = rospy.ServiceProxy('mavros/set_mode', SetMode)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

    rate = rospy.Rate(20.0)
    while not rospy.is_shutdown() and not state.connected:
        state = rospy.wait_for_message("mavros/state",State)
        rate.sleep()


    pose = PoseStamped()
    vel = TwistStamped()

    last_request = rospy.get_rostime()
    '''
    pose.pose.position.x = 0;
    pose.pose.position.y = 0;
    pose.pose.position.z = 2;

    vel.twist.linear.x = 0
    vel.twist.linear.y = 0
    vel.twist.linear.z = 0.5
    #send a few setpoints before starting
    set_mode_client(0,'OFFBOARD')
    print "******** OFFBOARD ENABLED *****"
    arming_client(True)
    print "****** ARMED ******"
    
    for i in range(0,100):
        #local_pos_pub.publish(pose);
        local_vel_pub.publish(vel)
        time.sleep(0.1)
    vel.twist.linear.z = 0
    '''   
    while not rospy.is_shutdown() :
        state = rospy.wait_for_message("mavros/state",State)
        if state.mode != 'OFFBOARD':
        	set_mode_client(0,'OFFBOARD')
        	print "OFFBOARD ENABLED"

        if not state.armed:
        	arming_client(True)

        joy = rospy.wait_for_message("joy",Joy)

        lh = joy.axes[0] #YAW
        lv = joy.axes[1] #Z  
        rh = joy.axes[2] #x
        rv = joy.axes[3] #y
        
        if lh != 0.0 or lv != 0.0 or rh !=0.0 or rv !=0.0:
            vel.twist.linear.x = rh * LINEAR_X_MUL_FACTOR
            vel.twist.linear.y = -rv * LINEAR_Y_MUL_FACTOR
            vel.twist.linear.z = lv * LINEAR_Z_MUL_FACTOR
            vel.twist.angular.z = lh * ANGULAR_Z_MUL_FACTOR
            local_vel_pub.publish(vel)
            curr_vel_x = vel.twist.linear.x
            curr_vel_y = vel.twist.linear.y
        else:
            '''
            vel.twist.linear.x = 0
            vel.twist.linear.y = 0
            vel.twist.linear.z = 0
            vel.twist.angular.z = 0.001
            local_vel_pub.publish(vel)
            '''
            curr_pose = rospy.wait_for_message("/mavros/local_position/pose" ,PoseStamped)
            local_pos_pub.publish(curr_pose)

        '''
        A basic wall repel control
        '''
        laserData = rospy.wait_for_message("/laser/scan", LaserScan)
        if any(value < 2 and value > 1 for value in laserData.ranges):
            vel.twist.linear.x = -curr_vel_x * 2
            vel.twist.linear.y = -curr_vel_y * 2
            vel.twist.linear.z = lv * LINEAR_Z_MUL_FACTOR
            vel.twist.angular.z = lh * ANGULAR_Z_MUL_FACTOR
            local_vel_pub.publish(vel)
        #print curr_pose

    #rospy.spin()

if __name__ == '__main__':
    try:
        flight()
    except rospy.ROSInterruptException:
        pass
