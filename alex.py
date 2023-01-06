from logger import Logger
from utils import delay
from coordinate import coordinates

def generate_droplets(upper_gantry, tray, row, dg8_id, eject_when_done=True):
    dz = coordinates['deck_plate']['dg8']['dz']
    assert type(dg8_id) == str
    dg8_ids = ['1000', '0100', '0010', '0001']
    assert dg8_id in dg8_ids
    channel_ids = ['100', '010', '001']
    # Create target name.
    target = 'dg8_{0}_'.format(dg8_id)
    # Pickup 200 uL tips.
    upper_gantry.tip_pickup(tray, row, use_drip_plate=False, pipette_tip_type=200, slow_z=True)
    # Aspirate 100 uL from Reagent Cartridge Row.
    upper_gantry.move_pipettor('reagent_cartridge_tray2_row4', use_drip_plate=False, pipette_tip_type=200)
    upper_gantry.aspirate(100)
    # Dispense 100 uL in the dg8 chip 100 channel
    upper_gantry.move_pipettor(target + '100', use_drip_plate=False, pipette_tip_type=200)
    upper_gantry.dispense(100)
    # Aspirate 24 uL from Reagent Cartridge Row.
    upper_gantry.move_pipettor('reagent_cartridge_tray2_row5', use_drip_plate=False, pipette_tip_type=200)
    upper_gantry.aspirate(24)
    # Dispense 24 uL in the dg8 chip 010 channel
    upper_gantry.move_pipettor(target + '010', use_drip_plate=False, pipette_tip_type=200)
    upper_gantry.dispense(24)
    # Wait.
    # Aspirate 40 uL from the dg8 001 channel.
    upper_gantry.move_pipettor(target + '001', use_drip_plate=False, pipette_tip_type=200)
    upper_gantry.aspirate(40)
    # Dispense on Tray CD Location D.
    #upper_gantry.move_pipettor([-350,-1773000,-1094000,0])
    #upper_gantry.dispense(40)

    if eject_when_done:
        upper_gantry.tip_eject(tray, row)

def test_sealed_translume_chip(upper_gantry):
    upper_gantry.tip_pickup('C', 12)
    upper_gantry.move_pipettor('reagent_cartridge_tray2_row1', use_drip_plate=False, pipette_tip_type=50)
    upper_gantry.aspirate(25)
    upper_gantry.move_pipettor('tray_out_location_tray2', use_drip_plate=False, pipette_tip_type=50)
    upper_gantry.dispense(30)
    upper_gantry.tip_eject('C', 12)

def show_chip_and_lid_transfer(upper_gantry):
    upper_gantry.move_chip(4, 'microwells', 'D')
    upper_gantry.move_lid(4, 'D')
    upper_gantry.turn_on_suction_cups()
    upper_gantry.move_pipettor([-434700,-1437000,0,-1198000])
    upper_gantry.move_pipettor([-434700,-970000,-265000,-1198000])
    upper_gantry.turn_off_suction_cups()
    upper_gantry.move_relative('up', 300000, 'fast')

def get_monitored_temperature(input_filename, output_filename):
    i = 0
    ofile = open(output_filename, 'w')
    with open(input_filename) as ifile:
        lines = ifile.readlines()
        for line in lines:
            if 'Message' in line:
                line = line.split(' ')
                value = line[-1].replace('\n','')
                try:
                    temp = float(value)
                    ofile.write("{0},{1}\n".format(i,temp))
                    i = i + 1
                except:
                    continue
        ofile.close()

