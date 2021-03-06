#!/usr/bin/env python

"""Extract images from a rosbag.
"""

import os,sys
import argparse
import cv2
import rosbag 
import csv
import string
from std_msgs.msg import Int32, String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge



def main():
    
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("x", help="Input experiment number")
    args = parser.parse_args()
    
    newpath = ((r'/home/labpc/f1tenth_sim/src/f1tenth_control/results/images_bagfile/bagfile_%s') % (args.x)) 
    if not os.path.exists(newpath): os.makedirs(newpath)
 
    camera1path = ((r'/home/labpc/f1tenth_sim/src/f1tenth_control/results/images_bagfile/bagfile_%s/camera1_images') % (args.x)) 
    if not os.path.exists(camera1path): os.makedirs(camera1path)
    camera2path = ((r'/home/labpc/f1tenth_sim/src/f1tenth_control/results/images_bagfile/bagfile_%s/camera2_images') % (args.x)) 
    if not os.path.exists(camera2path): os.makedirs(camera2path)
    camera3path = ((r'/home/labpc/f1tenth_sim/src/f1tenth_control/results/images_bagfile/bagfile_%s/camera3_images') % (args.x)) 
    if not os.path.exists(camera3path): os.makedirs(camera3path)
    camera4path = ((r'/home/labpc/f1tenth_sim/src/f1tenth_control/results/images_bagfile/bagfile_%s/camera4_images') % (args.x)) 
    if not os.path.exists(camera4path): os.makedirs(camera4path)
    
    bag_file = '/home/labpc/f1tenth_sim/src/f1tenth_control/results/bagfiles/cameras_and_steering_ang.bag'
    image_topic1 = '/camera1/rgb/image_raw'
    image_topic2 = '/camera2/rgb/image_raw'
    image_topic3 = '/camera3/rgb/image_raw'
    image_topic4 = '/camera4/rgb/image_raw' 
    ackermann_topic = '/ackermann_cmd'

    bag = rosbag.Bag(bag_file, "r")
    bridge = CvBridge()
    count = 0

    for topic, msg, t in bag.read_messages(topics=[image_topic1]):
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        cv2.imwrite(os.path.join(camera1path, "frame%06i.png" % count), cv_img)     
        print "Wrote image %i" % count
        count += 1
    
    count = 0
    for topic, msg, t in bag.read_messages(topics=[image_topic2]):  
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        cv2.imwrite(os.path.join(camera2path, "frame%06i.png" % count), cv_img)
        print "Wrote image %i" % count
        count += 1

    count = 0
    for topic, msg, t in bag.read_messages(topics=[image_topic3]):
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        cv2.imwrite(os.path.join(camera3path, "frame%06i.png" % count), cv_img)
        print "Wrote image %i" % count
        count += 1

    count = 0
    for topic, msg, t in bag.read_messages(topics=[image_topic4]):
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        cv2.imwrite(os.path.join(camera4path, "frame%06i.png" % count), cv_img)
        print "Wrote image %i" % count
        count += 1
        print t

    filename = (newpath + '/steering_ang_%s.csv') % (args.x)
    with open(filename, 'w+') as csvfile:
			filewriter = csv.writer(csvfile, delimiter = ',')
			firstIteration = True	#allows header row
			for topic, msg, t in bag.read_messages(topics=[ackermann_topic]):	# for each instant in time that has data for topicName
				#parse data from this instant, which is of the form of multiple lines of "Name: value\n"
				#	- put it in the form of a list of 2-element lists
				msgString = str(msg)
				msgList = string.split(msgString, '\n')
				instantaneousListOfData = []
				for nameValuePair in msgList:
					splitPair = string.split(nameValuePair, ':')
					for i in range(len(splitPair)):	#should be 0 to 1
						splitPair[i] = string.strip(splitPair[i])
					instantaneousListOfData.append(splitPair)
				#write the first row from the first element of each pair
				if firstIteration:	# header
					headers = ["rosbagTimestamp"]	#first column header
					for pair in instantaneousListOfData:
						headers.append(pair[0])
					filewriter.writerow(headers)
					firstIteration = False
				# write the value from each pair to the file
				values = [str(t)]	#first column will have rosbag timestamp
				for pair in instantaneousListOfData:
					if len(pair) > 1:
						values.append(pair[1])
				filewriter.writerow(values)

    bag.close()

    return

if __name__ == '__main__':
    main()
