#!/usr/bin/env python3
"""
File:          interface.py
Author:        Binit Shah
Last Modified: Binit on 2/20
"""

import time
import sim

system_type = None
system_options = ["sim", "raspi", "jetson"]

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
    global system_type

    if stype not in system_options:
        raise ValueError('system type not valid')
    system_type = stype
    if system_type == "sim":
        sim.start(sim_config)

def get_time():
    """Returns wall time of the system.

    :return: time of the device in ISO format
    :rtype:  float
    """
    if system_type == "sim":
        return sim.get_time()
    elif system_type == "raspi":
        return time.time()
    elif system_type == "jetson":
        return time.time()
    else:
        raise ValueError('system type has not been set')

def is_enabled():
    """Returns robot hard stop state.

    :return: whether robot is enabled
    :rtype:  boolean
    """
    if system_type == "sim":
        return sim.get_enabled()
    elif system_type == "raspi":
        pass
    elif system_type == "jetson":
        pass
    else:
        raise ValueError('system type has not been set')

def read_image():
    """Returns current image from the robot's camera.

    :return: non-buffered image from cam
    :rtype:  np.ndarray
    """
    if system_type == "sim":
        return sim.read_robot_cam()
    elif system_type == "raspi":
        pass
    elif system_type == "jetson":
        pass
    else:
        raise ValueError('system type has not been set')

def command_wheel_velocities(wheel_vels):
    """Commands the two motors to target angular velocities.

    :param wheels_vels: left and right target omegas (rad/s)
    :type wheel_vels:   Tuple(float, float)
    """
    if system_type == "sim":
        return sim.command_robot_vels(*wheel_vels)
    elif system_type == "raspi":
        pass
    elif system_type == "jetson":
        pass
    else:
        raise ValueError('system type has not been set')

def read_wheel_velocities():
    """Reads the two motor current angular velocities.

    :return: left and right current omegas
    :rtype:  Tuple(float, float)
    """
    if system_type == "sim":
        return sim.read_robot_vels()
    elif system_type == "raspi":
        pass
    elif system_type == "jetson":
        pass
    else:
        raise ValueError('system type has not been set')
