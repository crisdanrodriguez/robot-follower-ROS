# Robot Follower ROS

[![Python](https://img.shields.io/badge/Python-3.x-0A66C2?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![ROS](https://img.shields.io/badge/ROS-1%20%7C%20Catkin-0A66C2?style=flat-square&logo=ros&logoColor=white)](http://wiki.ros.org/catkin)
[![Tests](https://img.shields.io/github/actions/workflow/status/crisdanrodriguez/robot_follower_ROS/ci.yml?branch=main&style=flat-square&label=Tests&logo=githubactions&logoColor=white)](https://github.com/crisdanrodriguez/robot_follower_ROS/actions/workflows/ci.yml)

ROS 1 package for object following with two control pipelines: vision-based tracking from camera images and LiDAR-based following from laser scans.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Results](#results)
- [Documentation](#documentation)
- [Development](#development)
- [License](#license)
- [AI Assistance and Last Updated](#ai-assistance-and-last-updated)

## Overview

This repository contains a compact ROS 1 `catkin` package that publishes `cmd_vel` commands from either:

- Image-based ball detection and proportional visual servoing
- LiDAR-based nearest-object following

The package is organized around standalone Python nodes so it can be dropped into a ROS workspace without extra scaffolding.

## Installation

Example setup for a ROS 1 `catkin` workspace:

```bash
cd ~/catkin_ws/src
git clone https://github.com/crisdanrodriguez/robot_follower_ROS.git
cd ..
catkin_make
source devel/setup.bash
```

Example dependency installation for Ubuntu with ROS Noetic:

```bash
sudo apt install \
  ros-noetic-cv-bridge \
  ros-noetic-geometry-msgs \
  ros-noetic-sensor-msgs \
  ros-noetic-std-msgs \
  python3-opencv \
  python3-pip

pip3 install imutils
```

Notes:

- ROS message and bridge dependencies are declared in [`package.xml`](package.xml).
- `imutils` is used by the vision nodes and should be installed separately in your Python environment.
- Runtime behavior depends on the topics exposed by your robot or simulator.

## Usage

Vision-based tracking from a USB camera:

```bash
rosrun robot_follower ball_tracker_webcam.py
rosrun robot_follower follower_vision.py
```

Vision-based tracking from an image topic:

```bash
rosrun robot_follower ball_tracker_from_topic_vision.py
rosrun robot_follower follower_vision.py
```

LiDAR-based following:

```bash
rosrun robot_follower follower_lidar.py
```

Topic expectations in the current codebase:

- `ball_tracker_webcam.py` subscribes to `/usb_cam/image_raw`
- `ball_tracker_from_topic_vision.py` subscribes to `/two_wheels_robot/camera1/image_raw`
- `follower_lidar.py` subscribes to `front/scan`
- controller nodes publish velocity commands to `cmd_vel`

## Project Structure

```text
robot-follower-ROS/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── assets/
│   │   └── project-team.jpg
│   └── technical-notes.md
├── scripts/
│   ├── ball_tracker_from_topic_vision.py
│   ├── ball_tracker_webcam.py
│   ├── follower_lidar.py
│   ├── follower_vision.py
│   └── trackbars.py
├── tests/
│   └── test_scripts_compile.py
├── .editorconfig
├── .gitattributes
├── .gitignore
├── CMakeLists.txt
├── package.xml
└── README.md
```

## Results

- Demo video: [Robot follower demonstration](https://youtu.be/YEb-h3hIXVE)
- Project image: [docs/assets/project-team.jpg](docs/assets/project-team.jpg)

## Documentation

- Technical notes: [docs/technical-notes.md](docs/technical-notes.md)

## Development

Basic local validation:

```bash
python3 -m compileall scripts tests
python3 -m unittest discover -s tests -p 'test_*.py'
```

The included GitHub Actions workflow runs lightweight validation focused on syntax and test discovery without assuming a full ROS runtime in CI.

## License

This repository is currently marked as `UNLICENSED`, and no standalone license file is included. Add an explicit license before redistributing or reusing the code outside this repository.

## AI Assistance and Last Updated

AI assistance was used for repository curation, documentation refinement, packaging cleanup, and non-functional code quality improvements. 

Last updated: April 19, 2026.
