#!/usr/bin/env python

import subprocess

# Close all cameras
subprocess.call(["rosrun","baxter_tools","camera_control.py","-c","left_hand_camera"])
subprocess.call(["rosrun","baxter_tools","camera_control.py","-c","right_hand_camera"])
subprocess.call(["rosrun","baxter_tools","camera_control.py","-c","head_camera"])

# Open right and head cameras
subprocess.call(["rosrun","baxter_tools","camera_control.py","-o","head_camera","-r","960x600"])
subprocess.call(["rosrun","baxter_tools","camera_control.py","-o","right_hand_camera","-r","960x600"])

