'''
'''
import os.path as osp
import time

class Seyonic(object):
    ''' This class interfaces with the Seyonic Pipettor. The Pipettor consists
    of a controller and a pipettor. Commands are sent via ethernet to a
    RaspberryPi inside the controller, which routes the commands to the
    specified hardware. The pipettors should all have the default
    INPUTS:
        ip_address: string. address of controller unit. Default 10.0.0.178.
        port: int. TCP/IP port to be used. Default 10001.
        controller_address: int. address of controller. Default 208 (dec), 0xD0
        pipettor_address: int. address of pipettor. Default 16 (dec), 0x10
    '''
    def __init__(self, ip_address='10.0.0.178', port=10001, controller_address=208, pipettor_address=16):
        # SET/LOAD PARAMETERS
            # set max timeout for polling action status
        print("WARNING (seyonic_dumby, __init__): using seyonic_dumby for testing, change to seyonic in upper gantry for real tests")
        self.max_timeout = 10 # sec
            # delay time after setting pressure, before triggering for pressure
            # equalization
        self.pressure_delay = 0.3 # this should be loaded from config file
        # initialize pipettor connection
        #self.client = DispenserServer.ConnectClient()
        #self.client.EventsAndExceptionsActive = True
        #self.client.OpenTcp(ip_address, port)
        self.aspirate_volumes = [0] * 8
        self.dispense_volumes = [0] * 8
        self.cntrl_addr = controller_address
        self.pip_addr = pipettor_address
        self.get_aspirate_volumes()
        self.get_dispense_volumes()

    def _calculate_and_set_resvol(self,):
        return None

    def _calc_pressure(self,):
        return None

    def _poll_until_complete(self):
        return None

    def set_pressure(self, pressure):
        return None

    def get_actual_aspirate_volume(self):
        return None

    def get_actual_dispense_volume(self):
        return None

    def set_aspirate_volumes(self, volumes):
        return None

    def set_dispense_volumes(self, volumes):
        return None

    def get_aspirate_volumes(self):
        return None

    def get_dispense_volumes(self):
        return None

    def aspirate(self, pressure=None, debug=True):
        return None

    def dispense(self, pressure=None, debug=True):
        return None

    def close(self):
        return None
