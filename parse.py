'''
DESCRIPTION:
This module contains a Parser for handling command files in the form of csv files.

NOTE:

AUTHOR:
D.B and G.LC

AFFILIATION:
Bio-Rad, CDG, Advanced-Tech Team

CREATED ON:
8/31/2022
'''

import argparse

class Parser(argparse.ArgumentParser):
    # Public variables.
    COM = 'COM8' #'/dev/ttyUSB0'
    baud_rate = 115200
    commands_fpath = 'commands.csv'
    responses_fpath = 'responses.csv'

    # Private variables.
    __description = "Specify COM port, commands file (in), response file (out),and baud rate"
    __args = None
    __COM_port = None
    __baud_rate = None
    __input_fpath = None
    __output_fpath = None

    # Constructur.
    def __init__(self):
        super().__init__(self, description=self.__description)
        self.add_argument('-COM', default=self.COM, required=False)
        self.add_argument('-b', default=self.baud_rate, required=False)
        self.add_argument('-i', default=self.commands_fpath, required=False)
        self.add_argument('-o', default=self.responses_fpath, required=False)
        self.__args = self.parse_args()
        self.__COM_port = self.__args.COM
        self.__baud_rate = self.__args.b
        self.__input_fpath = self.__args.i
        self.__output_fpath = self.__args.o

    def getArgs(self):
        return self._args

    def getCOMPort(self):
        return self.__COM_port

    def getBaudRate(self):
        return self.__baud_rate

    def getInputFPath(self):
        return self.__input_fpath

    def getOutputFPath(self):
        return self.__output_fpath

    def setOutputFPath(self, output_fath):
        self.__output_fpath = output_fath
        self.__args.o = output_fath


