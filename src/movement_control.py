#!/usr/bin/env python

import rospy
from artiesans.msg import correctMove, uint8Array
from std_msgs.msg import String
import baxter_interface
import sys
import os



move = [0, 0]
def setPos(data):
	move[0] = data.data[0]
	move[1] = data.data[1]

error = False
def setError(data):
	error = data.moreThanOne or data.biggerOnTop or data.oneLess

def callback(data):
	start = {'left_s0': -1.25517977825, 'left_s1': -0.136140794769, 'left_e0': -0.000766990393066, 'left_e1': -0.0490873851563, 'left_w0': -3.04303438449, 'left_w1': -1.56772836343, 'left_w2': 1.76829635121}
	position1 = {'left_s0': -1.27972347083, 'left_s1': 0.0947233135437, 'left_e0': -0.28877188299, 'left_e1': 0.174106819226, 'left_w0': -2.71437900106, 'left_w1': -1.14511665685, 'left_w2': 1.56696137303}
	position0 = {'left_s0': -1.30043221144, 'left_s1':0.106995159833, 'left_e0': -0.178708761584, 'left_e1': 0.158767011365, 'left_w0': -2.77343726133, 'left_w1': -1.3936215442, 'left_w2': 1.570796325}
	position2 = {'left_s0': -1.23753899921, 'left_s1': 0.0483203947632, 'left_e0': -0.345912667273, 'left_e1': 0.355500047186, 'left_w0': -2.69788870761, 'left_w1': -0.763922431494, 'left_w2': 1.57501477216}
	arm = baxter_interface.Limb('left')
	global move
	global error

	print (data)
	#TODO finish the if statement
	if(not error and data.data == 'help' and move[0] != 3):
		if(move[0] == 0):
			arm.move_to_joint_positions(position0)
			arm.move_to_joint_positions(position0)
			arm.move_to_joint_positions(position0)
			arm.move_to_joint_positions(position0)
			arm.move_to_joint_positions(position0)
			arm.move_to_joint_positions(position0)



		elif(move[0] == 1):
			arm.move_to_joint_positions(position1)
			arm.move_to_joint_positions(position1)
			arm.move_to_joint_positions(position1)
			arm.move_to_joint_positions(position1)
			arm.move_to_joint_positions(position1)
			arm.move_to_joint_positions(position1)
		elif(move[0] == 2):
			arm.move_to_joint_positions(position2)
			arm.move_to_joint_positions(position2)
			arm.move_to_joint_positions(position2)
			arm.move_to_joint_positions(position2)
			arm.move_to_joint_positions(position2)
			arm.move_to_joint_positions(position2)
		if(move[1] == 0):
			arm.move_to_joint_positions(position0)
			arm.move_to_joint_positions(position0)
			arm.move_to_joint_positions(position0)
			arm.move_to_joint_positions(position0)
			arm.move_to_joint_positions(position0)
			arm.move_to_joint_positions(position0)
		elif(move[1] == 1):
			arm.move_to_joint_positions(position1)
			arm.move_to_joint_positions(position1)
			arm.move_to_joint_positions(position1)
			arm.move_to_joint_positions(position1)
			arm.move_to_joint_positions(position1)
			arm.move_to_joint_positions(position1)
		elif(move[1] == 2):
			arm.move_to_joint_positions(position2)
			arm.move_to_joint_positions(position2)
			arm.move_to_joint_positions(position2)
			arm.move_to_joint_positions(position2)
			arm.move_to_joint_positions(position2)
			arm.move_to_joint_positions(position2)

		arm.move_to_joint_positions(start)
		arm.move_to_joint_positions(start)
		arm.move_to_joint_positions(start)
		arm.move_to_joint_positions(start)
		arm.move_to_joint_positions(start)
		arm.move_to_joint_positions(start)



sub1 = rospy.Subscriber('/recognizer/output',String,callback)
sub2 = rospy.Subscriber("move",uint8Array,setPos)
sub2 = rospy.Subscriber("errors",correctMove,setError)

if __name__ == '__main__':
    rospy.init_node('movement_control', anonymous=True)
    rospy.spin()
