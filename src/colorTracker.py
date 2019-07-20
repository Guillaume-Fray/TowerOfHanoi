#!/usr/bin/env python

"""Allows the user to calibrate for HSV filtering later."""

# Standard libraries
from argparse import ArgumentParser

# ROS libraries
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

# Other libraries
import cv2
import numpy as np


def nothing():
    """Does nothing."""

    pass


def calibrator(msg, args):
    """Updates the calibration window"""

    bridge = args
    raw = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
    hsv = cv2.cvtColor(raw, cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h_low = cv2.getTrackbarPos('H_low', 'HSV Calibrator')
    s_low = cv2.getTrackbarPos('S_low', 'HSV Calibrator')
    v_low = cv2.getTrackbarPos('V_low', 'HSV Calibrator')
    h_high = cv2.getTrackbarPos('H_high', 'HSV Calibrator')
    s_high = cv2.getTrackbarPos('S_high', 'HSV Calibrator')
    v_high = cv2.getTrackbarPos('V_high', 'HSV Calibrator')

    # Normal masking algorithm
    lower = np.array([h_low, s_low, v_low])
    upper = np.array([h_high, s_high, v_high])

    mask = cv2.inRange(hsv, lower, upper)

    result = cv2.bitwise_and(raw, raw, mask=mask)

    cv2.imshow('HSV Calibrator', result)
    cv2.waitKey(30)


def main(node, subscriber):
    """Creates a camera calibration node and keeps it running."""

    # Initialize node
    rospy.init_node(node)

    # Initialize CV Bridge
    bridge = CvBridge()

    # Create a named window to calibrate HSV values in
    cv2.namedWindow('HSV Calibrator')

    # Creating track bar
    cv2.createTrackbar('H_low', 'HSV Calibrator', 0, 179, nothing)
    cv2.createTrackbar('S_low', 'HSV Calibrator', 0, 255, nothing)
    cv2.createTrackbar('V_low', 'HSV Calibrator', 0, 255, nothing)

    cv2.createTrackbar('H_high', 'HSV Calibrator', 50, 179, nothing)
    cv2.createTrackbar('S_high', 'HSV Calibrator', 100, 255, nothing)
    cv2.createTrackbar('V_high', 'HSV Calibrator', 100, 255, nothing)

    # Subscribe to the specified ROS topic and process it continuously
    rospy.Subscriber(subscriber, Image, calibrator, callback_args=(bridge))

    rospy.spin()


if __name__ == "__main__":
    PARSER = ArgumentParser()
    PARSER.add_argument("--subscribe", "-s",
                        default="/cameras/right_hand_camera/image",
                        help="ROS topic to subcribe to (str)", type=str)
    PARSER.add_argument("--node", "-n", default="CameraCalibrator",
                        help="Node name (str)", type=str)
    ARGS = PARSER.parse_args()

    main(ARGS.node, ARGS.subscribe)
