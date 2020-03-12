#!/usr/bin/env python3
"""
File:          test_raspi.py
Author:        Binit Shah
Last Modified: Binit on 2/21
"""

import interface

if __name__ == "__main__":
    interface.set_system("jetson", portA="/dev/ttyACM0")
    while True:
        print(interface.get_time())
