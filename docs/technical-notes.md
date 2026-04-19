# Technical Notes

## Package Summary

`robot_follower` is a ROS 1 `catkin` package built around small Python nodes for object following. The repository currently provides two independent control pipelines:

- visual tracking from camera images
- nearest-object following from LiDAR scans

## Nodes

| Node | Purpose | Key Inputs | Key Outputs |
| --- | --- | --- | --- |
| `ball_tracker_webcam.py` | Detects a colored object from a USB camera feed and publishes image-space target data. | `/usb_cam/image_raw` | `center`, `radius`, `kl` |
| `ball_tracker_from_topic_vision.py` | Detects a colored object from a ROS image topic and publishes image-space target data. | `/two_wheels_robot/camera1/image_raw` | `center`, `radius` |
| `follower_vision.py` | Converts visual target position and size into proportional `cmd_vel` commands. | `center`, `radius`, `kl` | `cmd_vel` |
| `follower_lidar.py` | Uses the nearest valid LiDAR return to generate proportional `cmd_vel` commands. | `front/scan` | `cmd_vel` |
| `trackbars.py` | Interactive HSV tuning utility for webcam-based calibration. | webcam stream | local OpenCV windows |

## Implementation Notes

- The project uses direct Python ROS nodes instead of a larger package layout, which keeps the repository lightweight and easy to inspect.
- Vision nodes rely on OpenCV, `cv_bridge`, and `imutils` for image processing and contour handling.
- The LiDAR follower filters non-finite scan values before computing the closest target, which makes the node safer to run on noisy scan streams.

## Scope

This repository does not currently include launch files, simulation assets, recorded bags, or hardware abstraction layers. The documentation and README intentionally reflect only the assets that are present in the repo today.
