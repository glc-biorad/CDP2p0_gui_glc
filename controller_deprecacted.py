
'''
DESCRIPTION:
This module contains the Controller which deals with read/writing to the COM port and executing commands. 

USAGE:
python controller.py -COM COM_port -i input_filename -o output_filename

NOTES:
Controller is inherets from serial.Serial

All command line arguments are optional, the default arguments are defined
at the top of this file. The input commands are assumed
to be separated by a newline character (one command per line). The output is
(command), (response)
..., ...

This file should read a csv file to get a list of serial commands, store those
in the approriate data structure, write the commands in an arbitrary order to
a specifiable COM port (default /dev/ttyUSB0), record the response in a separate
csv file, preferably also with the command that produced the response
'''

import sys
import time
import serial

from coordinate import Coordinate
from parse import Parser

from commands import commands

class ControllerDeprecated(serial.Serial):
    # Public variables.

    # Private variables.
    __COM_port = None
    __baud_rate = None
    __parser = Parser()
    __command_list = None
    __ADDRESS_MOTOR_X = 0x01
    __ADDRESS_MOTOR_Y = 0x02
    __ADDRESS_MOTOR_Z = 0x03
    __VELOCITY = Coordinate([100000, 100000, 100000])

    def __init__(self):
        # Get the COM port and baud rate.
        self.__COM_port = self.__parser.getCOMPort()
        self.__baud_rate = self.__parser.getBaudRate()

        # Setup the serial connection to the COM port.
        try:
            super().__init__(self.__COM_port, self.__baud_rate, timeout=2)
        except Exception as e:
            print(e)
            print("Connection timeout on COM port {0}".format(self.__COM_port))