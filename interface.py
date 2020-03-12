#!/usr/bin/env python3
"""
File:          interface.py
Author:        Ammar Ratnani
Last Modified: Binit on 3/11
"""

import sim
from time import time
from interfaces.serial_communicator import SerialCommunicator
from interfaces.jetson_camera import JetsonCamera

system_type = None
comms = None
cam = None

def set_system(stype, sim_config=None, motor_port='/dev/ttyACM0', stepper_port='/dev/ttyACM1'):
    """Configures system type on which software is running.

    Since the low level manipulation of GPIO, image capture,
    and system type depends on the hardware upon which the
    software is running, we set the system type here. 

    :param stype:        options: ["sim", "raspi", "jetson"]
    :type stype:         str
    :param sim_config:   configuration with which to start the simulator
    :type sim_config:    sim.SimConfig
    :param motor_port:   serial port of the motor controller
    :type motor_port:    str
    :param stepper_port: serial port of the stepper controller
    :type stepper_port:  str
    """
    global system_type, comms, cam

    if stype not in ["sim", "raspi", "jetson"]:
        raise ValueError('system type not valid')

    system_type = stype
    if system_type == "sim":
        sim.start(sim_config)
    elif system_type == "raspi":
        comms = SerialCommunicator(motor_port=motor_port, stepper_port=stepper_port)
    elif system_type == "jetson":
        cam = JetsonCamera()
        comms = SerialCommunicator(motor_port=motor_port, stepper_port=stepper_port)
    else:
        raise ValueError(f'Invalid system type: {stype}')


def get_time():
    """Returns wall time of the system.

    :return: time of the device in ISO format
    :rtype:  float
    """
    global system_type

    if system_type == "sim":
        return sim.get_time()
    elif system_type in ["raspi", "jetson"]:
        return time()
    else:
        raise ValueError('System type has not been set')


def read_image():
    """Returns current image from the robot's camera.

    :return: non-buffered image from cam
    :rtype:  np.ndarray
    """
    global system_type, cam

    if system_type == "sim":
        return sim.read_robot_cam()
    elif system_type == "raspi":
        return None
    elif system_type == "jetson":
        return cam.read()
    else:
        raise ValueError('System type has not been set')


def command_wheel_velocities(wheel_vels, is_conservative=False):
    """Commands the two motors to target angular velocities.
    wheel_vels[0] = left wheel target omega
    wheel_vels[1] = right wheel target omega

    Returns the relative motion of the robot since
    we last pinged the robot.
    rtype[0] = relative motion along x axis
    rtype[1] = relative motion along y axis
    rtype[2] = relative angular motion, aka heading

    :param wheels_vels:     left and right target omegas (rad/s)
    :param is_conservative: whether to accelerative aggressively or conservatively
    :type wheel_vels:       Tuple(float, float)
    :type is_conservative:  boolean
    :return:                relative robot motion
    :rtype:                 Tuple(float, float, float)
    """
    global system_type, comms

    if system_type == "sim":
        return sim.command_robot_vels(*wheel_vels)
    elif system_type == "raspi":
        return comms.set_target_vels(*wheel_vels, is_conservative)
    elif system_type == "jetson":
        return comms.set_target_vels(*wheel_vels, is_conservative)
    else:
        raise ValueError('System type has not been set')

# def trigger_block_stacker():
#     """Let the hardware know we're expecting to
#     pick up a block.
#     """
#     global system_type, comms

#     if system_type == "sim":
#         return sim.trigger_block_stacker()
#     elif system_type == "raspi":
#         return None
#     elif system_type == "jetson":
#         return board.trigger_block_stacker()
#     else:
#         raise ValueError('System type has not been set')


# def is_enabled():
#     """Returns robot hard stop state.

#     :return: whether robot is enabled
#     :rtype:  boolean
#     """
#     global system_type, comms

#     if system_type == "sim":
#         return sim.get_enabled()
#     elif system_type == "raspi":
#         return None
#     elif system_type == "jetson":
#         return board.enabled()
#     else:
#         raise ValueError('System type has not been set')
