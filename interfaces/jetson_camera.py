#!/usr/bin/env python3
"""
File:          jetson_camera.py
Author:        Binit Shah
Last Modified: Binit on 3/11
"""

import cv2

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

class JetsonCamera:

    def __init__(self):
        self.cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

    def read(self):
        if self.cap.isOpened() and cv2.getWindowProperty("CSI Camera", 0):
            ret_val, img = cap.read()
            if ret_val:
                return img
