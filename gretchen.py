'''
'''

from logger import Logger
from utils import delay

import datetime

def pre_amp_workflow(upper_gantry):
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
    logger = Logger(__file__, pre_amp_workflow.__name__, 'gretchen_pre_amp_workflow_day_{0}_{1}_{2}_time_{3}_{4}_{5}.txt'.format(month, day, year, hour, minute, second))
    logger.log('LOG-START', "Starting Gretchen's Pre-Amp Workflow on {0}/{1}/{2} at {3}:{4}:{5} {6}".format(month, day, year, hour, minute, second, am_or_pm))
    # Begin with eluted cfDNA in the Mag Separator.
    # Pickup 50 microliter tips for Batch A (re-use from elution step)
    upper_gantry.tip_pickup('C', 12)
    # Move to Reagent Cartridge Row X with water.
    upper_gantry.move_pipettor('reagent_cartridge_tray2_row1', use_drip_plate=False)
    # Aspirate 15 microliters of water.
    upper_gantry.aspirate(15)
    # Move to the Pre-Amp Thermocycler Row 1.
    upper_gantry.move_pipettor('pcr_thermocycler_row1')
    # Dispense 15 microliters of water in Pre-Amp Thermocycler Row 1.
    upper_gantry.dispense(20)
    # Move to the Mag Separator Row 1.
    upper_gantry.move_pipettor('mag_separator_row1')
    # Aspirate 10 microliters of cfDNA from the Mag Separator Row 1.
    upper_gantry.aspirate(10)
    # Move to the Pre-Amp Thermocycler Row 1.
    upper_gantry.move_pipettor('pcr_thermocycler_row1')
    # Dispense 10 microliters of cfDNA into Pre-Amp Thermocycler Row 1.
    upper_gantry.dispense(15)
    # Pipette mix 3-5 times in the Pre-Amp Thermocycler Row 1.
    upper_gantry.mix(aspirate_vol=25, dispense_vol=30, cycles=3)
    # Move to the Tip Transfer Tray and Eject Tips.
    upper_gantry.tip_eject('tip_transfer_tray', 1)
    # Move to tips used for EOTH residual removal and pick them up.
    upper_gantry.tip_pickup('tip_transfer_tray', 2)
    # Move to Reagent Cartridge Row X with mineral oil.
    upper_gantry.move_pipettor('reagent_cartridge_tray2_row2')
    # Aspirate 25 microliters of mineral oil.
    upper_gantry.aspirate(25)
    # Move to the Pre-Amp Thermocycler Row 1.
    upper_gantry.move_pipettor('pcr_thermocycler_row1')
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
    upper_gantry.move_pipettor('pcr_thermocycler_row1')
    # Dispense 25 microliters of water in Pre-Amp Thermocycler Row 1.
    upper_gantry.dispense(30)
    upper_gantry.move_pipettor('home')
    logger.log('LOG-END', "Ended Gretchen's Pre-Amp Workflow on {0}/{1}/{2} at {3}:{4}:{5} {6}".format(month, day, year, hour, minute, second, am_or_pm))
