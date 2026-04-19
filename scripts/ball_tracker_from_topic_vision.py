#!/usr/bin/env python3

"""Track a colored object from a ROS image topic."""

import argparse
from collections import deque

import cv2
import imutils
import numpy as np
import rospy
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Point
from sensor_msgs.msg import Image
from std_msgs.msg import Int32


class BallTracker:
    def __init__(self):
        rospy.init_node("ball_tracker")
        rospy.on_shutdown(self.cleanup)

        self.pub_center = rospy.Publisher("center", Point, queue_size=10)
        self.pub_radius = rospy.Publisher("radius", Int32, queue_size=10)
        self.image_sub = rospy.Subscriber(
            "/two_wheels_robot/camera1/image_raw",
            Image,
            self.camera_callback,
        )

        self.bridge_object = CvBridge()
        self.center_ros = Point()
        self.radius_ros = 0
        self.cnt_length = 0
        self.frame = None

        parser = argparse.ArgumentParser(
            description="Track a colored object from a ROS image topic."
        )
        parser.add_argument(
            "-b",
            "--buffer",
            type=int,
            default=64,
            help="max buffer size for the trail visualization",
        )
        self.args = vars(parser.parse_args(rospy.myargv()[1:]))

        self.red_lower = (0, 50, 0)
        self.red_upper = (15, 255, 255)
        self.pts = deque(maxlen=self.args["buffer"])

        ros_rate = rospy.Rate(10)
        rospy.loginfo("ball_tracker topic node initialized at 10 Hz")
        while not rospy.is_shutdown():
            if self.cnt_length == 0:
                self.center_ros = Point()
                self.radius_ros = 0
            self.pub_center.publish(self.center_ros)
            self.pub_radius.publish(self.radius_ros)
            ros_rate.sleep()

    def camera_callback(self, data):
        try:
            self.frame = self.bridge_object.imgmsg_to_cv2(
                data,
                desired_encoding="bgr8",
            )
        except CvBridgeError as error:
            rospy.logerr(error)
            return

        frame = imutils.resize(self.frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.red_lower, self.red_upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        self.cnt_length = len(cnts)
        if self.cnt_length > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            moments = cv2.moments(c)

            if moments["m00"] != 0:
                center = (
                    int(moments["m10"] / moments["m00"]),
                    int(moments["m01"] / moments["m00"]),
                )
            else:
                self.cnt_length = 0

            if radius > 10 and center is not None:
                self.center_ros.x = float(x)
                self.center_ros.y = float(y)
                self.center_ros.z = 0.0
                self.radius_ros = int(radius)

                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        self.pts.appendleft(center)

        for index in range(1, len(self.pts)):
            if self.pts[index - 1] is None or self.pts[index] is None:
                continue

            thickness = int(np.sqrt(self.args["buffer"] / float(index + 1)) * 2.5)
            cv2.line(frame, self.pts[index - 1], self.pts[index], (0, 0, 255), thickness)

        cv2.imshow("Frame", frame)
        cv2.waitKey(1)

    @staticmethod
    def cleanup():
        cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        BallTracker()
    except rospy.ROSInterruptException:
        pass
