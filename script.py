'''
'''

from logger import Logger
from utils import delay
from timer import Timer

from coordinate import coordinates

import datetime

class Script():
    # Public variables.
    # Private variables.
    # Privates constants.
    # Constructor.
    def __init__(self):
        a = 1

    # Droplet Generation Method.
    def droplet_generation(self, upper_gantry, tray_with_200uL_tips, row_with_200uL_tips, dg8_id, heater='D', droplet_type='standard'):
        dz = coordinates['deck_plate']['dg8']['dz']
        assert type(dg8_id) == str
        dg8_ids = ['1000', '0100', '0010', '0001']
        assert dg8_id in dg8_ids
        channel_ids = ['100', '010', '001']
        # Create target name.
        target = 'dg8_{0}_'.format(dg8_id)
        # Pickup 200 uL tips.
        upper_gantry.tip_pickup(tray_with_200uL_tips, row_with_200uL_tips, pipette_tip_type=200)
        # Aspirate 100 uL from Reagent Cartridge Row.
        upper_gantry.move_pipettor('reagent_cartridge_tray4_row4', use_drip_plate=False, pipette_tip_type=200)
        upper_gantry.aspirate(100)
        # Dispense 100 uL in the dg8 chip 100 channel
        upper_gantry.move_pipettor(target + '100', pipette_tip_type=200)
        upper_gantry.dispense(100)
        # Eject the tips to get 50 uL tips.
        upper_gantry.tip_eject('tip_transfer_tray', 5)
        upper_gantry.tip_pickup('A', 5)
        # Aspirate 24 uL from Reagent Cartridge Row.
        upper_gantry.move_pipettor('reagent_cartridge_tray4_row5', use_drip_plate=False, pipette_tip_type=50)
        upper_gantry.aspirate(24)
        # Dispense 24 uL in the dg8 chip 010 channel
        upper_gantry.move_pipettor(target + '010', pipette_tip_type=50)
        upper_gantry.dispense(24)
        # Eject tips.
        upper_gantry.tip_eject('A', 5)
        upper_gantry.move_pipettor(target + '001', pipette_tip_type=1000)
        upper_gantry.move_relative('down', dz)
        # Generate the droplets.
        upper_gantry.generate_droplets(droplet_type)
        # Aspirate 40 uL from the dg8 001 channel.
        #upper_gantry.tip_pickup('A', 5)
        #upper_gantry.move_pipettor(target + '001', pipette_tip_type=200)
        #upper_gantry.aspirate(40)
        # Dispense on Tray CD Location D.
        #upper_gantry.move_pipettor('tray_out_location_tray1')
        #upper_gantry.dispense(40)
        #upper_gantry.tip_eject('A', 5)

    def droplet_generation_demo(self, upper_gantry, tray_with_200uL_tips, row_with_200uL_tips, dg8_id, heater='D', droplet_type='standard'):
        dz = coordinates['deck_plate']['dg8']['dz']
        assert type(dg8_id) == str
        dg8_ids = ['1000', '0100', '0010', '0001']
        assert dg8_id in dg8_ids
        channel_ids = ['100', '010', '001']
        # Create target name.
        target = 'dg8_{0}_'.format(dg8_id)
        # Pickup 200 uL tips.
        upper_gantry.tip_pickup('A', 5)
        # Aspirate 100 uL from Reagent Cartridge Row.
        upper_gantry.move_pipettor('reagent_cartridge_tray4_row4', use_drip_plate=False, pipette_tip_type=50)
        upper_gantry.aspirate(40)
        # Dispense 100 uL in the dg8 chip 100 channel
        upper_gantry.move_pipettor(target + '100', pipette_tip_type=50)
        upper_gantry.dispense(45)
        # Eject the tips to get 50 uL tips.
        # Aspirate 24 uL from Reagent Cartridge Row.
        upper_gantry.move_pipettor('reagent_cartridge_tray4_row5', use_drip_plate=False, pipette_tip_type=50)
        upper_gantry.aspirate(24)
        # Dispense 24 uL in the dg8 chip 010 channel
        upper_gantry.move_pipettor(target + '010', pipette_tip_type=50)
        upper_gantry.dispense(24)
        # Eject tips.
        upper_gantry.tip_eject('A', 5)
        upper_gantry.move_pipettor(target + '001', pipette_tip_type=1000, use_drip_plate=False)
        upper_gantry.move_relative('down', dz, velocity='fast')
        # Generate the droplets.
        upper_gantry.generate_droplets(droplet_type)
        # Aspirate 40 uL from the dg8 001 channel.
        upper_gantry.tip_pickup('A', 5)
        upper_gantry.move_pipettor(target + '001', pipette_tip_type=200)
        upper_gantry.aspirate(40)
        # Dispense on Tray CD Location D.
        upper_gantry.move_pipettor('tray_out_location_tray1')
        upper_gantry.dispense(40)
        upper_gantry.tip_eject('A', 5)


    # Pre-Amp Method.
    def pre_amp(self, upper_gantry):
        # Get the time and day.
        today = datetime.datetime.now()
        day = today.day
        month = today.month
        year = today.year
        hour = today.hour
        minute = today.minute
        second = today.second
        if hour > 11:
            am_or_pm = 'pm'
            if hour > 12:
                hour = hour - 12
        else:
            am_or_pm = 'am'
        # Setup the logger.
        logger = Logger(__file__, __name__, 'gretchen_pre_amp_workflow_day_{0}_{1}_{2}_time_{3}_{4}_{5}.txt'.format(month, day, year, hour, minute, second))
        logger.log('LOG-START', "Starting Gretchen's Pre-Amp Workflow on {0}/{1}/{2} at {3}:{4}:{5} {6}".format(month, day, year, hour, minute, second, am_or_pm))
        # Begin with eluted cfDNA in the Mag Separator.
        # Pickup 50 microliter tips for Batch A (re-use from elution step)
        upper_gantry.tip_pickup('C', 12)
        # Move to Reagent Cartridge Row X with water.
        upper_gantry.move_pipettor('reagent_cartridge_tray2_row1', use_drip_plate=False)
        # Aspirate 15 microliters of water.
        upper_gantry.aspirate(15)
        # Move to the Pre-Amp Thermocycler Row 1.
        upper_gantry.move_pipettor('pcr_thermocycler_row1', use_drip_plate=False)
        # Dispense 15 microliters of water in Pre-Amp Thermocycler Row 1.
        upper_gantry.dispense(20)
        # Move to the Mag Separator Row 1.
        upper_gantry.move_pipettor('mag_separator_row1', use_drip_plate=False)
        # Aspirate 10 microliters of cfDNA from the Mag Separator Row 1.
        upper_gantry.aspirate(10)
        # Move to the Pre-Amp Thermocycler Row 1.
        upper_gantry.move_pipettor('pcr_thermocycler_row1', use_drip_plate=False)
        # Dispense 10 microliters of cfDNA into Pre-Amp Thermocycler Row 1.
        upper_gantry.dispense(15)
        # Pipette mix 3-5 times in the Pre-Amp Thermocycler Row 1.
        #upper_gantry.mix(aspirate_vol=25, dispense_vol=30, cycles=3)
        for i in range(3):
            upper_gantry.aspirate(25, pipette_tip_type=50)
            upper_gantry.dispense(30)
        # Move to the Tip Transfer Tray and Eject Tips.
        upper_gantry.tip_eject('tip_transfer_tray', 1)
        # Move to tips used for EOTH residual removal and pick them up.
        upper_gantry.tip_pickup('tip_transfer_tray', 2)
        # Move to Reagent Cartridge Row X with mineral oil.
        upper_gantry.move_pipettor('reagent_cartridge_tray2_row2', use_drip_plate=False)
        # Aspirate 25 microliters of mineral oil.
        upper_gantry.aspirate(25)
        # Move to the Pre-Amp Thermocycler Row 1.
        upper_gantry.move_pipettor('pcr_thermocycler_row1', use_drip_plate=False)
        # Dispense 25 microliters of mineral oil slowly into Pre-Amp Thermocycler Row 1.
        upper_gantry.dispense(30)
        # Move to the Tip Transfer Tray Row X and Eject Tips
        upper_gantry.tip_eject('tip_transfer_tray', 2)
        # Thermocycle for 5-7 cycles.
        # Move to the Tip Transfer Tray Row X and Pickup Tips.
        upper_gantry.tip_pickup('C', 11)
        # Move to the Reagent Cartridge Row X.
        upper_gantry.move_pipettor('reagent_cartridge_tray2_row4', use_drip_plate=False)
        # Aspirate 25 microliters of water.
        upper_gantry.aspirate(25)
        # Move to Pre-Amp Thermocycler Row 1.
        upper_gantry.move_pipettor('pcr_thermocycler_row1', use_drip_plate=False)
        # Dispense 25 microliters of water in Pre-Amp Thermocycler Row 1.
        upper_gantry.dispense(30)
        upper_gantry.move_pipettor('home')
        logger.log('LOG-END', "Ended Gretchen's Pre-Amp Workflow on {0}/{1}/{2} at {3}:{4}:{5} {6}".format(month, day, year, hour, minute, second, am_or_pm))

    # Waste Dispense Script.
    def waste_dispense(self, upper_gantry, dispense_vol, target, use_drip_plate=True, slow_z=False, use_z=True, relative_moves=[0,0,0,0], pipette_tip_type=None):
        logger = Logger(__file__, '{0}.{1}'.format(__name__, self.waste_dispense.__name__))
        logger.log('MESSAGE', "Dispensing {0} uL of waste to {1}".format(dispense_vol, target))
        timer = Timer(logger)
        timer.start(__file__, self.waste_dispense.__name__)
        # Move to the target location.
        upper_gantry.move_pipettor(target, use_drip_plate=use_drip_plate, slow_z=slow_z, use_z=use_z, relative_moves=relative_moves, pipette_tip_type=pipette_tip_type)
        # Dispense.
        upper_gantry.dispense(dispense_vol)
        timer.stop(__file__, self.waste_dispense.__name__)

    # Transfer Plasma Method.
    def transfer_plasma(self, upper_gantry, full_protocol=True, dz=350000):
        logger = Logger(__file__, __name__)
        timer = Timer(logger)
        timer.start(__file__, self.transfer_plasma.__name__)
        msg = """
        **********************************************************************************************
        Extraction: Transfer Plasma
        **********************************************************************************************
        """
        logger.log('HEADER', msg)
        trays = {
            1: ['A', 4],
            2: ['B', 3],
            3: ['C', 2],
            4: ['D', 1]
            }
        if full_protocol:
            runs = 4
        else:
            runs = 1
        for tray in range(1,runs+1):
            # Pickup tips.
            logger.log('MESSAGE', "Transfer Plasma from Sample Loading Rack {0}".format(trays[tray][0]))
            upper_gantry.tip_pickup(trays[tray][0], 1)
            for i in range(4):
                msg = "Transfering 1 mL of Plasma from the Sample Loading Rack {0} to the Heater/Shaker Row {1}".format(trays[tray][0], tray)
                timer.log_current_elapsed_time(__file__, self.transfer_plasma.__name__, msg)
                # Move to the Sample Loading Rack.
                upper_gantry.move_pipettor('sample_loading_tray{0}'.format(trays[tray][1]), use_drip_plate=False, pipette_tip_type=1000)
                # Aspirate 1 mL of Plasma.
                upper_gantry.aspirate(1000, pipette_tip_type=1000)
                # Move to Heater/Shaker.
                upper_gantry.move_pipettor('heater_shaker_row{0}'.format(tray), use_drip_plate=False, relative_moves=[0,0,dz,0], pipette_tip_type=1000)
                # Move relative up for the dispense.
                #upper_gantry.move_relative('down', int(int(coordinates['deck_plate']['heater_shaker'][tray-1][2]) + 100000 * tray), velocity='fast')
                # Dispense 1 mL Plasma. (20% rule from Seyonic)
                upper_gantry.dispense(1000)
                delay(2, 'seconds')
                upper_gantry.dispense(50)
                # Residual dispense
                #upper_gantry.move_relative('up', 100000, velocity='fast')
                #upper_gantry.dispense(100)
            # Tip eject.
            if full_protocol:
                upper_gantry.tip_eject(trays[tray][0], 1)
        timer.stop(__file__, self.transfer_plasma.__name__, time_units='minutes')

    # Binding Method.
    def binding(self, upper_gantry, full_protocol=True, rpm=1300, dz=350000):
        logger = Logger(__file__, __name__)
        timer = Timer(logger)
        timer.start(__file__, self.binding.__name__)
        msg = """
        **********************************************************************************************
        Extraction: Binding
        - Proteinase K (Alone with the Plasma), 40 uL per 1 mL Plasma <- Lysis Step
        - Rest of Binding Solution (935 uL per 1 mL Plasma Proteinase K)
            - Lysis Buffer 
            - Binding Buffer
            - Beads (maybe add last)
        **********************************************************************************************
        """
        logger.log('HEADER', msg)
        trays = {
            1: ['A', 4],
            2: ['B', 3],
            3: ['C', 2],
            4: ['D', 1]
            }
        if full_protocol:
            runs = 4
        else:
            runs = 1
        for tray in range(1,runs+1):
            msg = "Binding: Transfer 160 uL of Proteinase K for 4 mL of Plasma"
            # Pickup tips from the Tip Transfer Tray (Reuse).
            if full_protocol:
                upper_gantry.tip_pickup(trays[tray][0], 1)
            # Move to the Reagent Cartridge for Proteinase K. 
            upper_gantry.move_pipettor('reagent_cartridge_tray{0}_row4'.format(trays[tray][1]), pipette_tip_type=1000, use_drip_plate=False)
            # Aspirate 40 uL Proteinase K per mL of Plasma (160 uL total).
            upper_gantry.aspirate(160, pipette_tip_type=1000)
            # Move to the Heater/Shaker Row.
            #dz = 300000
            upper_gantry.move_pipettor('heater_shaker_row{0}'.format(tray), pipette_tip_type=1000, use_z=True, use_drip_plate=False)
            #upper_gantry.move_relative('down', int(int(coordinates['deck_plate']['heater_shaker'][tray-1][2]) + 300000), velocity='fast')
            # Dispense.
            upper_gantry.dispense(200)
            for i in range(1,5):
                if i == 1:
                    row = 1
                elif i == 2:
                    row = 2
                elif i == 3:
                    row = 11
                elif i == 4:
                    row = 12
                # Move to the Reagent Cartridge for the rest of the Binding Solution.
                upper_gantry.move_pipettor('reagent_cartridge_tray{0}_row{1}'.format(trays[tray][1], row), pipette_tip_type=1000, use_drip_plate=False)
                # Mix 935 uL 2 times.
                logger.log('WARNING', "Need to stop shaking")
                #upper_gantry.stop_shake()
                upper_gantry.aspirate(935, pipette_tip_type=1000)
                upper_gantry.dispense(935)
                #upper_gantry.aspirate(935, pipette_tip_type=1000)
                #upper_gantry.dispense(935)
                # Aspirate 935 uL of Binidng Solution.
                upper_gantry.aspirate(935, pipette_tip_type=1000)
                # Move to Heater/Shaker Row.
                upper_gantry.move_pipettor('heater_shaker_row{0}'.format(tray), pipette_tip_type=1000, use_z=True, use_drip_plate=False, relative_moves=[0,0,dz,0])
                #upper_gantry.move_relative('down', int(int(coordinates['deck_plate']['heater_shaker'][tray-1][2]) + 300000), velocity='fast')
                # Dispense Binding Solution.
                upper_gantry.dispense(935)
                # Wait a few seconds for the liquid to fall down the tips.
                delay(3, 'seconds')
                upper_gantry.dispense(100)
                # Mix 2 times.
                #upper_gantry.aspirate(1000, pipette_tip_type=1000)
                #upper_gantry.dispense(1010)
                #upper_gantry.aspirate(1000, pipette_tip_type=1000)
                #upper_gantry.dispense(1010)
                # Shake the Heater/Shaker.
                #upper_gantry.shake(rpm=rpm, shake_time=15, time_units='minutes')
                logger.log('WARNING', "Shaking needs to be on")
                #upper_gantry.shake(rpm)
            # Wait a few seconds for the liquid to fall down the tips.
            delay(3, 'seconds')
            upper_gantry.dispense(100)
            # Tip Eject.
            if full_protocol:
                upper_gantry.tip_eject(trays[tray][0], 1)
            # Bind for 15 minutes after 4 935 uL added.
            logger.log('WARNING', "15 minute delay removed.")
            #delay(15, 'minutes')
            # Turn off heat.
            logger.log('WARNING', "Turn off Heater/Shaker heat.")
            # Keep Shaking.
            logger.log('WARNING', "Keep shaking.")
        timer.stop(__file__, self.binding.__name__, time_units='minutes')

    # Pooling Method.
    def pooling(self, upper_gantry, full_protocol=True):
        logger = Logger(__file__, __name__)
        timer = Timer(logger)
        timer.start(__file__, self.pooling.__name__)
        msg = """
        **********************************************************************************************
        Extraction: Pooling
        **********************************************************************************************
        """
        logger.log('HEADER', msg)
        trays = {
            1: ['A', 4],
            2: ['B', 3],
            3: ['C', 2],
            4: ['D', 1]
            }
        if full_protocol:
            runs = 4
        else:
            runs = 1
        # Engage Magnet.
        upper_gantry.engage_magnet()
        for tray in range(1,runs+1):
            # Pickup tips.
            if full_protocol:
                upper_gantry.tip_pickup(trays[tray][0], 1)
            for round in range(1,10):
                # Move to the Heater/Shaker Row.
                upper_gantry.move_pipettor('heater_shaker_row{0}'.format(tray), pipette_tip_type=1000, use_drip_plate=False)
                # Aspirate 1 mL (8 mL in total but last transfer is less than 1 mL).
                volume = 860
                final_pre_dispense_bead_volume = 80
                number_of_dispenses = 5
                upper_gantry.aspirate(volume, pipette_tip_type=1000)
                # Move to the Sample Loading Rack for Magnet Pre-Dispense.
                self.pre_dispense(upper_gantry, trays[tray][1], pipette_tip_type=1000, number_of_dispenses=number_of_dispenses)
                # Move to the Mag Separator Row.
                upper_gantry.move_pipettor('mag_separator_row{0}'.format(tray), use_drip_plate=False, pipette_tip_type=1000, relative_moves=[0,0,20000,0])
                # Mix.
                upper_gantry.dispense(final_pre_dispense_bead_volume)
                delay(3, 'seconds')
                # Dispense the last 50 uL.
                upper_gantry.dispense(25, pressure='low')
            # Wait for Beads to Bind.
            delay(20, 'seconds')
            # Resuspend Beads.
            logger.log('MESSAGE', "Resuspend Beads left in the Mag Separator Row {0}".format(tray))
            # Aspirate from the Mag Separator.
            upper_gantry.aspirate(600, pressure='low', pipette_tip_type=1000)
            # Move to the Heater/Shaker Row.
            upper_gantry.move_pipettor('heater_shaker_row{0}'.format(tray), pipette_tip_type=1000, use_drip_plate=False, relative_moves=[-6000,0,0,0])
            # Dispense.
            upper_gantry.dispense(600)
            upper_gantry.move_relative('right', 6000, velocity='fast')
            # Mix.
            upper_gantry.aspirate(550)
            upper_gantry.move_relative('right', 5000, velocity='fast')
            upper_gantry.dispense(550)
            # Aspirate 820 uL.
            upper_gantry.aspirate(550, pipette_tip_type=1000)
            upper_gantry.move_relative('left', 5000 + 6000, velocity='fast')
            upper_gantry.dispense(600)
            upper_gantry.move_relative('right', 6000, velocity='fast')
            # Mix.
            upper_gantry.aspirate(550)
            upper_gantry.move_relative('right', 5000, velocity='fast')
            upper_gantry.dispense(550)
            upper_gantry.move_relative('left', 5000, velocity='fast')
            # Aspirate 820 uL.
            upper_gantry.aspirate(550, pipette_tip_type=1000)
            # Move to the Mag Separator.
            upper_gantry.move_pipettor('mag_separator_row{0}'.format(tray), use_drip_plate=False, pipette_tip_type=1000, relative_moves=[0,0,20000,0])
            # Dispense.
            upper_gantry.dispense(600)
            # Dispense Residual (50 uL).
            upper_gantry.aspirate(50, pipette_tip_type=1000)
            upper_gantry.dispense(50, pressure='low')
            # Wait 2 minutes.
            delay(2, 'minutes')
            upper_gantry.home_pipettor()
            delay(3, 'minutes')
            upper_gantry.move_pipettor('mag_separator_row{0}'.format(tray), use_drip_plate=False, pipette_tip_type=1000, relative_moves=[0,0,20000,0])
            # Aspirate 830 uL.
            upper_gantry.aspirate(720, pressure='low', pipette_tip_type=1000)
            # Move to the Sample Loading Rack for waste.
            #self.waste_dispense(upper_gantry, dispense_vol=850, target='sample_loading_tray{0}'.format(trays[tray][1]), use_drip_plate=False, pipette_tip_type=1000)
            upper_gantry.move_pipettor('sample_loading_tray{0}'.format(trays[tray][1]), pipette_tip_type=1000, use_drip_plate=False)
            # Dispense.
            upper_gantry.dispense(720)
            # Pop bubbles
            upper_gantry.aspirate(50, pipette_tip_type=1000)
            # Eject tips.
            upper_gantry.tip_eject(trays[tray][0], 1)
        timer.stop(__file__, self.pooling.__name__, time_units='minutes')

    # Pooling Method.
    def pre_dispense(self, upper_gantry, tray_int, pipette_tip_type=1000, number_of_dispenses=5):
        logger = Logger(__file__, __name__)
        timer = Timer(logger)
        timer.start(__file__, self.pre_dispense.__name__)
        msg = """
        **********************************************************************************************
        Extraction: Pre-Dispense
        **********************************************************************************************
        """
        logger.log('HEADER', msg)
        # Move relative to the magnet.
        upper_gantry.move_pipettor('sample_loading_tray{0}'.format(tray_int), pipette_tip_type=1000, use_drip_plate=False, relative_moves=[-3500,0,270000,0])
        #upper_gantry.move_relative('up', 350000, velocity='fast')
        delay(45, 'seconds')
        # Dispense 150 uL 5 times for a total of 750 uL leaving 250 uL in tip.
        for i in range(number_of_dispenses-1):
            if i == 0:
                vol = 100
            else:
                vol = 160
            # Dispense 150 uL.
            upper_gantry.dispense(vol)
            # Wait 3 seconds.
            delay(5, 'seconds')
        upper_gantry.dispense(200)
        # Move relative away from the magnet.
        upper_gantry.move_relative('right', 5500)
        timer.stop(__file__, self.pre_dispense.__name__, time_units='minutes')

    # Wash Method.
    def wash(self, upper_gantry, wash_number, wash_rounds=1, full_protocol=True, dz_usteps=100000):
        logger = Logger(__file__, __name__)
        timer = Timer(logger)
        timer.start(__file__, self.wash.__name__)
        msg = """
        **********************************************************************************************
        Extraction: Wash {0}
        **********************************************************************************************
        """.format(wash_number)
        assert type(wash_number) == int
        assert type(wash_rounds) == int
        wash_numbers = [1, 2]
        assert wash_number in wash_numbers
        logger.log('HEADER', msg)
        trays = {
            1: ['A', 4],
            2: ['B', 3],
            3: ['C', 2],
            4: ['D', 1]
            }
        if full_protocol:
            runs = 4
        else:
            runs = 1
        if wash_number == 1:
            reagent_cartridge_row = 3
            tip_row = 2
            delay_time_minutes = 2
        elif wash_number == 2:
            reagent_cartridge_row = 10
            tip_row = 3
            delay_time_minutes = 1
        for tray in range(1,runs+1):
            # Disengage Magnet.
            upper_gantry.disengage_magnet()
            for round in range(1,wash_rounds+1):
                if wash_rounds > 1:
                    logger.log('MESSAGE', "Round {0}".format(round))
                # Pickup tips.
                if round == 1:
                    upper_gantry.tip_pickup(trays[tray][0], tip_row)
                    #upper_gantry.tip_pickup('tip_transfer_tray', tip_row)
                # Move to Reagent Cartridge Row.
                upper_gantry.move_pipettor('reagent_cartridge_tray{0}_row{1}'.format(trays[tray][1], reagent_cartridge_row), use_drip_plate=False, pipette_tip_type=1000)
                # Aspirate 250 uL.
                upper_gantry.aspirate(250, pipette_tip_type=1000)
                # Move to Mag Separator.
                upper_gantry.move_pipettor('mag_separator_row{0}'.format(tray), use_drip_plate=False, pipette_tip_type=1000, relative_moves=[0,0,20000,0])
                # Dispense 250 uL. (solution is bubbly)
                logger.log('WARNING', "Currently dispensing at full pressure, change to low pressure.")
                upper_gantry.dispense(250, pressure='low')
                # Dispense 50 uL.
                #upper_gantry.dispense(50)
                # Mix: 200 uL 5 times.
                upper_gantry.aspirate(200, pipette_tip_type=1000)
                upper_gantry.dispense(200, pressure='low')
                upper_gantry.aspirate(200, pipette_tip_type=1000)
                upper_gantry.dispense(200, pressure='low')
                upper_gantry.aspirate(200, pipette_tip_type=1000)
                upper_gantry.dispense(200, pressure='low')
                upper_gantry.aspirate(200, pipette_tip_type=1000)
                upper_gantry.dispense(200, pressure='low')
                upper_gantry.aspirate(200, pipette_tip_type=1000)
                upper_gantry.dispense(200, pressure='low')
                # Mix: Move to Mag Separator Row (back to the bottom).
                #upper_gantry.move_pipettor('mag_separator_row{0}'.format(tray))
                # Engage magnet
                upper_gantry.engage_magnet()
                upper_gantry.dispense(50, pressure='low')
                # Wait 5 seconds.
                delay(10, 'seconds')
                # Dispense 50 uL
                #upper_gantry.move_relative('up', dz_usteps, velocity='fast')
                upper_gantry.aspirate(100, pipette_tip_type=1000)
                upper_gantry.dispense(100, pressure='low')
                # Move relative up (to top of liquid).
                upper_gantry.move_relative('up', dz_usteps, velocity='fast')
                upper_gantry.dispense(50, pressure='low')
                # Wait.
                delay(delay_time_minutes, 'minutes')
                # Move to Mag Separator Row (back to the bottom).
                upper_gantry.move_pipettor('mag_separator_row{0}'.format(tray), use_drip_plate=False, pipette_tip_type=1000, relative_moves=[0,0,20000,0])
                # Aspirate 250 uL.
                upper_gantry.aspirate(250, pressure='low', pipette_tip_type=1000)
                # Move to the Reagent Cartridge (Waste).
                upper_gantry.move_pipettor('reagent_cartridge_tray{0}_row12'.format(trays[tray][1]), pipette_tip_type=1000, use_drip_plate=False)
                # Dispense 300 uL.
                upper_gantry.dispense(250)
                # Aspirate 50 uL to avoid bubble (snuffle back).
                #upper_gantry.move_relative('up', dz_usteps, velocity='fast')
                upper_gantry.dispense(50)
                if wash_rounds > 1:
                    logger.log('MESSAGE', "Round {0} Complete.".format(round))
            # Eject tips.
            logger.log('MESSAGE', "Putting Wash 1 tips in Tray {0} Row 1 to avoid contamination.".format(trays[tray][0]))
            upper_gantry.tip_eject(trays[tray][0], tip_row)
        timer.stop(__file__, self.wash.__name__, time_units='minutes')

    # Pre-Elution Method.
    def pre_elution(self, upper_gantry, full_protocol=True, air_dry_time_minutes=5):
        logger = Logger(__file__, __name__)
        timer = Timer(logger)
        timer.start(__file__, self.pre_elution.__name__)
        msg = """
        **********************************************************************************************
        Extraction: Pre-Elution (Removal of excess EtOH and Air Dry Time)
        **********************************************************************************************
        """
        logger.log('HEADER', msg)
        trays = {
            1: ['A', 4],
            2: ['B', 3],
            3: ['C', 2],
            4: ['D', 1]
            }
        if full_protocol:
            runs = 4
        else:
            runs = 1
        for tray in range(1,runs+1):
            timer.log_current_elapsed_time(__file__, self.pre_elution.__name__, "Pre-Elution Run {0} / {1}.".format(tray, runs))
            # Pickup tips.
            upper_gantry.tip_pickup(trays[tray][0], 5)
            #upper_gantry.tip_pickup('tip_trasnfer_tray', 3)
            # Move to Mag Separator Row.
            upper_gantry.move_pipettor('mag_separator_row{0}'.format(tray), use_drip_plate=False)
            # Aspirate Residual EtOH (30 uL).
            upper_gantry.aspirate(45)
            # Move to the Reagent Cartridge for Waste.
            upper_gantry.move_pipettor('reagent_cartridge_tray{0}_row12'.format(trays[tray][1]), use_drip_plate=False)
            # Dispense Residual EtOH.
            upper_gantry.dispense(45)
            # Tip Eject in the Tip Transfer Tray Row.
            upper_gantry.tip_eject(trays[tray][0], 5)
            # Home Pipettor.
            upper_gantry.move_pipettor('home', use_drip_plate=False)
            # Air dry.
            delay(air_dry_time_minutes, 'minutes')
        timer.stop(__file__, self.pre_elution.__name__, time_units='minutes')

    # Elution Method.
    def elution(self, upper_gantry, full_protocol=True):
        logger = Logger(__file__, __name__)
        timer = Timer(logger)
        timer.start(__file__, self.elution.__name__)
        msg = """
        **********************************************************************************************
        Extraction: Elution
        **********************************************************************************************
        """
        logger.log('HEADER', msg)
        trays = {
            1: ['A', 4],
            2: ['B', 3],
            3: ['C', 2],
            4: ['D', 1]
            }
        if full_protocol:
            runs = 4
        else:
            runs = 1
        for tray in range(1,runs+1):
            timer.log_current_elapsed_time(__file__, self.elution.__name__, "Elution Run {0} / {1}.".format(tray, runs))
            # Disengage Meganet for beads to loosen up.
            upper_gantry.disengage_magnet()
            # Pickup tips.
            upper_gantry.tip_pickup(trays[tray][0], 6)
            # Move to the Reagent Cartridge Row for 9 the Elution Buffer.
            upper_gantry.move_pipettor('reagent_cartridge_tray{0}_row5'.format(trays[tray][1]), use_drip_plate=False, pipette_tip_type=50)
            # Aspirate 36 uL.
            upper_gantry.aspirate(36, pipette_tip_type=50)
            # Move to the Mag Separator Row
            upper_gantry.move_pipettor('mag_separator_row{0}'.format(tray), use_drip_plate=False, pipette_tip_type=50)
            # Dispense 36 uL.
            upper_gantry.dispense(36)
            # Mix 15 times (estimates to 5 minutes of mixing).
            logger.log('WARNING', "This 5 minute mixing will probably be less than 5 minutes because the time analysis was taken from a 1 mL tip not a 50 uL tip.")
            for i in range(10):
                upper_gantry.aspirate(25)
                upper_gantry.dispense(25)
            # Engage Magnet.
            upper_gantry.engage_magnet()
            upper_gantry.move_relative('up', 20000, velocity='fast')
            upper_gantry.dispense(50)
            # Delay for a bit
            delay(20, 'seconds')
            # Move to mag separator.
            #upper_gantry.move_pipettor('mag_separator_row{0}'.format(tray))
            upper_gantry.move_relative('down', 20000, velocity='fast')
            # Aspirate 25 uL.
            upper_gantry.aspirate(25, pipette_tip_type=50)
            # Dispense 25 uL.
            upper_gantry.dispense(25, pressure='low')
            # Residual dispense
            upper_gantry.move_relative('up', 20000, velocity='fast')
            upper_gantry.dispense(10, pressure='low')
            # Wait 30 seconds.
            delay(30, 'seconds')
            # Aspirate 20 uL.
            upper_gantry.move_relative('down', 20000, velocity='fast')
            upper_gantry.home_pipettor()
            delay(10, 'minutes')
            upper_gantry.move_pipettor('mag_separator_row{0}'.format(tray), use_drip_plate=False, pipette_tip_type=50)
            upper_gantry.aspirate(7)
            # Move to the Assay Strip.
            upper_gantry.move_pipettor('assay_strip_row{0}'.format(tray + (tray - 1)), use_drip_plate=False, pipette_tip_type=50)
            # Dispense 20 uL.
            upper_gantry.dispense(7)
            # Eject tips.
            #upper_gantry.tip_eject(trays[tray][0], 6)
            # Home the Pipettor.
            #upper_gantry.home_pipettor()
        timer.stop(__file__, self.elution.__name__, time_units='minutes')

    # cfDNA Extraction Method.
    def extraction(self, upper_gantry, full_protocol=True):
        logger = Logger(__file__, __name__)
        logger.log('LOG-START', "Starting cfDNA Extraction Protocol with Full Protocol set to {0}.".format(full_protocol))
        timer = Timer(logger)
        timer_protocol = Timer(logger)

        timer_protocol.start(__file__, __name__)
        # Set the Heater/Shaker Temperature.
        logger.log('WARNING', "Make sure to set the temperature of the Heater/Shaker at the beginning of the Extraction Protocol.")
        #upper_gantry.change_heater_shaker_temperature(37, block=False)

        # Transfer Plasma Step
        self.transfer_plasma(upper_gantry, full_protocol=False)

        # Binding Step
        self.binding(upper_gantry, full_protocol=False)

        # Pooling Step
        self.pooling(upper_gantry, full_protocol=False)

        # Wash 1 Step
        self.wash(upper_gantry, wash_number=1, wash_rounds=2, full_protocol=False, dz_usteps=100000)

        # Wash 2 Step
        self.wash(upper_gantry, wash_number=2, wash_rounds=1, full_protocol=False, dz_usteps=100000)

        # Pre-Elution Step.
        self.pre_elution(upper_gantry, full_protocol=False, air_dry_time_minutes=5)

        # Elution Step
        self.elution(upper_gantry, full_protocol=False)

        timer_protocol.stop(__file__, __name__, time_units='minutes')
        logger.log('LOG-END', "cfDNA Extraction Protocol Complete.")

    def quant(self):
        return None

    def thermocycle(self, 
                    meerstetter, 
                    n_cycles:int, denature_time_in_minutes: int, 
                    addresses: list, 
                    high_temperatures: list, high_temperature_time: int, 
                    low_temperatures:list, low_temperature_time: int,
                    final_hold_temperature: int) -> None:
        """
        Input:
            meerstetter: Meerstetter object
            n_cycles: number of cycles
            denature_time_in_minutes: 

        """
        logger = Logger(__file__, self.thermocycle.__name__)
        for address in addresses:
            i = addresses.index(address)
            meerstetter.change_temperature(address, high_temperatures[i], block=False)
        delay(denature_time_in_minutes, 'minutes')
        for cycle in range(n_cycles):
            logger.log('MESSAGE', "Cycle {0} of {1}".format(cycle+1, n_cycles))
            for address in addresses:
                i = addresses.index(address)
                meerstetter.change_temperature(address, high_temperatures[i], block=False)
            delay(high_temperature_time, 'seconds')
            for address in addresses:
                i = addresses.index(address)
                meerstetter.change_temperature(address, low_temperatures[i], block=False)
            delay(low_temperature_time, 'seconds')
        for address in addresses:
                i = addresses.index(address)
                meerstetter.change_temperature(address, final_hold_temperature, block=False)

    # Pooling Method.
    def assay_prep(self, upper_gantry):
        logger = Logger(__file__, __name__)
        logger.log('LOG-START', "Starting Assay Prep Protocol.")
        timer = Timer(logger)
        timer_protocol = Timer(logger)

        timer_protocol.start(__file__, __name__)

        # Transfer 6.25 uL from the mag separator to the assay strip
        #upper_gantry.move_pipettor('mag_separator_row1', use_drip_plate=False, pipette_tip_type=50)
        #upper_gantry.aspirate(7, pipette_tip_type=50)
        #upper_gantry.move_pipettor('assay_strip_row1', use_drip_plate=False, pipette_tip_type=50)
        #upper_gantry.dispense(7)

        # Mix 5 times
        for i in range(5):
            upper_gantry.aspirate(20, pipette_tip_type=50)
            upper_gantry.dispense(20)

        #upper_gantry.aspirate(22, pipette_tip_type=50)
        #upper_gantry.move_pipettor('dg8_1000_010', use_drip_plate=False, pipette_tip_type=50)
        #upper_gantry.dispense(22, pressure='very low')

        timer_protocol.stop(__file__, __name__, time_units='minutes')
        logger.log('LOG-END', "Assay Prep Protocol Complete.")

    def generate_droplets_and_load(self, upper_gantry, droplet_type='pico'):
        droplet_types = ['pico', 'standard']
        assert droplet_type in droplet_types
        upper_gantry.aspirate(22, pipette_tip_type=50)
        upper_gantry.move_pipettor('dg8_1000_010', use_drip_plate=False, pipette_tip_type=50)
        upper_gantry.dispense(22, pressure='very low')
        upper_gantry.tip_eject('A', 6)
        upper_gantry.tip_pickup('A', 4)
        upper_gantry.move_pipettor('reagent_cartridge_tray4_row6', use_drip_plate=False, pipette_tip_type=1000)
        upper_gantry.aspirate(100, pipette_tip_type=1000)
        upper_gantry.move_pipettor('dg8_1000_100', use_drip_plate=False, pipette_tip_type=1000, use_z=False)
        upper_gantry.move_relative('d', 715000, velocity='fast')
        upper_gantry.move_relative('r', 2000, velocity='fast')
        upper_gantry.dispense(120, pressure='low')
        upper_gantry.tip_eject('A', 4)
        dz = coordinates['deck_plate']['dg8']['dz']
        upper_gantry.move_pipettor('dg8_1000_001', use_drip_plate=False, pipette_tip_type=None, relative_moves=[0,0,-dz,0])
        upper_gantry.generate_droplets(droplet_type)
        upper_gantry.home_pipettor()
