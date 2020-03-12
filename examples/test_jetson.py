#!/usr/bin/env python3
"""
File:          test_jetson.py
Author:        Binit Shah
Last Modified: Binit on 3/12
"""

import interface
import time

if __name__ == "__main__":
    interface.set_system("jetson", motor_port="/dev/cu.usbmodem36428601")
    while True:
        # print(interface.command_wheel_velocities((0.0, 0.0)))
        print(interface.get_time())
        time.sleep(3)