def thermocycling_test_AAA8_55_Peltier(reader, peltier, check_in_time=10):
    # Setup the logger.
    logger = Logger(__file__, __name__)
    logger.log("LOG-START", "Running Alex's Thermocycler protocol with Heater D only (AAA8_1-40_Peltier.toml).")
    # Load the chip.
    logger.log("MESSAGE", "Chip has been loaded.")
    # Close the tray.
    #reader.close_tray('CD')
    logger.log("MESSAGE", "Tray CD has been closed.")
    # Lower the heater.
    #reader.lower_heater('D')
    logger.log("MESSAGE", "Heater D has been lowered.")
    # Set the temperature to 92 degC.
    peltier.change_temperature(95, block=False)
    # Handle errors....
    peltier.monitor_device(10*60, check_in_every_N_seconds=check_in_time)
    print("Starting cycles now!")
    # Perform this test N times.
    N = 55
    for i in range(N):
        logger.log('MESSAGE', "Starting cycle number {0} for Alex's protocol".format(i+1))
        peltier.change_temperature(92, block=False)
        # Handle errors....
        peltier.monitor_device(2*40, check_in_every_N_seconds=check_in_time)
        peltier.change_temperature(60, block=False)
        # Handle errors....
        peltier.monitor_device(2*60, check_in_every_N_seconds=check_in_time)
    # Change temp to 30 and hold for 2 minutes then go to 4!!!
    peltier.change_temperature(30, block=False)
    peltier.monitor_device(2*60, check_in_every_N_seconds=check_in_time)

