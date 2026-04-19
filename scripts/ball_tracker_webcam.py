#!/usr/bin/env python3

"""Track a colored object from a webcam ROS image stream."""

import cv2
import imutils
import rospy
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Point
from sensor_msgs.msg import Image
from std_msgs.msg import Int32


class BallTracker:
    def __init__(self):
        rospy.init_node("ball_tracker")
        rospy.on_shutdown(self.cleanup)

        self.bridge_object = CvBridge()
        self.center_ros = Point()
        self.radius_ros = 0
        self.cnt_length = 0

        self.init_trackbars()

        self.pub_center = rospy.Publisher("center", Point, queue_size=10)
        self.pub_radius = rospy.Publisher("radius", Int32, queue_size=10)
        self.pub_kl = rospy.Publisher("kl", Int32, queue_size=10)

        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.camera_callback)

        ros_rate = rospy.Rate(10)
        rospy.loginfo("ball_tracker webcam node initialized at 10 Hz")
        while not rospy.is_shutdown():
            if self.cnt_length == 0:
                self.center_ros = Point()
                self.radius_ros = 0

            self.pub_center.publish(self.center_ros)
            self.pub_radius.publish(self.radius_ros)
            ros_rate.sleep()

    def camera_callback(self, data):
        try:
            frame = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as error:
            rospy.logerr(error)
            return

        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        ilow_h = cv2.getTrackbarPos("lowH", "image")
        ihigh_h = cv2.getTrackbarPos("highH", "image")
        ilow_s = cv2.getTrackbarPos("lowS", "image")
        ihigh_s = cv2.getTrackbarPos("highS", "image")
        ilow_v = cv2.getTrackbarPos("lowV", "image")
        ihigh_v = cv2.getTrackbarPos("highV", "image")
        erode = cv2.getTrackbarPos("erode", "image")
        dilate = cv2.getTrackbarPos("dilate", "image")

        kl = cv2.getTrackbarPos("kl", "image")
        self.pub_kl.publish(kl)

        hsv_lower = (ilow_h, ilow_s, ilow_v)
        hsv_upper = (ihigh_h, ihigh_s, ihigh_v)

        mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
        mask = cv2.erode(mask, None, iterations=erode)
        mask = cv2.dilate(mask, None, iterations=dilate)
        cv2.imshow("Mask", mask)

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

        cv2.imshow("Frame", frame)
        cv2.waitKey(1)

    def init_trackbars(self):
        cv2.namedWindow("image")

        ilow_h = 0
        ihigh_h = 13
        ilow_s = 66
        ihigh_s = 255
        ilow_v = 115
        ihigh_v = 255
        erode = 5
        dilate = 10
        kl = 10

        cv2.createTrackbar("lowH", "image", ilow_h, 255, self.callback)
        cv2.createTrackbar("highH", "image", ihigh_h, 255, self.callback)
        cv2.createTrackbar("lowS", "image", ilow_s, 255, self.callback)
        cv2.createTrackbar("highS", "image", ihigh_s, 255, self.callback)
        cv2.createTrackbar("lowV", "image", ilow_v, 255, self.callback)
        cv2.createTrackbar("highV", "image", ihigh_v, 255, self.callback)
        cv2.createTrackbar("erode", "image", erode, 10, self.callback)
        cv2.createTrackbar("dilate", "image", dilate, 10, self.callback)
        cv2.createTrackbar("kl", "image", kl, 30, self.callback)

    @staticmethod
    def callback(_value):
        pass

    @staticmethod
    def cleanup():
        cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        BallTracker()
    except rospy.ROSInterruptException:
        pass
