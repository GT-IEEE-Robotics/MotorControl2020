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

    def __init__(self, portA='/dev/ttyACM0', portB='/dev/ttyACM1', baud=115200, tout=.5):
        # Read from both of the ports
        sr1 = serial.Serial(portA, baud, timeout=tout)
        sr2 = serial.Serial(portA, baud, timeout=tout)
        # Wait for the arduinos to boot, then read the result
        time.sleep(3)
        sr1res = sr1.readline().decode("utf-8")[0:-2]
        sr2res = sr2.readline().decode("utf-8")[0:-2]

        # Figure out which one is which
        if sr1res not in ["stepper","motor"] \
        or sr2res not in ["stepper","motor"] \
        or sr1res != sr2res:
            raise RuntimeError("Invalid arduinos")
        elif sr1res == "stepper":
            self.sr_stepper = sr1
            self.sr_motor = sr2
        elif sr2res == "stepper":
            self.sr_stepper = sr2
            self.sr_motor = sr1
        else:
            raise RuntimeError("Invalid arduinos")

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
            # Write to the Serial
            self.sr_motor.write(str.encode(f"<{w_l},{w_r},{int(is_conservative)}>\n"))
            self.sr_motor.flush()
            # Parse the result
            return tuple(map(int,
                self.sr_motor.readline().decode("utf-8")[1:-3].split(",")))
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
