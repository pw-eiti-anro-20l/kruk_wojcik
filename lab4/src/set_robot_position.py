import rospy

from PyKDL import *
from tf.transformations import *
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path

dh_data = {
    "i1": [0, 1, 0, 0],
    "i2": [0, 1, 1.57, 1.57],
    "i3": [0, 1, 1.57, 1.57]
}  

def createChain ():
    chain = Chain ()
    f = Frame ()
    d, theta = None, None

    for i in dh_data:
        prev_d, prev_theta = d, theta
        a, d, alpha, theta = dh_data [i]
        if not i == "i1":
            cur_frame = f.DH (a, alpha, prev_d, prev_theta)
            segment = Segment (Joint (Joint.TransZ), cur_frame)
            chain.addSegment (segment)

    chain.addSegment (Segment (Joint (Joint.TransZ), f.DH (0, 0, d, theta)))
    return chain

def calculate_cartesian (data, chain):
    solver = ChainFkSolverPos_recursive (chain)
    
    jnts = JntArray (chain.getNrOfJoints ())
    for i in range (0, 3):
        jnts [i] = data.position [i]
    
    cartesian = Frame () 
    solver.JntToCart (jnts, cartesian)
    return cartesian

def create_PoseStamped (cartesian):
    pose_stamped = PoseStamped ()
    pose_stamped.header.frame_id = 'base_link'
    pose_stamped.header.stamp = rospy.Time.now ()

    pose_stamped.pose.position.x = cartesian.p [0]
    pose_stamped.pose.position.y = cartesian.p [1]
    pose_stamped.pose.position.z = cartesian.p [2]

    quats = cartesian.M.GetQuaternion ()

    pose_stamped.pose.orientation.x = quats [0]
    pose_stamped.pose.orientation.y = quats [1]
    pose_stamped.pose.orientation.z = quats [2]
    pose_stamped.pose.orientation.w = quats [3]

    return pose_stamped

def new_path (data, path):
    chain = createChain ()
    result = calculate_cartesian (data, chain) 

    pose_stamped = create_PoseStamped (result)
    path.header = pose_stamped.header
    path.poses.append (pose_stamped)
    return path