class Alex():
    def __init__(self):
        a = 1

    def AAA8_1_10(self, meerstetter, h1, h2):
        """
        This is a thermocycling protocol with 10 cycles and 
        """
        # Setup the logger.
        logger = Logger(__file__, __name__)
        logger.log("LOG-START", "Running Alex's Thermocycler protocol (AAA8_1_10) with {0} and {1}.".format(h1, h2))
        
        # Set the temperature to 92 degC.
        meerstetter.change_temperature(h1, 95, block=False)
        meerstetter.change_temperature(h2, 98, block=False)
        # Handle errors....
        meerstetter.monitor_devices_2(h1, h2, 1*60, check_in_every_N_seconds=10)
        # Perform this test N times.
        meerstetter.thermocycle_2(h1=h1, h2=h2, number_of_cycles=10, high_T=92, high_T_time=40, high_T_time_units='seconds', low_T=59, low_T_time=60, low_T_time_units='seconds')
        # Change temp to 30 and hold for 2 minutes then go to 4!!!
        meerstetter.change_temperature(h1, 30, block=False)
        meerstetter.change_temperature(h2, 30, block=False)
        meerstetter.monitor_devices_2(h1, h2, 2*60, check_in_every_N_seconds=10)
        logger.log('LOG-END', "Alex's Thermocycling protocol (AAA8_1_10) is complete on {0} and {1}".format(h1, h1))

    def AAA8_1_55(self, meerstetter, h1, h2):
        """
        This is a thermocycling protocol with 55 cycles and 
        """
        heater_d = {
            95: 98,
            60: 58,
            92: 94,
            30: 28
            }
        # Setup the logger.
        logger = Logger(__file__, __name__)
        logger.log("LOG-START", "Running Alex's Thermocycler protocol (AAA8_1_55) with {0}.".format(h1))
        # Set the temperature to 92 degC.
        meerstetter.change_temperature(h1, 95, block=False)
        meerstetter.change_temperature(h2, heater_d[95], block=False)
        # Handle errors....
        meerstetter.monitor_devices(h1, h2, 10*60, check_in_every_N_seconds=10)
        # Perform this test N times.
        meerstetter.thermocycle_2(h1=h1, h2=h2, number_of_cycles=55, high_T=92, high_T_time=40, high_T_time_units='seconds', low_T=60, low_T_time=60, low_T_time_units='seconds', high_T_2=heater_d[92], low_T_2=heater_d[60])
        # Change temp to 30 and hold for 2 minutes then go to 4!!!
        meerstetter.change_temperature(h1, 30, block=False)
        meerstetter.change_temperature(h2, heater_d[30], block=False)
        meerstetter.monitor_devices_2(h1, h2, 2*60, check_in_every_N_seconds=10)
        logger.log('LOG-END', "Alex's Thermocycling protocol (AAA8_1_55) is complete on {0}".format(h1))

    def AAA8_1_40(self, meerstetter, h1, h2):
        """
        This is a thermocycling protocol with 55 cycles and 
        """
        # Setup the logger.
        logger = Logger(__file__, __name__)
        logger.log("LOG-START", "Running Alex's Thermocycler protocol (AAA8_1_40) with {0}.".format(h1))
        # Set the temperature to 92 degC.
        meerstetter.change_temperature(h1, 84, block=False)
        meerstetter.change_temperature(h2, 84, block=False)
        # Handle errors....
        meerstetter.monitor_devices_2(h1, h2, 3*60, check_in_every_N_seconds=10)
        # Perform this test N times.
        meerstetter.thermocycle_2(h1=h1, h2=h2, number_of_cycles=40, high_T=84, high_T_time=40, high_T_time_units='seconds', low_T=55, low_T_time=80, low_T_time_units='seconds', high_T_2=84, low_T_2=55)
        # Change temp to 30 and hold for 2 minutes then go to 4!!!
        meerstetter.change_temperature(h1, 30, block=False)
        meerstetter.change_temperature(h2, 30, block=False)
        logger.log('LOG-END', "Alex's Thermocycling protocol (AAA8_1_40) is complete on {0}".format(h1))

    def AAA8_1_45(self, meerstetter, h1, h2):
        """
        This is a thermocycling protocol with 45 cycles and 
        """
        # Setup the logger.
        logger = Logger(__file__, __name__)
        logger.log("LOG-START", "Running Alex's Thermocycler protocol (AAA8_1_45) with {0}.".format(h1))
        # Set the temperature to 92 degC.
        meerstetter.change_temperature(h1, 84, block=False)
        meerstetter.change_temperature(h2, 84, block=False)
        # Handle errors....
        meerstetter.monitor_devices_2(h1, h2, 3*60, check_in_every_N_seconds=10)
        # Perform this test N times.
        meerstetter.thermocycle_2(h1=h1, h2=h2, number_of_cycles=45, high_T=84, high_T_time=30, high_T_time_units='seconds', low_T=55, low_T_time=60, low_T_time_units='seconds', high_T_2=84, low_T_2=55)
        #meerstetter.change_temperature(h1, 88, block=False)
        #meerstetter.change_temperature(h2, 92, block=False)
        #meerstetter.monitor_devices_2(h1, h2, 40, check_in_every_N_seconds=10)
        # Change temp to 30 and hold for 2 minutes then go to 4!!!
        #meerstetter.change_temperature(h1, 88, block=False)
        #meerstetter.change_temperature(h2, 92, block=False)
        #meerstetter.monitor_devices_2(h1, h2, 2*60, check_in_every_N_seconds=10)
        meerstetter.change_temperature(h1, 30, block=False)
        meerstetter.change_temperature(h2, 30, block=False)
        meerstetter.monitor_devices_2(h1, h2, 2*60, check_in_every_N_seconds=10)
        logger.log('LOG-END', "Alex's Thermocycling protocol (AAA8_1_40) is complete on {0}".format(h1))

    def AAA8_1_22(self, meerstetter, h1, h2):
        """
        This is a thermocycling protocol with 55 cycles and 
        """
        # Setup the logger.
        logger = Logger(__file__, __name__)
        logger.log("LOG-START", "Running Alex's Thermocycler protocol (AAA8_1_40) with {0}.".format(h1))
        # Set the temperature to 92 degC.
        meerstetter.change_temperature(h1, 84, block=False)
        meerstetter.change_temperature(h2, 84, block=False)
        # Handle errors....
        meerstetter.monitor_devices_2(h1, h2, 3*60, check_in_every_N_seconds=10)
        # Perform this test N times.
        meerstetter.thermocycle_2(h1=h1, h2=h2, number_of_cycles=22, high_T=84, high_T_time=30, high_T_time_units='seconds', low_T=50, low_T_time=40, low_T_time_units='seconds', high_T_2=84, low_T_2=50)
        meerstetter.change_temperature(h1, 84, block=False)
        meerstetter.change_temperature(h2, 84, block=False)
        meerstetter.monitor_devices_2(h1, h2, 30, check_in_every_N_seconds=10)
        # Change temp to 30 and hold for 2 minutes then go to 4!!!
        meerstetter.change_temperature(h1, 84, block=False)
        meerstetter.change_temperature(h2, 84, block=False)
        meerstetter.monitor_devices_2(h1, h2, 2*60, check_in_every_N_seconds=10)
        meerstetter.change_temperature(h1, 30, block=False)
        meerstetter.change_temperature(h2, 30, block=False)
        meerstetter.monitor_devices_2(h1, h2, 2*60, check_in_every_N_seconds=10)
        logger.log('LOG-END', "Alex's Thermocycling protocol (AAA8_1_40) is complete on {0}".format(h1))

    def AAA8_1_5(self, meerstetter, h1, h2):
        """
        This is a thermocycling protocol with 55 cycles and 
        """
        heater_d = {
            95: 95,
            60: 60,
            92: 92,
            30: 30
            }
        # Setu
        # Setup the logger.
        logger = Logger(__file__, __name__)
        logger.log("LOG-START", "Running Alex's Thermocycler protocol (AAA8_1_1) with {0}.".format(h1))
        # Set the temperature to 92 degC.
        meerstetter.change_temperature(h1, 84, block=False)
        meerstetter.change_temperature(h2, 84, block=False)
        # Handle errors....
        meerstetter.monitor_devices_2(h1, h2, 1*30, check_in_every_N_seconds=10)
        # Perform this test N times.
        meerstetter.thermocycle_2(h1=h1, h2=h2, number_of_cycles=5, high_T=84, high_T_time=30, high_T_time_units='seconds', low_T=55, low_T_time=40, low_T_time_units='seconds', high_T_2=84, low_T_2=55)
        meerstetter.change_temperature(h1, 84, block=False)
        meerstetter.change_temperature(h2, 84, block=False)
        meerstetter.monitor_devices_2(h1, h2, 30, check_in_every_N_seconds=10)
        # Change temp to 30 and hold for 2 minutes then go to 4!!!
        meerstetter.change_temperature(h1, 30, block=False)
        meerstetter.change_temperature(h2, 30, block=False)
        meerstetter.monitor_devices_2(h1, h2, 2*60, check_in_every_N_seconds=10)
        logger.log('LOG-END', "Alex's Thermocycling protocol (AAA8_1_1) is complete on {0}".format(h1))


    def get_monitored_temperatures_2(self, address_1, address_2, input_filename, output_filename_1, output_filename_2):
        i = 0
        ofile = open(output_filename_1, 'w')
        with open(input_filename) as ifile:
            lines = ifile.readlines()
            for line in lines:
                if 'Message' in line:
                    line = line.split(' ')
                    print(line)
                    try:
                        if int(line[4]) == address_1:
                            value = line[-1].replace('\n','')
                            try:
                                temp = float(value)
                                ofile.write("{0},{1}\n".format(i,temp))
                                i = i + 1
                            except:
                                continue
                    except:
                        continue
            ofile.close()
        i = 0
        ofile = open(output_filename_2, 'w')
        with open(input_filename) as ifile:
            lines = ifile.readlines()
            for line in lines:
                if 'Message' in line:
                    line = line.split(' ')
                    print(line)
                    try:
                        if int(line[4]) == address_2:
                            value = line[-1].replace('\n','')
                            try:
                                temp = float(value)
                                ofile.write("{0},{1}\n".format(i,temp))
                                i = i + 1
                            except:
                                continue
                    except:
                        continue
            ofile.close()