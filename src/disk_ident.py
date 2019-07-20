#!/usr/bin/env python

import rospy
from array import *
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Bool
from std_msgs.msg import Int8MultiArray, ByteMultiArray, Float64MultiArray
from artiesans.msg import gamePositions
#from face_rec.msg import gamePositions
from baxter_core_msgs.msg import DigitalIOState
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import time
import imutils

# publishes the positions of the disks
publisher = rospy.Publisher('board', gamePositions)
#diskPosPub = rospy.Publisher('/artisans/disk_positions', Int8MultiArray)
#diskPresentPub = rospy.Publisher('/artisans/disk_present', ByteMultiArray)

sizes = {
    'Blue': 5,
    'Green': 4,
    'Yellow': 3,
    'Orange': 2,
    'Pink': 1
}

#callback function for camera subscriber, called by the camera subscriber for every frame.
def callback(data):
    
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    cv2.imshow("Hand Camera Feed", cv_image)
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    detect_disks(hsv, cv_image);
    cv2.waitKey(1) # needed for cv2.imshow to take effect. REMOVE otherwise

def detect_disks(hsv, cv_image):
		

	#Board Night
	#boardLower = (0, 55, 35)
	#boardUpper = (31, 80, 255)

	#Board Day
	boardLower = (0, 44, 60)
	boardUpper = (26, 101, 101)

	#LightGreen
	#lightgreenLower = (29, 86, 6)
	#lightgreenUpper = (64, 255, 255)

        #Skl Green
	lightgreenLower = (30, 45, 21)
	lightgreenUpper = (70, 148, 170)

	#DarkBlue
	#darkblueLower = (83, 51, 31)
	#darkblueUpper = (116, 255, 255)

        #Blue SKL
	darkblueLower = (74, 75, 20)
	darkblueUpper = (139, 113, 170)

	#LightBlue Night
	#lightblueLower = (83, 70, 37)
	#lightblueUpper = (105, 145, 119)

	#Orange
	#orangeLower = (0, 141, 32)
	#orangeUpper = (16, 255, 255)

        #Orange Night
	orangeLower = (1, 128, 33)
	orangeUpper = (19, 168, 106)

	#Yellow
	#yellowLower = (13, 119, 59)
	#yellowUpper = (34, 255, 255)

        #Yellow SKL
	yellowLower = (21, 113, 47)
	yellowUpper = (30, 255, 255)

	#Pink
	pinkLower = (155, 98, 37)
	pinkUpper = (179, 255, 255)

	colors = ["Board", "Green", "Blue", "Orange", "Yellow", "Pink"]
	
        frame = cv_image
		
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)


	masks = []

	maskBoard = cv2.inRange(hsv, boardLower, boardUpper)
    	maskBoard = cv2.erode(maskBoard, None, iterations=2)
    	maskBoard = cv2.dilate(maskBoard, None, iterations=2)
	masks.append(maskBoard)

	maskLGreen = cv2.inRange(hsv, lightgreenLower,lightgreenUpper)
	maskLGreen = cv2.erode(maskLGreen, None, iterations=2)
	maskLGreen = cv2.dilate(maskLGreen, None, iterations=2)        
	masks.append(maskLGreen)

	maskDBlue = cv2.inRange(hsv, darkblueLower, darkblueUpper)
	maskDBlue = cv2.erode(maskDBlue, None, iterations=2)
	maskDBlue = cv2.dilate(maskDBlue, None, iterations=2)
	masks.append(maskDBlue)

	maskOrange = cv2.inRange(hsv, orangeLower, orangeUpper)
	maskOrange = cv2.erode(maskOrange, None, iterations=2)
	maskOrange = cv2.dilate(maskOrange, None, iterations=2)
	masks.append(maskOrange)

	maskYellow = cv2.inRange(hsv, yellowLower, yellowUpper)
	maskYellow = cv2.erode(maskYellow, None, iterations=2)
	maskYellow = cv2.dilate(maskYellow, None, iterations=2)
	masks.append(maskYellow)

	maskPink = cv2.inRange(hsv, pinkLower, pinkUpper)
	maskPink = cv2.erode(maskPink, None, iterations=2)
	maskPink = cv2.dilate(maskPink, None, iterations=2)
	masks.append(maskPink)
	        
        index = 0
	pos = np.array(([0, 0, 0, False], [0, 0, 0, False], [0, 0, 0, False], [0, 0, 0, False], [0, 0, 0, False], [0, 0, 0,  False]),dtype=object)        
	for mask in masks:
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)		
		pos[index][0] = colors[index]
		pos[index][1] = cnts                
                index += 1      		
	
	center = None        
	centers = []

	xs = [160, 310, 430]

	cv2.rectangle(frame, (xs[0] - 60, 110), (xs[0] + 60, 290), (255, 255, 255))
	cv2.rectangle(frame, (xs[1] - 60, 110), (xs[1] + 60, 290), (255, 255, 255))
	cv2.rectangle(frame, (xs[2] - 60, 110), (xs[2] + 60, 290), (255, 255, 255))
	
        for i in range(6):
		cnt = pos[i][1]
		
		if 1 <= len(cnt) < 7:
		    #area = cv2.contourArea(cnt)
		    c = max(cnt, key=cv2.contourArea)
		    rect = cv2.minAreaRect(c)
		    M = cv2.moments(c)
		    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		    centers.append(center)
		    pos[i][2] = center
		    if(center != 0):
			pos[i][3] = True	       
		    box = cv2.cv.BoxPoints(rect)
		    box = np.int0(box)
		    cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
		    ((x, y), radius) = cv2.minEnclosingCircle(c)

		    if 10 < radius < 60:			
		        cv2.circle(frame, center, 5, (255, 255, 255), -1)
                print(pos[i][0])
		print(pos[i][2])
		print(pos[i][3])
		print("-----------------")
		
		

		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		positions = []
		ready = True
		for i in range (6):			
			if(pos[i][3] == False):
				ready = False		


        
	coord = [['Green'], ['Blue'], ['Orange'], ['Yellow'], ['Pink']]
	for i in range (1,6):
		coord[i-1].append(pos[i][2])
    	def sortKey(obj):
		ans = 0
		if(obj[1] != 0):
		    ans = obj[1][0]
		return ans
	coord.sort(key=sortKey)

	ans = gamePositions()

	
	poles = [[], [], []]

	index = 0
	while(index < len(coord) and coord[index][1] == 0): index += 1
	for n in range(3):

		while(index < len(coord) and abs(coord[index][1][0] - xs[n]) < 60):
		    poles[n].append(coord[index])
		    index += 1

	def sortKey2(obj):
		ans = 1000000000000000
		if(obj[1] != 0):
		    ans = obj[1][1]
		return ans
    	poles[0].sort(reverse=True, key=sortKey2)
	poles[1].sort(reverse=True, key=sortKey2)
	poles[2].sort(reverse=True, key=sortKey2)

	print(poles)
    
    
	ans.ready = ready
	ans.first = []
	for n in poles[0]:
		ans.first.append(sizes[n[0]])

	ans.second = []
	for n in poles[1]:
		ans.second.append(sizes[n[0]])

	ans.third = []
	for n in poles[2]:
		ans.third.append(sizes[n[0]])

	print(ans)

	publisher.publish(ans)

       
if __name__ == '__main__':
    rospy.init_node('disksIdentification', anonymous=True)

#create subscriber to the right hand camera, each frame recieved calls the callback function
camera_sub = rospy.Subscriber("/cameras/right_hand_camera/image",Image,callback)

#prevents program from exiting, allowing subscribers and publishers to keep operating
#in our case that is the camera subscriber and the image processing callback function
rospy.spin()


