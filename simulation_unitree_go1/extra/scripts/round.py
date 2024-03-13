#! /usr/bin/env python2

import rospy
from geometry_msgs.msg import Point, Twist
import time
from extra.srv import Stop  

class TurnNode(object):
    def __init__(self):
        rospy.Service('explore_stop_service', Stop, self.handle_stop_restart)
        self.paused = True
        self.vel_msg = Twist()
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    def handle_stop_restart(self, req):
        if req.stop == True:
            rospy.loginfo("Restarting the node...")
            self.paused = False

        if req.stop == False:
            rospy.loginfo("Stopping the node...")
            self.paused = True


        return True

    # Rotation state function that keeps rotating with a constant velocity
    def rotation_state(self):
        self.vel_msg.angular.z = 0.5
        print("TURNIIIIIIIIIIIIIIIIIIIIIIIIIIIINNNNNNNNNNNNNNNNNNNNNNNGGGGGGGGGGG")
        self.pub.publish(self.vel_msg)

    def run(self):
        rate = rospy.Rate(10)  

        while not rospy.is_shutdown():
            if not self.paused:
                self.rotation_state()

            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('Turning_node')
    hello_node = TurnNode()
    hello_node.run()

