#! /usr/bin/env python3

import rospy
from nav_msgs.msg import OccupancyGrid
import subprocess
import time 
from geometry_msgs.msg import Twist

global process
#global delta 
x_dim = 18 # x dimension of the map 
y_dim = 18 # y dimension of the map

map_percentage = 0
total_grids = 29500

global pub

def kill_all():
    global pub
    msg = Twist()
    msg.linear.x = 0
    msg.linear.y = 0
    msg.linear.z = 0
    msg.angular.x = 0
    msg.angular.y = 0
    msg.angular.z = 0
    pub.publish(msg)
    
    #subprocess.run(['rosnode', 'kill', '/explore', '/move_base', '/laser_scan_matcher_node', '/Turning_node', '/Controller_node'])
    subprocess.run(['killall', 'roslaunch'])
 
def map_cb(msg):
   # global delta
    global process, map_percentage
    
    occupied = msg.data.count(100)
    free = msg.data.count(0)
    
    map_percentage=((free+occupied)/(total_grids))*100
    #print('grids: ', free + occupied)
    
    print(map_percentage)
    if(map_percentage > 200.0):
        map_percentage = 0
        kill_all()
        time.sleep(5)
        print("RESTAAAAAARTTTTTTTT")
        launch_ros_file()
    
        #stop
        #launch

def launch_ros_file():
    global process
    try:
        process = subprocess.Popen(['roslaunch', 'go1_simulation', 'slam.launch'])
        # time.sleep(2)
        # process1 = subprocess.Popen(['rosrun', 'extra', 'controller.py'])
        # time.sleep(2)
        # process2 = subprocess.Popen(['rosrun', 'extra', 'round.py'])      

# messagebox.showinfo("Result", myproc.stdout)
    except OSError as e:
        print(f"Error launching ROS file: {e}")


def map_occupancy():
   # global delta
    
    rospy.init_node('map_check', anonymous=True)
    sub = rospy.Subscriber('/map', OccupancyGrid, map_cb)
   # delta = rospy.get_param("slam_gmapping/delta")
    launch_ros_file()
    rospy.spin()

if __name__ == '__main__':
    global pub 
    pub = rospy.Publisher('cmd_vel', Twist)
    map_occupancy()


