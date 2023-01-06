''' The goal for this file is to be able to wrap functions to control the
instrument to make execution on CDP2.0 independent of implementation
'''

# pipettor stuff, may want to move this to upper_gantry
import pythonnet
from pythonnet import load
load("coreclr")
# from logger import Logger

from upper_gantry import UpperGantry
from reader import Reader
#from peltier import Peltier
from led import LEDS

led_colors = [LEDS[k]['name'] for k in LEDS.keys()]

class Connection_Interface(object):
    def __init__(self,):
        # init reader (xyz motion, imager, filterwheel, )
        self.reader = Reader()
        # init upper gantry (pipettor, xyz1z2 motion)
        self.upper_gantry = UpperGantry()
        # init prep deck components
        # init thermocyclers


    # upper gantry
    def moveAspirateDispense(self, start, end, asp_vol, disp_vol, **kwargs):
        self.upper_gantry.move_aspirate_dispense(self, start, end,
            asp_vol, disp_vol, use_drip_plate_source=True,
            use_drip_plate_target=True, **kwargs)

    def moveUpperGantry(self, loc, **kwargs):
        ''' would be great if loc could be a string, a number in microsteps, or
        a number in mm'''
        self.upper_gantry.move_pipettor(self, loc, use_drip_plate=True,
            pipette_tip_type=None, use_z=True, **kwargs)

    def homeUpperGantry(self,):
        self.upper_gantry.home_pipettor()

    def turnOnSuction(self,):
        pass

    def turnOffSuction(self,):
        pass

    def aspirate(self, asp_vol, **kwargs):
        self.upper_gantry.aspirate(self, asp_vol, pressure=None,
            pipette_tip_type=None, **kwargs)

    def dispense(self, disp_vol, **kwargs):
        self.upper_gantry.dispense(self, disp_vol, pressure=None,
            pipette_tip_type=None, **kwargs)


    # prep deck stuff
    def setPreampTemp(self, temp):
        pass
    def getPreampTemp(self,):
        pass
    def setHSTemp(self, temp):
        pass
    def getGSTemp(self,):
        pass
    def setHSSpeed(self, rpm):
        pass
    def startHSShake(self,):
        pass
    def stopHSShake(self,):
        pass
    def engageMagSep(self,):
        pass
    def disengageMagSep(self,):
        pass
    def setAuxHTemp(self, num, temp):
        pass
    def getAuxHTemp(self, num):
        pass
    def setChillerTemp(self, temp):
        pass
    def getChillerTemp(self,):
        pass

    # reader stuff
    def homeImager(self,):
        self.reader.home_reader()

    def get_pos_reader_submodule(self, submodule):
        return int(self.reader.get_position_submodule(submodule))

    def moveImager(self, loc):
        ''' would be great if loc could be a string, numbers in microsteps, or
        numbers in mm'''
        self.reader.move_reader(loc)

    def moveImager_relative(self, loc):
        '''currently loc is in steps, loc is a [x, y, z] list'''
        x_now, y_now, z_now, fw_now = self.reader.get_position() # x, y, z, fw
        xconv = 75000
        yconv = 23000
        zconv = 100000
        # convert to mm!
        target = [loc[0] + x_now, loc[1] + y_now, loc[2] + z_now, loc[3]]
        target = [target[0]*xconv, target[1]*yconv, target[2]*zconv, target[3]*1]
        self.reader.move_reader(target)

    def moveFilterWheel(self, color, blocking=True):
        self.reader.rotate_filter_wheel(color, block=blocking)

    def turnOnLED(self, color, intensity=0.1):
        # "accept" both floating point numbers and integers
        if intensity < 1:
            intensity_percent = intensity * 100
        elif intensity == 1:
            intensity_percent = 100
        else:
            intensity_percent = intensity
        self.reader.illumination_on(color, intensity_percent)

    def switchToLED(self, color, intensity=0.1):
        # "accept" both floating point numbers and integers
        if intensity < 1:
            intensity_percent = intensity * 100
        elif intensity == 1:
            intensity_percent = 100
        else:
            intensity_percent = intensity
        self.reader.illumination_offmult()
        self.reader.illumination_on(color, intensity_percent)

    def turnOffLED(self, color):
        self.reader.illumination_off(color, use_fast_api=True,
            go_home=False)

    def turnOffLEDs(self,):
        self.reader.illumination_offmult()

    def snap_single(self, **kwargs):
        return self.reader.capture_image(**kwargs)

    def setExposureTimeMicroseconds(self, exp_time_microseconds):
        self.reader.set_exposure(exp_time_microseconds)

    def getExposureTime(self):
        return self.reader.get_exposure()

    def setdPCRTemp(self, num, temp):
        pass

    def getdPCRTemp(self, num, temp):
        pass

    def captureImage(self):
        return self.reader.camcontroller.snap_single()

    def open_tray(self, mode):
        # see reader.py open tray for modes
        self.reader.open_tray(mode)

    def close_tray(self, mode):
        self.reader.close_tray(mode)

    def raise_heater(self, heater):
        self.reader.raise_heater(heater)

    def lower_heater(self, heater):
        self.reader.lower_heater(heater)

    # maybe these should go away, deprecated
    def close_CD(self):
        self.reader.close_tray_only()

    def open_CD(self):
        self.reader.open_tray_only()

    def close_AB(self):
        self.reader.close_AB_only()
    def open_AB(self):
        self.reader.open_AB_only()

    def close(self):
        self.reader.close()
        self.upper_gantry.close()
        # close peltier
class Dummy_Camera(object):
    def __init__(self):
        self.camera = None

class Dummy_Reader(object):
    def __init__(self):
        self.camcontroller = Dummy_Camera()

class Dummy_Interface(object):
    def __init__(self,):
        self.reader = Dummy_Reader()

    def illumination_offmult(self):
        pass

    def get_pos_reader_submodule(self, submodule):
        return 0

    def turnOffLED(self,color):
        pass

if __name__ == "__main__":
    import time
    ci = Connection_Interface()
    # ci.reader.illumination_only_on('FAM', intensity_percent=10)
    # time.sleep(1)
    # ci.reader.illumination_offmult()
    # time.sleep(3)
    print('ILLUMINATION SHOULD BE OFF')
    # img = ci.captureImage()
    # time.sleep(3)
    for color in ['ALEXA405', 'FAM', 'HEX', 'ATTO', 'CY5', 'CY55']:

        ci.reader.illumination_off(color)
