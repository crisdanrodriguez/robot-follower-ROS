#!/usr/bin/env python3

"""Generate velocity commands from LiDAR data."""

import math

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class FollowerClass:
    def __init__(self):
        rospy.init_node("follower_lidar")
        rospy.on_shutdown(self.cleanup)

        self.velocity = Twist()
        self.closest_range = 0.0
        self.closest_angle = 0.0

        self.pub_vel = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        rospy.Subscriber("front/scan", LaserScan, self.laser_cb)

        self.rate = rospy.Rate(10)
        rospy.loginfo("follower_lidar node initialized at 10 Hz")
        while not rospy.is_shutdown():
            self.velocity_controller()
            self.rate.sleep()

    def velocity_controller(self):
        kl = 0.25
        kw = 0.35

        self.velocity = Twist()

        if self.closest_range > 0.5:
            self.velocity.linear.x = kl * self.closest_range
        self.velocity.angular.z = kw * self.closest_angle

        self.pub_vel.publish(self.velocity)

    def laser_cb(self, msg):
        closest_reading = self._closest_finite_reading(msg)
        if closest_reading is None:
            self.closest_range = 0.0
            self.closest_angle = 0.0
            return

        self.closest_range, closest_index = closest_reading
        self.closest_angle = (
            msg.angle_min + closest_index * msg.angle_increment
        ) + math.radians(120)

    @staticmethod
    def _closest_finite_reading(msg):
        valid_readings = [
            (distance, index)
            for index, distance in enumerate(msg.ranges)
            if math.isfinite(distance) and distance > 0
        ]
        if not valid_readings:
            return None
        return min(valid_readings, key=lambda item: item[0])

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
