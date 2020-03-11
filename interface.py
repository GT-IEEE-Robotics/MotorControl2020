#!/usr/bin/env python3
"""
File:          interface.py
Author:        Ammar Ratnani
Last Modified: Ammar on 2/22
"""

from simple_pid import PID
from math import sin, cos, pi, sqrt
from time import time

from iface_lib.arduino import Arduino
import sim



system_type = None
system_options = ["sim", "raspi", "jetson"]
board = None

def set_system(stype, sim_config=None):
    """Configures system type on which software is running.

    Since the low level manipulation of GPIO, image capture,
    and system type depends on the hardware upon which the
    software is running, we set the system type here. 

    :param stype:      options: ["sim", "raspi", "jetson"]
    :type stype:       str
    :param sim_config: configuration with which to start the simulator
    :type sim_config:  sim.SimConfig
    """
    global board
    global system_type

    if stype not in system_options:
        raise ValueError('system type not valid')

    system_type = stype
    if system_type == "sim":
        sim.start(sim_config)
    elif system_type == "raspi":
        pass
    elif system_type == "jetson":
        board = Arduino()
    else:
        raise ValueError(f'Invalid system type: {stype}')


def get_time():
    """Returns wall time of the system.

    :return: time of the device in ISO format
    :rtype:  float
    """
    if system_type == "sim":
        return sim.get_time()
    elif system_type in ["raspi", "jetson"]:
        return time()
    else:
        raise ValueError('System type has not been set')


def is_enabled():
    """Returns robot hard stop state.

    :return: whether robot is enabled
    :rtype:  boolean
    """
    if system_type == "sim":
        return sim.get_enabled()
    elif system_type == "raspi":
        return None
    elif system_type == "jetson":
        return board.enabled()
    else:
        raise ValueError('System type has not been set')


def read_image():
    """Returns current image from the robot's camera.

    :return: non-buffered image from cam
    :rtype:  np.ndarray
    """
    if system_type == "sim":
        return sim.read_robot_cam()
    elif system_type in ["raspi", "jetson"]:
        return None
    else:
        raise ValueError('System type has not been set')


def command_wheel_velocities(wheel_vels, is_conservative):
    """Commands the two motors to target angular velocities.
    wheel_vels[0] = left wheel target omega
    wheel_vels[1] = right wheel target omega

    :param wheels_vels:     left and right target omegas (rad/s)
    :param is_conservative: whether to accelerative aggressively or conservatively
    :type wheel_vels:       Tuple(float, float)
    :type is_conservative:  boolean
    """
    if system_type == "sim":
        return sim.command_robot_vels(*wheel_vels, is_conservative)
    elif system_type == "raspi":
        pass
    elif system_type == "jetson":
        board.setTargetVels(*wheel_vels, is_conservative)
    else:
        raise ValueError('System type has not been set')

def read_motion_update():
    """Reads the relative motion of the robot since
    we last queried the robot.
    rtype[0] = relative motion along x axis
    rtype[1] = relative motion along y axis
    rtype[2] = relative angular motion, aka heading

    :return: relative robot motion
    :rtype:  Tuple(float, float, float)
    """
    if system_type == "sim":
        return sim.read_motion_update()
    elif system_type == "raspi":
        return None
    elif system_type == "jetson":
        return board.getVels()
    else:
        raise ValueError('System type has not been set')
