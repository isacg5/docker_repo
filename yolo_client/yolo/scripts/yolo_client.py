#!/usr/bin/env python2

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import requests
import cv2
import numpy as np

counter = 0

rospy.init_node('yolo_client')

# Create a CvBridge
bridge = CvBridge()

# Initialize the variable to store the latest image
latest_image = None

# ROS Publisher for recognized classes
recognized_class_pub = rospy.Publisher('/recognized_class', String, queue_size=10)

def image_callback(msg):
    global latest_image
    global counter 
    
    counter = counter + 1

    if counter > 10:
        counter = 0

    #   try:
        # Convert ROS Image message to OpenCV format
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Encode the image to JPEG format for transmission
        _, img_encoded = cv2.imencode('.jpg', cv_image)

        # Send the image to the Flask API using HTTP POST request
        url = "http://192.168.12.70:5001/process_image"
        headers = {'Content-Type': 'image/jpeg'}
        response = requests.post(url, data=img_encoded.tostring(), headers=headers)

        # Extract the list of detected classes from the API response
        detected_classes = response.json().get('detected_classes', [])

        # Publish each detected class to the ROS topic
        for detection in detected_classes:

            #Extract the class label
            detected_class = detection.get('class', '')
        
            if detected_class:
                if detected_class == "tennis racket":
                    detected_class = "paddel racket"
                        
                #rospy.loginfo(f"Detected Class: {detected_class}")
                rospy.loginfo("detected Class: {}".format(detected_class))
                # Publish the detected class to the "/recognized_class" topic
                recognized_class_pub.publish(String(detected_class))

#    except Exception as e:
#        rospy.logerr(f"Error processing image: {str(e)}")

# Subscribe to the image topic
image_topic = "/camera/color/image_raw"  # Replace with your actual image topic
rospy.Subscriber(image_topic, Image, image_callback)

# Keep the node running
rospy.spin()
