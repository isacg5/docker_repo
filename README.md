
CONNECT WIFI TO ROBOT
sudo date --set="2024-03-15 10:34:00"

FIRST TERMINAL
ssh unitree@192.168.123.15
sudo date --set="2024-03-14 11:38:00"
cd UnitreeSLAM
export ROS_IP=192.168.123.15
./ERF_Navigation_Challenge1.sh


SECOND TERMINAL
ssh unitree@192.168.123.15
cd UnitreeSLAM
export ROS_IP=192.168.123.15
./ERF_Navigation_Challenge2.sh


THIRD TERMINAL
ssh unitree@192.168.123.15
export ROS_IP=192.168.123.15
roslaunch realsense2_camera rs_camera.launch

FOURTH TERMINAL
ssh unitree@192.168.123.15
export ROS_IP=192.168.123.15
cd Desktop/ERF_LOG/unige_navigation
roslaunch start logger.launch teamName:=unige challengeType:=navigation


FIFTH TERMINAL
cd Desktop/docker_repo/src
python3 map_occupancy.py










export ROS_IP=192.168.12.165
export ROS_MASTER_URI=http://192.168.123.15:11311


roslaunch start logger.launch teamName:=unige challengeType:=navigation

roslaunch realsense2_camera rs_camera.launch
