#!/usr/bin/env python3
"""
File:          serial_communicator.py
Author:        Ammar Ratnani
Last Modified: Binit on 3/11
"""

import serial
import time

class SerialCommunicator:
    """Uses Serial to communicate with two teensies.
    """

    def __init__(self, motor_port='/dev/ttyACM0', stepper_port='/dev/ttyACM1', baud=115200, tout=.5):
        # Read from both of the ports
        self.sr_motor = serial.Serial(motor_port, baud, parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS,
        timeout=0.1)
        time.sleep(1)
        # self.sr_stepper = serial.Serial(stepper_port, baud, timeout=tout)

    def close(self):
        if self.sr_motor.isOpen():
            self.sr_motor.flush()
            self.sr_motor.close()
        if self.sr_stepper.isOpen():
            self.sr_stepper.flush()
            self.sr_stepper.close()

    def set_target_vels(self, w_r, w_l, is_conservative):
        # Can generate an exception
        # If we fail for any reason, return None
        try:
            self.sr_motor.write(str.encode(f"<{'{:.6f}'.format(w_l)},{'{:.6f}'.format(w_r)},{int(is_conservative)}>\n"))
            self.sr_motor.flush()
            raw = self.sr_motor.readline().decode("utf-8")[1:-3].split(",")
            return (float(raw[0]), float(raw[1]), float(raw[2]))
        except:
            return None

    # def prepare_for_block(self):
    #     try:
    #         # Write to the Serial
    #         self.sr_stepper.write(str.encode(f"P\n"))
    #         self.sr_stepper.flush()
    #         # No result for this one
    #     except:
    #         pass

    # def query_stepper_state(self):
    #     # The stepper board handles enabled as well
    #     try:
    #         # Write the command
    #         self.sr_stepper.write(str.encode("Q\n"))
    #         self.sr_stepper.flush()
    #         # Parse the result, stripping the <, >, and \r\n
    #         return tuple(map(lambda x: bool(int(x)),
    #             self.sr_stepper.readline()[1:-3].split(",")))
    #     except:
    #         return (None, None)
