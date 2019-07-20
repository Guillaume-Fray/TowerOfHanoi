#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from cv_bridge import CvBridge, CvBridgeError
import cv2

class timer:
    def __init__(self, onDelay, offDelay):
        self.onDelay = onDelay
        self.onDeleayStart = onDelay
        self.offDelay = offDelay
        self.offDelayStart = offDelay

    def getVal(self, val):
        #print(self.onDelay, self.onDeleayStart, self.offDelay, self.offDelayStart)
        if(val):
            if(self.onDelay > 0):
                ans = False
                self.onDelay = self.onDelay - 1
            else:
                ans = True

            self.offDelay = self.offDelayStart
        else:
            ans = False
            if(self.onDelay < self.onDeleayStart):
                if(self.offDelay > 0):
                    ans = True
                    if(self.onDelay > 0): ans = False
                    self.offDelay = self.offDelay - 1
                else:
                    ans = False
                    self.onDelay = self.onDeleayStart

        return ans
            

# publisher to which we post whether a face has been detected or not
pub = rospy.Publisher('/artiesans/facedetection',Bool)

t = timer(8, 25)

#callback function for camera subscriber, called by the camera subscriber for every frame.
def callback(data):
    global t

    bridge = CvBridge()
    
    #Convert incoming image from a ROS image message to a CV image that open CV can process.
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")

    #Display the converted cv image, this is the raw camera feed data.
    #cv2.imshow("Head Camera Feed", cv_image)

    #detect faces
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray", gray)
    
    face_cascade = cv2.CascadeClassifier('/opt/ros/groovy/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray,1.3,5)


    ans = t.getVal(len(faces) > 0)

    color = (255, 0, 0)

    if(ans):
        color = (0, 255, 0)

    cv2.rectangle(cv_image,(3,3),(10,20),color,2)

    for(x,y,w,h)in faces:
        cv2.rectangle(cv_image,(x,y),(x+w,y+h),(255,0,0),2)


    publisher = rospy.Publisher('/robot/xdisplay', Image)
    

    #cv2.imshow("Image", cv_image)
    #cv2.imshow("gray", gray)
    cv2.imshow("Image", cv_image)
    
    #print(rospy.Subscriber("/hanoi/var",String,callback))
    #Publish detected true/false
    pub.publish( ans )
    
    
    #publisher.publish(bridge.cv2_to_imgmsg(cv_image, "bgr8"))

    cv2.waitKey(1) # needed for cv2.imshow to take effect. REMOVE otherwise

#create subscriber to the right hand camera, each frame recieved calls the callback function
camera_sub = rospy.Subscriber("/cameras/head_camera/image",Image,callback)

if __name__ == '__main__':
    rospy.init_node('facedetection', anonymous=True)
    rospy.spin()


