#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan

rewardSum = 0

def callback(data):
    global rewardSum
    #print data.ranges
    if any((value < 2 and value > 1) for value in data.ranges):
        print "TOO CLOSE TO THE WALL"
        rewardSum += -1
    #print rewardSum    
    if min(data.ranges) < 2 and min(data.ranges) > 1:
        print min(data.ranges)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/laser/scan", LaserScan, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
