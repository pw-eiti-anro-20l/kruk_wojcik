#!/usr/bin/env python

import rospy 
import curses
from geometry_msgs.msg import Twist

def move(direction, keybinds, speed):
    vel_msg = Twist()
    
    if direction == ord (keybinds['go_forward']):
        vel_msg.linear.x = speed
    elif direction == ord (keybinds['go_backward']):
        vel_msg.linear.x = -speed
    elif direction == ord (keybinds['go_left']):
        vel_msg.angular.z = speed 
    elif direction == ord (keybinds['go_right']): 
        vel_msg.angular.z = -speed

    return vel_msg


def printInfo(stdscr, keybinds):
    myStr = ""
    for string in keybinds:
        myStr = myStr + keybinds[string] + ", "

    myStr = "Move with: " + myStr
    stdscr.addstr(myStr)

def main(stdscr):
    keybinds = rospy.get_param('my_robot')
    speed = rospy.get_param('speed')
    printInfo(stdscr, keybinds)
   
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    stdscr.nodelay(0)     
    vel_msg = Twist()
   
    while not rospy.is_shutdown():
        ch = stdscr.getch()
        vel_msg = move (ch, keybinds, speed)
        velocity_publisher.publish(vel_msg)

def init():
    rospy.init_node('my_robot', anonymous=True)
    curses.wrapper(main)

if __name__ == "__main__":
    init ()
