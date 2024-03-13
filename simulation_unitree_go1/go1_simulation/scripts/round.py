#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Point, Twist
from assignment1_EXP.msg import Marker
import time

IMG_WIDTH = 800
IMG_HEIGHT = 800
EXTRA_RANGE = 20
LIMIT_DISTANCE = 200

# Velocity for real robot: 0.1

class RobotController():
    def __init__(self):
        self.vel_msg = Twist()
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)


    # Rotation state function that keeps rotating with a constant velocity
    def rotation_state(self):
        self.vel_msg.angular.z = 1
        self.pub.publish(self.vel_msg)
        time.sleep(5)
        self.vel_msg.angular.z = 0
        self.pub.publish(self.vel_msg)


    
if __name__ == "__main__":
    time.sleep(2)

    rospy.init_node('Controller_node')

    robot_controller = RobotController()
 
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        robot_controller.planning()
        rate.sleep()
