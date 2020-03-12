#!/usr/bin/env python3
"""
File:          teleop.py
Author:        Binit Shah
Last Modified: Binit on 3/11
"""

import argparse
import curses
import interface

vel_limit = 10
vel_delta = 0.1
vel_ltarget = 0.0
vel_rtarget = 0.0

def increaseLTargetVel():
    global vel_ltarget, vel_rtarget
    vel_ltarget += vel_delta
    if vel_ltarget >= vel_limit:
        vel_ltarget = vel_limit

def decreaseLTargetVel():
    global vel_ltarget, vel_rtarget
    vel_ltarget -= vel_delta
    if vel_ltarget <= -vel_limit:
        vel_ltarget = -vel_limit

def increaseRTargetVel():
    global vel_ltarget, vel_rtarget
    vel_rtarget += vel_delta
    if vel_rtarget >= vel_limit:
        vel_rtarget = vel_limit

def decreaseRTargetVel():
    global vel_ltarget, vel_rtarget
    vel_rtarget -= vel_delta
    if vel_rtarget <= -vel_limit:
        vel_rtarget = -vel_limit

def process_keyboard_events(char):
    """Read keyboard events
    And publishes them for all of game to process
    """
    if char == ord('q'):
        exit()
    elif char == curses.KEY_LEFT:
        increaseRTargetVel()
        decreaseLTargetVel()
    elif char == curses.KEY_RIGHT:
        increaseLTargetVel()
        decreaseRTargetVel()
    elif char == curses.KEY_UP:
        increaseLTargetVel()
        increaseRTargetVel()
    elif char == curses.KEY_DOWN:
        decreaseLTargetVel()
        decreaseRTargetVel()

def main(porta, portb, do_visualize):
    global vel_ltarget, vel_rtarget
    screen = curses.initscr() # get the curses screen window
    curses.noecho() # turn off input echoing
    curses.cbreak() # respond to keys immediately (don't wait for enter)
    screen.keypad(True) # map arrow keys to special values
    screen.addstr(0, 0, "arrow keys to control, q to exit")
    interface.set_system("jetson", portA=porta, portB=portb)

    try:
        while True:
            char = screen.getch()
            screen.clear()
            process_keyboard_events(char)
            vel_ltarget = round(vel_ltarget, 1)
            vel_rtarget = round(vel_rtarget, 1)
            screen.addstr(0, 0, f"vel_ltarget: {vel_ltarget}, vel_rtarget: {vel_rtarget}")
            interface.command_wheel_velocities((vel_ltarget, vel_rtarget))
    finally:
        # shut down cleanly
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("porta", help="port name of the serial connection to the teensy, typically /dev/tty*", type=str)
    parser.add_argument("portb", help="port name of the serial connection to the teensy, typically /dev/tty*", type=str)
    parser.add_argument('-v', help="visualization, false disables pygame viz", action='store_true')
    args = parser.parse_args()

    main(args.porta, args.portb, args.v)
