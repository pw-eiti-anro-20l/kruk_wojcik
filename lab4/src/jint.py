#!/usr/bin/python
import math
import rospy

from set_robot_position import new_path
from interpolation import interpolate

from lab4.srv import jint

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header
from nav_msgs.msg import Path

bounds = {
    "i1": [-1, 0],             
    "i2": [-1, 0],             
    "i3": [-1, 0],
}

def inBounds (req):
    global bounds
    if req.base_link_link1 < bounds ['i1'] [0]:
        return False
    elif req.base_link_link1 > bounds ['i1'] [1]:
        return False
    elif req.link1_link2 < bounds ['i2'] [0]: 
        return False
    elif req.link1_link2 > bounds ['i2'] [1]:
        return False
    elif req.link2_link3 < bounds ['i3'] [0]:
        return False
    elif req.link2_link3 > bounds ['i3'] [1]:
        return False
    return True

def joint_state_constructor ():
    js = JointState()
    js.name = ['base_link_link1', 'link1_link2', 'link2_link3']
    js.header = Header()
    js.header.stamp = rospy.Time.now()
    return js 

path = Path ()
def mainLoop (req):
    req_p = [req.base_link_link1, req.link1_link2, req.link2_link3]
    prev_p = rospy.wait_for_message (
            'joint_states', JointState, timeout = 10).position

    cur_time = float (0)
    frq = 100
    rate = rospy.Rate (frq)

    for x in range (int (frq * req.time)):
        poses = []
        for i in range (0, 3):
            poses.append (interpolate (
                prev_p [i], req_p [i], cur_time, req.time, req.type))
            
        js = joint_state_constructor ()
        js.position = poses
        pub.publish (js)
        pub_path.publish (new_path (js, path))

        cur_time += float (1) / frq
        rate.sleep ()

def handler (req):
    if not inBounds (req):
        return False
    mainLoop (req)
    return True

def main ():
    rospy.init_node ('jint_node', anonymous = False)
    s = rospy.Service ('jint_control_srv', jint, handler)
    rospy.spin ()

if __name__ == "__main__":
    pub = rospy.Publisher ('int', JointState, queue_size = 10)
    pub_path = rospy.Publisher ('pathJint', Path, queue_size = 10)
    main ()
