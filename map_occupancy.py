#! /usr/bin/env python3

import rospy
from nav_msgs.msg import OccupancyGrid
import subprocess
import time 

global process
#global delta 
x_dim = 18 # x dimension of the map 
y_dim = 18 # y dimension of the map

total_grids = 29500

def kill_all():
    subprocess.run(['rosnode', 'kill', '/explore', '/move_base', '/laser_scan_matcher_node', '/Turning_node', '/Controller_node'])
 
def map_cb(msg):
   # global delta
    global process
    
    occupied = msg.data.count(100)
    free = msg.data.count(0)
    
    map_percentage=((free+occupied)/(total_grids))*100
    #print('grids: ', free + occupied)
    
    print(map_percentage)
    if(map_percentage > 80.0):
        kill_all()
        time.sleep(5)
        launch_ros_file()
        #stop
        #launch

def launch_ros_file():
    global process
    try:
        process = subprocess.Popen(['roslaunch', 'go1_simulation', 'slam.launch'])
        time.sleep(2)
        process1 = subprocess.Popen(['rosrun', 'extra', 'controller.py'])
        time.sleep(2)
        process2 = subprocess.Popen(['rosrun', 'extra', 'round.py'])      

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
    map_occupancy()


