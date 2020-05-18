#!/usr/bin/python

import rospy
from interpolation import interpolate 
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from lab4.srv import oint

def createPoseStamped (data):
    ps = PoseStamped ()
    ps.pose.position.x = data [0]
    ps.pose.position.y = data [1]
    ps.pose.position.z = data [2]
    ps.pose.orientation.x = data [3]
    ps.pose.orientation.y = data [4]
    ps.pose.orientation.z = data [5]
    ps.pose.orientation.w = data [6]
    ps.header.stamp = rospy.Time.now ()
    ps.header.frame_id = 'base_link'
    return ps

def createPath (pose_stamped):
    path.header = pose_stamped.header
    path.poses.append (pose_stamped)
    return path


prev_p = [0, 0, 0, 0, 0, 0, 1]
def moveLoop (req):
    global prev_p
    frq = 30
    rate = rospy.Rate (frq)
    cur_time = 0
    new_p = [req.x, req.y, req.z, req.qx, req.qy, req.qz, req.qw]

    for i in range (int (frq * req.time)):
        cur_p = []
        for j in range (0, 7):
            cur_p.append (interpolate (
                prev_p [j], new_p [j], cur_time, req.time, req.type))
    
        ps = createPoseStamped (cur_p)
        pose_pub.publish (ps)   
        path_pub.publish (createPath (ps))

        cur_time += float (1) / frq
        rate.sleep ()
    prev_p = new_p

def properTime (time):
    if time > 0:
        return True
    return False
    
def handler (req):
    if not properTime (req.time):
        return False
    moveLoop (req)
    return True

def main ():
    rospy.init_node ('oint_node', anonymous = False)
    s = rospy.Service ('oint_control_srv', oint, handler) 
    rospy.spin ()

if __name__ == '__main__':
    pose_pub = rospy.Publisher ('poseOint', PoseStamped, queue_size = 10)
    path_pub = rospy.Publisher ('pathOint', Path, queue_size = 10)
    path = Path ()
    main ()
