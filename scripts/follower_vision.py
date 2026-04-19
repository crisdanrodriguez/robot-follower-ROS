#!/usr/bin/env python3

"""Generate velocity commands from image-space target detections."""

import rospy
from geometry_msgs.msg import Point, Twist
from std_msgs.msg import Int32


class FollowerClass:
    def __init__(self):
        rospy.init_node("follower_vision")
        rospy.on_shutdown(self.cleanup)

        self.velocity = Twist()
        self.img_half_x = 300
        self.ball_x = 0
        self.radius = 0
        self.kl = 3

        self.pub_vel = rospy.Publisher("cmd_vel", Twist, queue_size=1)

        rospy.Subscriber("center", Point, self.center_cb)
        rospy.Subscriber("radius", Int32, self.radius_cb)
        rospy.Subscriber("kl", Int32, self.kl_cb)

        self.rate = rospy.Rate(10)
        rospy.loginfo("follower_vision node initialized at 10 Hz")
        while not rospy.is_shutdown():
            if self.radius == 0:
                self.stop()
            else:
                self.velocity_controller()
            self.rate.sleep()

    def velocity_controller(self):
        kw = 0.001
        x_offset = self.img_half_x - self.ball_x

        self.velocity = Twist()
        if abs(x_offset) > 15:
            self.velocity.angular.z = kw * x_offset
        if 50 < self.radius < 200:
            self.velocity.linear.x = self.kl * (1 / self.radius)

        self.pub_vel.publish(self.velocity)

    def center_cb(self, point):
        self.ball_x = point.x

    def radius_cb(self, msg):
        self.radius = msg.data

    def kl_cb(self, msg):
        self.kl = msg.data

    def stop(self):
        self.velocity = Twist()
        self.pub_vel.publish(self.velocity)

    def cleanup(self):
        self.stop()


if __name__ == "__main__":
    try:
        FollowerClass()
    except rospy.ROSInterruptException:
        pass
