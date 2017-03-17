#!/usr/bin/python

import rospy
import mavros
from mavros.utils import *
from mavros_msgs.msg import State
from mavros_msgs.srv import SetMode, StreamRate, StreamRateRequest, CommandBool
from geometry_msgs.msg import *
import time
import kb_hit

def state_cb(state):
    print state

def flight():
    key = False
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

    while not rospy.is_shutdown() :
        state = rospy.wait_for_message("mavros/state",State)
        kb = kb_hit.KBHit()
        if state.mode != 'OFFBOARD':
        	set_mode_client(0,'OFFBOARD')
        	print "OFFBOARD ENABLED"

        if not state.armed:
        	arming_client(True)
        	print "ARMED"
        curr_pose = rospy.wait_for_message("/mavros/local_position/pose" ,PoseStamped)  
        if kb.kbhit():
            key = kb.getch()

            if key == 'a':
                vel.twist.linear.x = -1
                vel.twist.linear.y = 0
                vel.twist.linear.z = 0
                vel.twist.angular.z = 0
            elif key == 'd':
                vel.twist.linear.x = 1
                vel.twist.linear.y = 0
                vel.twist.linear.z = 0
                vel.twist.angular.z = 0
            elif key == 'w':
                vel.twist.linear.x = 0
                vel.twist.linear.y = 1
                vel.twist.linear.z = 0
                vel.twist.angular.z = 0
            elif key == 's':
                vel.twist.linear.x = 0
                vel.twist.linear.y = -1
                vel.twist.linear.z = 0
                vel.twist.angular.z = 0
            elif key == 'q':
                vel.twist.linear.x = 0
                vel.twist.linear.y = 0
                vel.twist.linear.z = 1
                vel.twist.angular.z = 0
            elif key == 'e':
                vel.twist.linear.x = 0
                vel.twist.linear.y = 0
                vel.twist.linear.z = -1
                vel.twist.angular.z = 0
            elif key == 'r':
                vel.twist.linear.x = 0
                vel.twist.linear.y = 0
                vel.twist.linear.z = 0
                vel.twist.angular.z = 1
            local_vel_pub.publish(vel)

            kb.set_normal_term()
        else:
            vel.twist.linear.x = 0
            vel.twist.linear.y = 0
            vel.twist.linear.z = 0
            vel.twist.angular.z = 1
            local_vel_pub.publish(vel)
        #print curr_pose

    #rospy.spin()

if __name__ == '__main__':
    try:
        flight()
    except rospy.ROSInterruptException:
        pass
