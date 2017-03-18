#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan

rewardSum = 0

def callback(data):
    global rewardSum
    listRange = []
    for i in range(0,360):
		listRange.append(round(data.ranges[i],2))
    #rospy.loginfo(rospy.get_caller_id() + "%s\n\n\n\n\n", listRange)
    if any(value < 2 and value > 1 for value in listRange):
        print "TOO CLOSE TO THE WALL"
        rewardSum += -1
    print rewardSum    
    
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
