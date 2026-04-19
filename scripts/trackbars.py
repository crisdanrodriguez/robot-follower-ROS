#!/usr/bin/env python3

"""Interactive HSV tuning utility for webcam-based calibration."""

import cv2
import imutils
import numpy as np


def callback(_value):
    pass


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam device 0.")

    cv2.namedWindow("image")

    ilow_h = 0
    ihigh_h = 7
    ilow_s = 220
    ihigh_s = 255
    ilow_v = 182
    ihigh_v = 255
    erode = 0
    dilate = 0

    cv2.createTrackbar("lowH", "image", ilow_h, 255, callback)
    cv2.createTrackbar("highH", "image", ihigh_h, 255, callback)
    cv2.createTrackbar("lowS", "image", ilow_s, 255, callback)
    cv2.createTrackbar("highS", "image", ihigh_s, 255, callback)
    cv2.createTrackbar("lowV", "image", ilow_v, 255, callback)
    cv2.createTrackbar("highV", "image", ihigh_v, 255, callback)
    cv2.createTrackbar("erode", "image", erode, 10, callback)
    cv2.createTrackbar("dilate", "image", dilate, 10, callback)

    try:
        while True:
            ilow_h = cv2.getTrackbarPos("lowH", "image")
            ihigh_h = cv2.getTrackbarPos("highH", "image")
            ilow_s = cv2.getTrackbarPos("lowS", "image")
            ihigh_s = cv2.getTrackbarPos("highS", "image")
            ilow_v = cv2.getTrackbarPos("lowV", "image")
            ihigh_v = cv2.getTrackbarPos("highV", "image")
            erode = cv2.getTrackbarPos("erode", "image")
            dilate = cv2.getTrackbarPos("dilate", "image")

            ret, frame = cap.read()
            if not ret:
                continue

            frame = imutils.resize(frame, width=600)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_hsv = np.array([ilow_h, ilow_s, ilow_v])
            higher_hsv = np.array([ihigh_h, ihigh_s, ihigh_v])

            mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
            mask = cv2.erode(mask, None, iterations=erode)
            mask = cv2.dilate(mask, None, iterations=dilate)

            cv2.imshow("hsv", hsv)
            cv2.imshow("mask", mask)
            cv2.imshow("frame", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
