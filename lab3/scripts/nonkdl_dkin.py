#! /usr/bin/python

import rospy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped 
from tf.transformations import *
    
dh_data = {
    "i1": [0, 1, 0, 0],
    "i2": [0, 1, 1.57, 1.57],
    "i3": [0, 1, 1.57, 1.57]
}  

bounds = {
    "i1": [-0.3, 0],             
    "i2": [-1, 0],             
    "i3": [-1, 0],             
}

def trans_matrix (data):
    matrix = translation_matrix((0, 0, 0));
    j = 0
    for i in dh_data:
        a, d, al, th = dh_data [i]

        trans_z = translation_matrix ((0, 0, d * (1 + data.position[j])))
        rot_z = rotation_matrix (th, (0, 0, 1))
        trans_x = translation_matrix ((a, 0, 0))
        rot_x = rotation_matrix (al, (1, 0, 0))

        mat = concatenate_matrices(trans_x, rot_x, rot_z, trans_z)
        matrix = concatenate_matrices(matrix, mat)
        j += 1
    return matrix

def response_PoseStamped (matrix, data):
    pose_stamped = PoseStamped()

    axis_translation = translation_from_matrix (matrix)

    pose_stamped.header.frame_id = "base_link"
    pose_stamped.header.stamp = data.header.stamp
    pose_stamped.pose.position.x = axis_translation [0]
    pose_stamped.pose.position.y = axis_translation [1]
    pose_stamped.pose.position.z = axis_translation [2]
    
    quaternions = quaternion_from_matrix (matrix)

    pose_stamped.pose.orientation.x = quaternions [0]
    pose_stamped.pose.orientation.y = quaternions [1]
    pose_stamped.pose.orientation.z = quaternions [2]
    pose_stamped.pose.orientation.w = quaternions [3]
    return pose_stamped

def inBounds (data):
    j = 0
    for bound in bounds:
        if bounds [bound][0] > data.position [j] or bounds [bound][1] < data.position [j]:
            return False
    return True

def callback (data):
    if not inBounds (data):
        rospy.logerr ("you cant go there :(")
        return

    matrix = trans_matrix (data)
    my_pose = response_PoseStamped (matrix, data)
    publisher = rospy.Publisher('nonkdl_dkin_msgs', PoseStamped, queue_size=10)
    publisher.publish (my_pose)

if __name__ == '__main__':
    rospy.init_node('NONKDL_DKIN', anonymous = False)
    rospy.Subscriber("joint_states", JointState , callback)
    rospy.spin()
