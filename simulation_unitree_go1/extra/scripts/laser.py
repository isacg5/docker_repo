#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
import sensor_msgs.msg
import math

pub = rospy.Publisher('/scan', LaserScan, queue_size = 10)
scan = LaserScan()

def laser_cb(msg):
    #desired_angle = 90.0
    desired_angle = 180.0

    desired_angle_rad = desired_angle * (math.pi / 180.0)


    angle_min = msg.angle_min
    angle_max = msg.angle_max


   # start_index = len(msg.ranges) // 2 - 100
    start_index = len(msg.ranges) // 2 - 200


    middle_values = msg.ranges[start_index:start_index + 400]
    intensit = msg.intensities[start_index:start_index + 400]

    
    current_time = rospy.Time.now()
    scan.header.stamp = current_time
    scan.header.frame_id = msg.header.frame_id
    # scan.angle_min = -0.785398
    # scan.angle_max = 0.785398
    scan.angle_min = -math.pi/2
    scan.angle_max = math.pi/2

    scan.angle_increment = msg.angle_increment
    scan.time_increment = 4.99999987369e-05
    scan.range_min = 0.00999999977648
    scan.range_max = 32.0
    scan.ranges = middle_values
    scan.intensities = intensit

    pub.publish(scan)

def listener():
    rospy.init_node('revised_scan', anonymous=True)
    sub = rospy.Subscriber('/full_scan', LaserScan, laser_cb)
    rospy.spin()

if __name__ == '__main__':
    listener()
