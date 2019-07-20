#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from baxter_core_msgs.msg import DigitalIOState
from std_msgs.msg import String
from math import copysign
from artiesans.msg import correctMove
import sys
import os

nodPub = rospy.Publisher('/robot/head/command_head_nod',Bool)


# phase = 3 => Game is running

phase = 0
speak = False
faceDetected = False
userSpeech = ""
boardRecognition = False


def speech0(data):
	global phase
	if(data.data == True and phase == 0):
		command = "rosrun sound_play say.py \"Hey mate, I'm Baxter. Do you wanna play a game?\" 				voice_cmu_us_clb_arctic_clunits" 
		os.system(command)
		phase = 990
	while (phase == 990):
		for i in range (0, 300000):
			nodPub.publish( True )
			print i
		phase = 1
	nodPub.publish( False )
face_sub = rospy.Subscriber('/artiesans/facedetection',Bool,speech0)



def speech1(data):
	global phase
	if(data.data == "yes" and phase == 991):
		command = "rosrun sound_play say.py \"Boooooring. Alright. Goodbye then.\" 			voice_cmu_us_clb_arctic_clunits"
		os.system(command)
		phase = 992
	if(data.data == "no" and phase == 991):
		phase = 1
		data.data = "yes"
	if(data.data == "yes" and phase == 1):
		command = "rosrun sound_play say.py \"Great! You've just made my day! This game is 				called the Tower of Hanoi. You might have heard of it but just in case I'm 				gonna tell you the rules anyway.\" voice_cmu_us_clb_arctic_clunits" 
		os.system(command)
		for i in range (0, 700000):
			print i
		phase = 2

	if(data.data == "no" and phase == 1):
		command = "rosrun sound_play say.py \"What a shame, I'm so bored and as you can see I 				cannot move much. Bad leg. Are you sure you don't want to play?\" 				voice_cmu_us_clb_arctic_clunits" 
		os.system(command)
		phase = 991
face_sub = rospy.Subscriber('/recognizer/output',String,speech1)



def speech2(data):
	global phase
	if(data.data == "yes" and phase == 993):
		command =  "rosrun sound_play say.py \"Great! Let's get cracking. Show me your first move.\" voice_cmu_us_clb_arctic_clunits" 
		os.system(command) 
		phase = 3 
	if(data.data ==	"no" and phase == 993):
		phase = 2 
	if(phase == 2):
		command = "rosrun sound_play say.py \"You need to get all disks from the leftmost peg  to the rightmost peg, and in the exact same order. You cannot move more than one disk at a time and you cannot move a larger disk on top of a smaller one. You'll be the one moving the disks but at any time you can ask for my help by saying 'Help', or quit the game by saying 'Quit'. Do you understand?\" 			voice_cmu_us_clb_arctic_clunits"
		os.system(command)
		phase = 993
face_sub = rospy.Subscriber('/recognizer/output',String,speech2)


# Help/Quit
def speech3(data):
	global phase
	if(data.data == "help" and phase == 3):
		command =  "rosrun sound_play say.py \"No worries, I've got your back.\" voice_cmu_us_clb_arctic_clunits" 
		os.system(command)
		phase = 994
	if(data.data == "quit" and phase == 3):
		command =  "rosrun sound_play say.py \"Game over. Artiesans, please reset the game.\" 					voice_cmu_us_clb_arctic_clunits" 
		os.system(command)
		phase = 999
face_sub = rospy.Subscriber('/recognizer/output',String,speech3)

# to wait until Baxter has finished to move the disk into the right position
def speech4(data):
	global phase
	if (phase == 3 and (data.moreThanOne == True or data.biggerOnTop == True)):
		command =  "rosrun sound_play say.py \"Please put the game in its previous configuration.\" voice_cmu_us_clb_arctic_clunits" 
		os.system(command)
		phase = 4
		for i in range(200000):
			print i
		phase = 3

wrong_sub = rospy.Subscriber('errors',correctMove,speech4)



if __name__ == '__main__':
	rospy.init_node('robot_speech', anonymous=True)
	rospy.spin()
