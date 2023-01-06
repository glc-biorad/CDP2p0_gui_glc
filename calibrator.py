'''
Offset based on current current unit A coordinates.
 Better practice would be to give each unit their own coordinate.py
  so that testing at unit A does not affect the other units inadvertently.
'''

from upper_gantry_coordinate import UpperGantryCoordinate
from reader_coordinate import ReaderCoordinate

class Calibrator():
    # Public variables.
    # Private variables.
    __unit = None

    # Private constants.
    __UNITS = {
        'A': {
            'location': '',
            'calibrated': True,
            },
        'B': {},
        'C': {},
        'D': {},
        'E': {},
        'F': {},
        }

    __OFFSETS = {
        'steps': {
            'pipettor_gantry': {
                'x': {
                    'A': 0,
                    'B': 5500,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                'y': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                'z': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                'drip_plate': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                },
            'reader': {
                'x': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                'y': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                'z': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                'filter_wheel': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                },
            },
        'velocity': {
            'pipettor_gantry': {
                'x': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                'y': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                'z': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                'drip_plate': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                },
            'reader': {
                'x': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                'y': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                'z': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                'filter_wheel': {
                    'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 0,
                    'E': 0,
                    'F': 0,
                    },
                },
            },
        'temperature': {},
        'volume': {},
        }

    def __init__(self, unit):
        self.__unit = unit

    def get_unit(self):
        return self.__unit

    def calibrate(self, offset_type, module_name, unit_A_ugc):
        # Get the offset from unit A.
        if offset_type == 'steps' or offset_type == 'velocity':
            x_offset = self.__OFFSETS[offset_type][module_name]['X'][self.__unit]
            y_offset = self.__OFFSETS[offset_type][module_name]['Y'][self.__unit]
            z1_offset = self.__OFFSETS[offset_type][module_name]['Z'][self.__unit]
            x = unit_A_ugc.x + x_offset
            y = unit_A_ugc.y + y_offset
            z1 = unit_A_ugc.z + z1_offset
            if module_name == 'pipettor_gantry':
                z2_offset = self.__OFFSETS[offset_type][module_name]['drip plate'][self.__unit]
                z2 = unit_A_ugc.drip_plate + z2_offset
                return UpperGantryCoordinate(x, y, z1, z2)
            elif module_name == 'reader':
                z2_offset = self.__OFFSETS[offset_type][module_name]['filter wheel'][self.__unit]
                z2 = unit_A_ugc.filter_wheel + z2_offset
                return ReaderCoordinate(x, y, z1, z2)
                        