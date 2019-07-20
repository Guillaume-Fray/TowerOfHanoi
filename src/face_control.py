#!/usr/bin/env python

import rospy
import cv2
import random
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import threading


url = {
	'joy'		:	{
		'NE'	:	'src/artiesans/src/white/JoyNEWhite.png',
		'SE'	:	'src/artiesans/src/white/JoySEWhite.png',
		'SW'	:	'src/artiesans/src/white/JoySWWhite.png',
		'blink'	:	'src/artiesans/src/white/JoyBlinkWhite.png'
	},
	'enjoyNE'	:	'JoyNEWhite.jpg',
	'enjoyNE'	:	'JoyNEWhite.jpg',
	'enjoyNE'	:	'JoyNEWhite.jpg',
	'enjoyNE'	:	'JoyNEWhite.jpg',
	'enjoyNE'	:	'JoyNEWhite.jpg',
	'enjoyNE'	:	'JoyNEWhite.jpg',
	'enjoyNE'	:	'JoyNEWhite.jpg',
	'enjoyNE'	:	'JoyNEWhite.jpg',
	'enjoyNE'	:	'JoyNEWhite.jpg',
	'enjoyNE'	:	'JoyNEWhite.jpg',
	'enjoyNE'	:	'JoyNEWhite.jpg',
	'enjoyNE'	:	'JoyNEWhite.jpg',
	'enjoyNE'	:	'JoyNEWhite.jpg'
}

class timer:
    def __init__(self, onDelay, offDelay):
        self.onDelay = onDelay
        self.onDeleayStart = onDelay
        self.offDelay = offDelay
        self.offDelayStart = offDelay
        self.finished = False

    def getVal(self):
        #print(self.onDelay, self.onDeleayStart, self.offDelay, self.offDelayStart)
        self.finished = False
        if(self.onDelay > 0):
            ans = False
            self.onDelay -= 1
            self.offDelay = self.offDelayStart
        else:
            ans = True
            if(self.offDelay > 0):
                self.offDelay = self.offDelay - 1
            else:
                self.onDelay = self.onDeleayStart
                self.finished = True

        return ans

def prog():
	blinkT = timer(500, 17)
	lookT = timer(500, 1)

	dir = ['NE', 'SE', 'SW']
	index = 0

	bridge = CvBridge()
	publisher = rospy.Publisher('/robot/xdisplay', Image)
	while(True):

	
		if(blinkT.finished):
			blinkT = timer(random.randint(320,580), 17)
	
		if(not blinkT.getVal()):
			if(lookT.getVal()):
				index = random.randint(0, len(dir)-1)
				lookT = timer(random.randint(120, 500), 1)
			img = cv2.imread(url['joy'][dir[index]])
		else:
			img = cv2.imread(url['joy']['blink'])
	


		cv2.imshow('image',img)
		
		publisher.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
		
		k = cv2.waitKey(1) & 0xFF
		print(k)
		if(k == 27): break
	cv2.destroyAllWindows()	

if __name__ == '__main__':
	rospy.init_node('face_control', anonymous=True)

	threading.Thread(target=prog, args=()).start()
	
	rospy.spin()
