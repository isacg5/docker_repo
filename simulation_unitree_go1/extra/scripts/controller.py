#!/usr/bin/env python2
import sys
import rospy
from extra.srv import Stop
import time 
from geometry_msgs.msg import *
from nav_msgs.msg import Odometry
import math

class ControllerNode(object):
    def __init__(self):
        self.position = Point()
        self.last_position = Point()
        self.distance = 0
        self.threshold = 2
               
    def odomCb(self, msg):
        self.position = msg.pose.pose.position
#        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB", self.position)

    def get_distance(self):
        self.distance = math.sqrt((self.position.x - self.last_position.x)**2 + (self.position.y - self.last_position.y)**2)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", self.distance)

    def controller(self):
        rospy.wait_for_service('explore_stop_service')
        while True:
            stop_restart_n = rospy.ServiceProxy('explore_stop_service', Stop)
            resp1 = stop_restart_n(False)
            time.sleep(30)
            self.get_distance()
            if(self.distance > self.threshold): 
                self.last_position = self.position
                resp1 = stop_restart_n(True)
                time.sleep(15)
        return resp1.success


if __name__ == "__main__":
    rospy.init_node('Controller_node')
    contr = ControllerNode()
    rospy.Subscriber('odometry/imu', Odometry ,contr.odomCb)
    contr.controller()
