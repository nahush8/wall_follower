#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy


def callback(data):
    '''
	listRange = []
	for i in range(0,360):
		listRange.append(round(data.ranges[i],2))
	rospy.loginfo(rospy.get_caller_id() + "%s\n\n\n\n\n", listRange)
    '''
    print "------------"
    print data.axes[0]
    print "\n"
    print data.axes[3]
    print "\n"
    print "------------"

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('joy_listener', anonymous=True)

    #rospy.Subscriber("/joy", Joy, callback)
    joy = rospy.wait_for_message("joy",Joy)
    print "------------"
    print joy.axes[0]
    print "\n"
    print joy.axes[3]
    print "\n"
    print "------------"
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

if __name__ == '__main__':
    while True:
        listener()
