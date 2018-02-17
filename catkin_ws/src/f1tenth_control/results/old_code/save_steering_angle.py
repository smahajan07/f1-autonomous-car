#!/usr/bin/env python

"""Extract images from a rosbag.
"""
import rospy
import os,sys
import argparse
import cv2
import rosbag 
import csv
import string
from std_msgs.msg import Int32, String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ackermann_msgs.msg import AckermannDriveStamped
    
def main():
    
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("x", help="Input trial number")
    args = parser.parse_args()
    
    global filename, filewriter, firstIteration


    newpath = ((r'/home/labpc/f1tenth_sim/src/f1tenth_control/results/images/trial_%s') % (args.x))
    filename = (newpath + '/steering_angle_data_%s.csv' % (args.x))

    with open(filename, 'w+') as csvfile:
	filewriter = csv.writer(csvfile, delimiter = ',')
	firstIteration = True	#allows header row

    rospy.init_node('ackermann_listener')

    while True:
	    #rospy.Subscriber('/ackermann_cmd', AckermannDriveStamped, ackermann_callback,queue_size=1)
	msg = rospy.wait_for_message('/ackermann_cmd',AckermannDriveStamped)
	with open(filename, 'a') as csvfile:
	   	filewriter = csv.writer(csvfile, delimiter = ',')
		msgString = str(msg)
		msgList = string.split(msgString, '\n')
		instantaneousListOfData = []
		for nameValuePair in msgList:
			splitPair = string.split(nameValuePair, ':')
		        for i in range(len(splitPair)):	#should be 0 to 1
				splitPair[i] = string.strip(splitPair[i])
			instantaneousListOfData.append(splitPair)
		onlySteeringAngle = instantaneousListOfData[7:8]
		#filewriter.writerow(onlySteeringAngle)
		#write the first row from the first element of each pair
		if firstIteration:	# header
			headers = ["rosbagTimestamp"]	#first column header
			for pair in onlySteeringAngle:
				headers.append(pair[0])
			filewriter.writerow(headers)
			firstIteration = False
		# write the value from each pair to the file
		t = rospy.Time.now()
		values = [str(t)]	#first column will have rosbag timestamp
		for pair in onlySteeringAngle:
			if len(pair) > 1:
				values.append(pair[1])
		filewriter.writerow(values)        
        rospy.sleep(2)

    # Spin until ctrl + c
    rospy.spin()

'''def ackermann_callback(msg):
    global filewriter, firstIteration
    with open(filename, 'a') as csvfile:
   	filewriter = csv.writer(csvfile, delimiter = ',')
        msgString = str(msg)
	msgList = string.split(msgString, '\n')
        instantaneousListOfData = []
        for nameValuePair in msgList:
		splitPair = string.split(nameValuePair, ':')
                for i in range(len(splitPair)):	#should be 0 to 1
			splitPair[i] = string.strip(splitPair[i])
		instantaneousListOfData.append(splitPair)
        onlySteeringAngle = instantaneousListOfData[7:8]
        #filewriter.writerow(onlySteeringAngle)
	#write the first row from the first element of each pair
	if firstIteration:	# header
		headers = ["rosbagTimestamp"]	#first column header
		for pair in onlySteeringAngle:
			headers.append(pair[0])
		filewriter.writerow(headers)
		firstIteration = False
	# write the value from each pair to the file
        t = rospy.Time.now()
	values = [str(t)]	#first column will have rosbag timestamp
	for pair in onlySteeringAngle:
		if len(pair) > 1:
			values.append(pair[1])
	filewriter.writerow(values) '''       

if __name__ == '__main__':
    main()

