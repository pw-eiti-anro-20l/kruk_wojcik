#!/usr/bin/python
import rospy
from lab4.srv import oint

def init ():
    rospy.wait_for_service ('oint_service')
    try:
        inter = rospy.ServiceProxy ('oint_service', oint)
        response = inter (0, 0, 0, 0, 0, 0, 1, 0.1, 'linear')
        return response
    except rospy.ServiceException, e:
        print "sSrvice failed"

if __name__ == "__main__":
    print ("setting up...")
    init ()
    print ("rviz set up")
