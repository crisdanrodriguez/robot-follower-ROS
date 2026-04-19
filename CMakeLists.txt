cmake_minimum_required(VERSION 3.0.2)
project(robot_follower)

find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  geometry_msgs
  rospy
  sensor_msgs
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS
    cv_bridge
    geometry_msgs
    rospy
    sensor_msgs
    std_msgs
)

catkin_install_python(PROGRAMS
  scripts/ball_tracker_from_topic_vision.py
  scripts/ball_tracker_webcam.py
  scripts/follower_lidar.py
  scripts/follower_vision.py
  scripts/trackbars.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
