'''
'''

from timer import Timer
from utils import delay
from logger import Logger 

import os

class Paul():
    # Public variables.
    # Private variables.
    # Private constants.
    # Constructor.
    def __init__(self):
        a = 1

    # Timing Estimates Protocol Method.
    def timing_estimates_protocol(self, upper_gantry):
        # Setup the logger.
        logger = Logger(__file__, __name__)
        logger.log('LOG-START', "Starting Paul's Timing Estimate Protocol.")
        # Setup the timer.
        timer = Timer(logger)
        timer_protocol = Timer(logger)
        # Home the pipettor for safety.
        timer.start(__file__, 'home_pipettor')
        timer_protocol.start(__file__, __name__)
        upper_gantry.home_pipettor()
        timer.stop(__file__, 'home_pipettor')
        # Tip Pickups.
        timer.start(__file__, 'tip_pickup')
        upper_gantry.tip_pickup('A', 1)
        timer.stop(__file__, 'tip_pickup')
        # Move to the Sample Rack.
        timer.start(__file__, 'move_pipettor')
        upper_gantry.move_pipettor('sample_loading_tray4', use_drip_plate=False, pipette_tip_type=1000)
        timer.stop(__file__, 'move_pipettor')
        # Mix.
        timer.start(__file__, 'mix')
        upper_gantry.aspirate(1000, pipette_tip_type=1000)
        upper_gantry.dispense(1010)
        upper_gantry.aspirate(1000, pipette_tip_type=1000)
        upper_gantry.dispense(1010)
        upper_gantry.aspirate(1000, pipette_tip_type=1000)
        upper_gantry.dispense(1010)
        timer.stop(__file__, 'mix')
        # Aspirate from the Sample Rack.
        timer.start(__file__, 'aspirate')
        upper_gantry.aspirate(840)
        timer.stop(__file__, 'aspirate')
        # Move the pipettor to the Reagent Cartridge
        timer.start(__file__, 'move_pipettor')
        upper_gantry.move_pipettor('reagent_cartridge_tray4_row1')
        timer.stop(__file__, 'move_pipettor')
        # Aspirate from the Reagent Cartridge.
        timer.start(__file__, 'aspirate')
        upper_gantry.aspirate(160)
        timer.stop(__file__, 'aspirate')
        # Move the pipettor to the Heater/Shaker.
        timer.start(__file__, 'move_pipettor')
        upper_gantry.move_pipettor('heater_shaker_row1')
        timer.stop(__file__, 'move_pipettor')
        # Dispense in to the Heater/Shaker.
        timer.start(__file__, 'dispense')
        upper_gantry.dispense(1000)
        timer.stop(__file__, 'dispense')
        # Mix.
        timer.start(__file__, 'mix')
        upper_gantry.aspirate(1000, pipette_tip_type=1000)
        upper_gantry.dispense(1010)
        timer.stop(__file__, 'mix')
        timer_protocol.stop(__file__, __name__)
        logger.log('LOG-END', "Done with Paul's Timing Estimate Protocol.")
