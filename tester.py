'''
'''

from logger import Logger
from utils import delay
from timer import Timer

class Tester():
    # Public variables.
    # Private variables.
    __module = None

    # Private constants.
    __MODULES = [
        'pipettor_gantry',
        'reader',
        'pipettor',
        'peltier',
        ]

    __TESTABLE_TIP_SIZES = []
    # Constructor.
    def __init__(self, module=None):
        if module != None:
            assert type(module) == str
            assert module.lower() in self.__MODULES
        self.__module = module

    # Verifiy Functionality Method.
    def verify_all_functionality(self, upper_gantry, reader, peltier):
        conversion = {
            1: 'D',
            2: 'C',
            3: 'B',
            4: 'A',
            }
        answers = ['yes', 'no', 'y', 'n']
        # Setup the logger.
        logger = Logger(__file__, __name__)
        timer_protocol = Timer(logger)
        timer_protocol.start(__file__, __name__)
        timer = Timer(logger)
        logger.log('LOG-START', "Verifying all functionality for the upper gantry, reader, and peltier for this device.")
        msg = """
            Before verification begins, please do the following:
            - Press down on the E-stop to cut all power to the motors.
            - Physically pull the upper gantry towards you (Y-axis), enough to see it home, and the same for
              the X-axis, pull it to your left, enough to see it home. Z1 and Z2 (drip plate) is hard move 
              so let it be.
            - Physically move the reader towards you (Y-axis), move the reader to your right (X-axis), 
              down (Z1-axis), and rotate the filter wheel (Z2-axis).
            - Partially close Tray AB (furthest back) about half an inch, same for Tray CD (closest tray).
            - Gently push down on all 4 heaters, A, B, C, D (from back to front, respectively), down enough
              to see that they can home.
            - Fill sample loading tray C with 1 mL of water for testing aspiration then dispense.
            - Place 1 lid on the lid tray.
            - Place 1 chip on the tip transfer tray.
            - Make sure that the 32 Deep Well plate is clipped into the heater/shaker. To do this,
              push the pin away from you so that the locking mechanism unlocks on the heater/shaker,
              so that the 32 Deep Well plate arms close on the plate.
            - Make sure there are 1 mL tips in tip tray C row 1.
            - Make sure there are 50 uL tips in tip tray C row 12.
            - Make sure there are no tips in the tip transfer tray.
        """
        logger.log('MESSAGE', msg)
        print('\n*****************************************************************************************************')
        print("\nPLEASE MAKE SURE YOU DID EVERYTHING IN THE CHECKLIST ABOVE BEFORE STARTING THIS TEST.\n")
        print('*****************************************************************************************************\n')
        answer = input("Did you do everything in the checklist? [yes/no]?\n")
        assert type(answer) == str
        assert answer in answers
        if answer[0].lower() != 'y':
            logger.log('LOG-END', "The checklist was not followed, aborting for safety.")
            return
        logger.log('MESSAGE', "The user has read the entire checklist to make sure they implemented everything in it.")
        msg = """
            Now that you agree all the checks are satisfied and you are not worried about breaking your unit,
            depress the E-stop which involves a clockwise twist (follow the arrows).
        """
        logger.log('MESSAGE', msg)
        msg = """
            Did you depress the E-stop and wait about 5 seconds for the motors to reengage? (you should have hard a short
            hum indicating that the motors are engaged). Motor reengaging can be physically tested by trying to move
            the Upper Gantry Seyonic Pipettor head, if it can't be easily moved, the motors are engaged, the same
            can be done with the Reader. [yes/no]?\n"
        """
        answer = input(msg)
        assert type(answer) == str
        assert answer[0].lower() in answers
        if answer[0].lower() != 'y':
            logger.log('MESSAGE', "The E-stop was not depressed, or the motors did not reengage.")
            answer = input("Did you depress the E-stop [yes/no]?\n")
            assert type(answer) == str
            assert answer[0].lower() in answers
            if answer[0].lower() == 'y':
                logger.log('LOG-END', "The E-stop was depressed, therefore the motors were not engaged, contact maintenance. Aborting.")
            else:
                logger.log('LOG-END', "The E-stop was not depressed. Aborting.")
            return
        msg = """

            *****************************************************************************************************
            DURING THE VERIFICATION PROCESS HAVE YOUR HAND READY TO HIT THE E-STOP AT ANY MOMENT TO MINIMIZE THE 
            RISK OF BREAKING SOMETHING ON THE INSTRUMENT.
            *****************************************************************************************************

        """
        logger.log('MESSAGE', msg)
        answer = input("Are you ready to begin verification [yes/no]?\n")
        assert type(answer) == str
        assert answer in answers
        if answer[0].lower() != 'y':
            logger.log('LOG-END', "User is not ready, aborting.")
            return
        else:
            logger.log('MESSAGE', "The user has agreed to start verification for this unit.")
        # Verify Homing of the Upper Gantry.
        answer = input("Verify Upper Gantry Homing [yes/no]?\n")
        assert type(answer) == str
        assert answer in answers
        if answer[0].lower() != 'y':
            logger.log('MESSAGE', "The user is skipping upper_gantry.home_pipettor().")
            upper_gantry_homed = False
        else:
            upper_gantry.home_pipettor()
            upper_gantry_homed = True
        # Verify Homing of the Reader.
        answer = input("Verify Reader Homing [yes/no]?\n")
        assert type(answer) == str
        assert answer in answers
        if answer[0].lower() != 'y':
            logger.log('MESSAGE', "The user is skipping reader.home_reader().")
            reader_homed = False
        else:
            reader.home_reader()
            reader_homed = True
        # Verify Tip Pickup and Tip Eject.
        if upper_gantry_homed:
            answer = input("Verify Tip Pickup and Tip Eject for all Tip Trays [yes/no]?\n")
            assert type(answer) == str
            assert answer in answers
            if answer[0].lower() != 'y':
                logger.log('MESSAGE', "The user is skipping tip pickup and tip eject for all tip trays.")
            else:
                for tray in range(1,5):
                    if tray != 2:
                        logger.log('WARNING', "Only testing Tip Tray C.")
                        continue
                    for row in range(1,13):
                        logger.log('MESSAGE', "Tip Pickup: Tray {0}, Row {1}.".format(conversion[tray], row))
                        upper_gantry.tip_pickup(conversion[tray], row, slow_z=True)
                        answer = input("Were tips picked up from Tip Tray {0} Row {1} [yes/no]?\n".format(conversion[tray], row))
                        assert type(answer) == str
                        assert answer in answers
                        if answer[0].lower() != 'y':
                            logger.log('ERROR', "Tip Pickup from Tip Tray {0} Row {1} was unsuccessful, contact maintenance.".format(conversion[tray], row))
                            logger.log('LOG-END', "Aborting due to verification failure.")
                            return
                        else:
                            logger.log('MESSAGE', "Tip Pickup in Tip Tray {0} Row {1} was successful. Continuing to Tip Eject.".format(conversion[tray], row))
                        upper_gantry.tip_eject(conversion[tray], row)
                        answer = input("Were tips ejected into Tip Tray {0} Row {1} [yes/no]?\n".format(conversion[tray], row))
                        assert type(answer) == str
                        assert answer in answers
                        if answer[0].lower() != 'y':
                            logger.log('ERROR', "Tip Eject into Tip Tray {0} Row {1} was unsuccessful, contact maintenance.".format(conversion[tray], row))
                            logger.log('LOG-END', "Aborting due to verification failure.")
                            return
                        else:
                            logger.log('MESSAGE', "Tip Eject in Tip Tray {0} Row {1} was successful.".format(conversion[tray], row))
                for row in range(1,9):
                    logger.log('MESSAGE', "Tip Pickup: Tip Transfer Tray Row {0}".format(row))
                    upper_gantry.tip_pickup('tip_transfer_tray', row, slow_z=True)
                    answer = input("Were tips picked up from Tip Transfer Tray Row {0} [yes/no]?\n".format(row))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Tip Pickup from the Tip Transfer Tray Row {0} was unsuccessful, contact maintenance.".format(row))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Tip Pickup in the Tip Transfer Tray Row {0} was successful. Continuing to Tip Eject.".format(row))
                    upper_gantry.tip_eject('tip_transfer_tray', row)
                    answer = input("Were tips ejected into the Tip Transfer Tray Row {0} [yes/no]?\n".format(row))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Tip Eject into the Tip Transfer Tray Row {0} was unsuccessful, contact maintenance.".format(row))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Tip Eject in the Tip Transfer Tray Row {0} was successful.".format(row))
            # Verify Reagent Cartridge Positions with two different tip size (50 uL).
            answer = input("Verify Reagent Cartridge Positions/Aspirate/Dispense with 1 mL tips [yes/no]?\n")
            assert type(answer) == str
            assert answer in answers
            if answer[0].lower() != 'y':
                logger.log('MESSAGE', "The user is skipping Reagent Cartridge Verification.")
            else:
                # Pickup 1mL tips.
                upper_gantry.tip_pickup('C', 1)
                # Move to the Reagent Cartridge Positions.
                for row in range(1, 13):
                    if row == 10 or row == 11:
                        logger.log('WARNING', "Skipping Reagent Cartridge Row {0}.".format(row))
                        continue
                    logger.log('MESSAGE', "Reagent Cartridge Row {0}".format(row))
                    upper_gantry.move_pipettor('reagent_cartridge_tray2_row{0}'.format(row), use_drip_plate=True, slow_z=True)
                    answer = input("Was the position test for the Reagent Cartridge Row {0} a success [yes/no]?\n".format(row))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Position Tests for the Reagent Cartridge Row {0} was unsuccessful, contact maintenance.".format(row))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Position Tests for the Reagent Cartridge Row {0} was successful. Continuing to Aspiration.".format(row))
                    upper_gantry.aspirate(500)
                    answer = input("Was the aspiration test for the Reagent Cartridge Row {0} a success [yes/no]?\n".format(row))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Aspiration Tests for the Reagent Cartridge Row {0} was unsuccessful, contact maintenance.".format(row))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Aspiration Tests for the Reagent Cartridge Row {0} was successful. Continuing to Dispense.".format(row))
                    upper_gantry.dispense(550)
                    answer = input("Was the dispense test for the Reagent Cartridge Row {0} a success [yes/no]?\n".format(row))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Dispense Tests for the Reagent Cartridge Row {0} was unsuccessful, contact maintenance.".format(row))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Dispense Tests for the Reagent Cartridge Row {0} was successful.".format(row))
            # Verify Reagent Cartridge Positions with two different tip size (50 uL).
            answer = input("Verify Reagent Cartridge Positions/Aspirate/Dispense with 50 uL tips [yes/no]?\n")
            assert type(answer) == str
            assert answer in answers
            if answer[0].lower() != 'y':
                logger.log('MESSAGE', "The user is skipping Reagent Cartridge Verification.")
            else:
                # Pickup 1mL tips.
                upper_gantry.tip_pickup('C', 12)
                # Move to the Reagent Cartridge Positions.
                for row in range(1, 13):
                    if row == 10 or row == 11:
                        logger.log('WARNING', "Skipping Reagent Cartridge Row {0}.".format(row))
                        continue
                    logger.log('MESSAGE', "Reagent Cartridge Row {0}".format(row))
                    upper_gantry.move_pipettor('reagent_cartridge_tray2_row{0}'.format(row), use_drip_plate=True, slow_z=True)
                    answer = input("Was the position test for the Reagent Cartridge Row {0} a success [yes/no]?\n".format(row))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Position Tests for the Reagent Cartridge Row {0} was unsuccessful, contact maintenance.".format(row))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Position Tests for the Reagent Cartridge Row {0} was successful. Continuing to Aspiration.".format(row))
                    upper_gantry.aspirate(25)
                    answer = input("Was the aspiration test for the Reagent Cartridge Row {0} a success [yes/no]?\n".format(row))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Aspiration Tests for the Reagent Cartridge Row {0} was unsuccessful, contact maintenance.".format(row))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Aspiration Tests for the Reagent Cartridge Row {0} was successful. Continuing to Dispense.".format(row))
                    upper_gantry.dispense(30)
                    answer = input("Was the dispense test for the Reagent Cartridge Row {0} a success [yes/no]?\n".format(row))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Dispense Tests for the Reagent Cartridge Row {0} was unsuccessful, contact maintenance.".format(row))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Dispense Tests for the Reagent Cartridge Row {0} was successful.".format(row))
                upper_gantry.tip_eject('C', 1)
            # Verify Sample Loading Positions with the 1 mL tips.
            answer = input("Verify Sample Loading Positions/Aspirate/Dispense with 1 mL tips [yes/no]?\n")
            assert type(answer) == str
            assert answer in answers
            if answer[0].lower() != 'y':
                logger.log('MESSAGE', "The user is skipping Sample Loading Verification.")
            else:
                # Pickup 1mL tips.
                upper_gantry.tip_pickup('C', 1)
                # Move to the Sample Loading Positions.
                for tray in range(1, 5):
                    if tray == 1:
                        logger.log('WARNING', "Skipping Sample Loading Tray {0}.".format(tray))
                        continue
                    logger.log('MESSAGE', "Sample Loading Tray {0}".format(tray))
                    upper_gantry.move_pipettor('sample_loading_tray{0}'.format(tray), use_drip_plate=False, slow_z=True)
                    answer = input("Was the position test for the Sample Loading Tray {0} a success [yes/no]?\n".format(tray))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Position Tests for the Sample Loading Tray {0} was unsuccessful, contact maintenance.".format(tray))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Position Tests for the Sample Loading Tray {0} was successful. Continuing to Aspiration.".format(tray))
                    upper_gantry.aspirate(500)
                    answer = input("Was the aspiration test for the Sample Loading Tray {0} a success [yes/no]?\n".format(tray))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Aspiration Tests for the Sample Loading Tray {0} was unsuccessful, contact maintenance.".format(tray))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Aspiration Tests for the Sample Loading Tray {0} was successful. Continuing to Dispense.".format(tray))
                    upper_gantry.dispense(550)
                    answer = input("Was the dispense test for the Sample Loading Tray {0} a success [yes/no]?\n".format(tray))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Dispense Tests for the Sample Loading Tray {0} was unsuccessful, contact maintenance.".format(tray))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Dispense Tests for the Sample Loading Tray {0} was successful.".format(tray))
                upper_gantry.tip_eject('C', 1)
            # Veryify the Heater/Shaker Locations with 1 mL and 50 uL tips.
            answer = input("Verify Heater/Shaker Positions/Aspirate/Dispense with 1 mL tips [yes/no]?\n")
            assert type(answer) == str
            assert answer in answers
            if answer[0].lower() != 'y':
                logger.log('MESSAGE', "The user is skipping Heater/Shaker Verification.")
            else:
                # Pickup 1mL tips.
                upper_gantry.tip_pickup('C', 1)
                # Move to the Heater/Shaker Positions with 1 mL.
                for row in range(1,5):
                    logger.log('MESSAGE', "Heater/Shaker Row {0}".format(row))
                    upper_gantry.move_pipettor('heater_shaker_row{0}'.format(row), use_drip_plate=False, slow_z=True)
                    answer = input("Was the position test for the Heater/Shaker Row {0} a success [yes/no]?\n".format(row))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Position Tests for the Heater/Shaker Row {0} was unsuccessful, contact maintenance.".format(row))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Position Tests for the Heater/Shaker Row {0} was successful. Continuing to Aspiration.".format(row))
                    upper_gantry.aspirate(500)
                    answer = input("Was the aspiration test for the Heater/Shaker Row {0} a success [yes/no]?\n".format(row))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Aspiration Tests for the Heater/Shaker Row {0} was unsuccessful, contact maintenance.".format(row))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Aspiration Tests for the Heater/Shaker Row {0} was successful. Continuing to Dispense.".format(row))
                    upper_gantry.dispense(550)
                    answer = input("Was the dispense test for the Heater/Shaker Row {0} a success [yes/no]?\n".format(row))
                    assert type(answer) == str
                    assert answer in answers
                    if answer[0].lower() != 'y':
                        logger.log('ERROR', "Dispense Tests for the Heater/Shaker Row {0} was unsuccessful, contact maintenance.".format(row))
                        logger.log('LOG-END', "Aborting due to verification failure.")
                        return
                    else:
                        logger.log('MESSAGE', "Dispense Tests for the Heater/Shaker Row {0} was successful.".format(row))
                # Eject Tips.
                upper_gantry.tip_eject('C', 1)
            # Verify the Heater/Shaker with 50 uL tips.
            # Verify the PCR Thermocycler positions with the 50 uL tips.
            # Verify Aux Heaters with 1 mL and 50 uL tips.
            # Verify the Assay Strips with the 50 uL tips.
            # Verify the DNA Quant Strips with the 50 uL tips.
            # Verify the Chip Loading Locations with the 1 mL and 50 uL tips.
            # Verify Aspiration
            # Verify Dispense
            # Verify Mixing
            # Verify Chip and Lid Transfer.
            # Verify Tray closing with Lidded Chip.
            # Verify Heater Clamping with Lidded Chips.
            # Home Pipettor when done.
            answer = input("Home the pipettor now that verification of the Upper Gantry is complete [yes/no]?\n")
            assert type(answer) == str
            assert answer in answers
            if answer[0].lower() != 'y':
                logger.log('MESSAGE', "The user is skipping homing of the pipettor after verification of the Upper Gantry functionality.")
            else:
                logger.log('MESSAGE', "The user is homing the pipettor after successfully verifying Upper Gantry functionality.")
        # Verify Temperature Calibration on the ddPCR Thermocyclers (Heater A, B, C, D).
        # Verify Reader Movement to Heater Locations.
        # Verify LED functionality.
        # Verify Heater/Shaker shaking.
        # Veryify Chiller.
        # Veryify Mag Separator Motion.
        
        timer_protocol.stop(__file__, __name__)
        logger.log('LOG-END', "Verification is complete.")
