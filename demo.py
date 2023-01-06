'''
'''
from utils import delay
from logger import Logger
from timer import Timer

from script import Script

from coordinate import coordinates

def run(upper_gantry, reader):
    # Pickup tips.
    upper_gantry.tip_pickup('A', 1)
    # Aspirate sample and dispense into lysis tube
    upper_gantry.move_pipettor('sample_loading_tray4', use_drip_plate=False)
    upper_gantry.aspirate(500)
    upper_gantry.move_pipettor('heater_shaker_row1', use_drip_plate=False)
    upper_gantry.dispense(600)
    # Get reagent.
    upper_gantry.move_pipettor('reagent_cartridge_tray4_row1', use_drip_plate=False)
    upper_gantry.aspirate(500)
    upper_gantry.move_pipettor('heater_shaker_row1', use_drip_plate=False)
    upper_gantry.dispense(600)
    # Eject tips.
    upper_gantry.tip_eject('A', 1)
    # Close PCR Tray
    reader.close_tray('CD')
    reader.lower_heater('D')
    # Light show
    reader.move_reader('heater_d')
    reader.illumination_on('alexa405')
    delay(1, 'second')
    reader.illumination_off('alexa405')
    reader.illumination_on('cy55')
    delay(1, 'second')
    reader.illumination_off('cy55')
    reader.illumination_on('cy5')
    delay(1, 'second')
    reader.illumination_off('cy5')
    reader.illumination_on('fam')
    delay(1, 'second')
    reader.illumination_off('fam')
    reader.illumination_on('hex')
    delay(1, 'second')
    reader.illumination_off('hex')
    reader.illumination_on('atto')
    delay(1, 'second')
    reader.illumination_off('atto')

def run_long(upper_gantry, reader):
    """
    Minimum Demo Conditions:
      - Requirements
        - Home the Pipettor and Reader prior to starting the demo for a faster demo.
        - Fill the volumes
        - Load one liddless chip on the tip transfer tray.
        - Load one lid on to the Lid Tray.
        - Load DG8 onto 15 degree incline holder.
      - Consumables
        - Tip Tray A
        - Reagent Cartridge A
        - Sample Loading A
        - Heater/Shaker
        - Mag Separator
        - Tip Transfer Tray
        - Lid Tray
        - PCR Thermocycler
        - Droplet or Microwell Chips
      - Volumes
        - 
      - Tips
        - 1 mL
        - 50 uL tips
    """
    logger = Logger(__file__, __name__)
    timer = Timer(logger)
    timer_plasma = Timer(logger)
    timer_binding = Timer(logger)
    timer_pooling = Timer(logger)
    timer_pre_amp = Timer(logger)
    timer_droplet_generation = Timer(logger)
    timer_protocol = Timer(logger)
    msg = """

        ***************************************************************************
        Starting the CDP 2.0 demo script which involves a minimalization of cfDNA
        Extraction, minimal Pre-Amp, droplet generation, chip loading, and mock
        Imaging.
        ***************************************************************************

    """
    logger.log('LOG-START', msg)
    timer_protocol.start(__file__,__name__)
    logger.log('MESSAGE', "Clearing up space for the Tip Transfer Tray.")
    timer.start(__file__, __name__)
    # Move the chip from Tip Transfer Tray to Tray CD Out Location D - (Suction Cup Showcase)
    #upper_gantry.move_chip(4, 'microwells', 'D')
    timer.stop(__file__, __name__)
    # ------------------------------------------------------------------------------
    # Extraction (Minimal Showcase of the Apostle Extraction)
    # ------------------------------------------------------------------------------
    msg = """
        \n**************************************************************************
        Extraction (Minimal Showcase of the Apostle Extraction)
        ******************************************************************************\n
    """
    logger.log('MESSAGE', msg)
    # *** TRANSFER PLASMA ***
    msg = """
        Transfer Plasma from Sample Loading to the 32 Deep Well Plate on the 
        Heater/Shaker.
    """
    logger.log('MESSAGE', msg)
    # Pickup tips from Tip Tray A Row 1.
    #upper_gantry.tip_pickup('A', 1)
    # Move to Sample Loading Rack A
    #upper_gantry.move_pipettor('sample_loading_tray4', use_drip_plate=False)
    # Aspirate 1 mL of Plasma.
    #upper_gantry.aspirate(950)
    # Move to Heater/Shaker Row 1.
    #upper_gantry.move_pipettor('heater_shaker_row1')
    # Dispense 1 mL of Plasma.
    #upper_gantry.dispense(1000)
    # Eject Tips in the Tip Transfer Tray Row 1.
    #upper_gantry.tip_eject('tip_transfer_tray', 1)
    # Pickup tips from Tip Tray A Row 2.
    #upper_gantry.tip_pickup('A', 2)
    # Move to the Sample Loading Rack B.
    #upper_gantry.move_pipettor('sample_loading_tray3', use_drip_plate=False)
    # Aspirate 1 mL of Plasma.
    #upper_gantry.aspirate(1000)
    # Move to the Heater/Shaker Row 2.
    #upper_gantry.move_pipettor('heater_shaker_row2')
    # Dispense 1 mL of plasma.
    #upper_gantry.dispense(1000)
    # Eject tips in the Tip Transfer Tray Row 3.
    #upper_gantry.tip_eject('tip_transfer_tray', 3)
    # *** BINDING ***
    logger.log('MESSAGE', 'Binding')
    # Pickup tips from the Tip Transfer Tray Row 1 (Tip Re-use Showcase).
    #upper_gantry.tip_pickup('tip_transfer_tray', 1)
    # Move to Reagent Cartridge A Row 1.
    #upper_gantry.move_pipettor('reagent_cartridge_tray4_row1', pipette_tip_type=1000)
    # Mix.
    #upper_gantry.mix(750, 750, 3)
    # Aspirate 935 uL of Binding Solution.
    #upper_gantry.aspirate(885)
    # Move to the Heater/Shaker Row 1.
    #upper_gantry.move_pipettor('heater_shaker_row1')
    # Dispense 935 uL of Binding Solution.
    #upper_gantry.dispense(935)
    # Mix Plasma and Binding Solution.
    #upper_gantry.mix(750, 750, 3)
    # Shake at 1500 RPM.
    #upper_gantry.move_relative('up', 500000, velocity='fast')
    #upper_gantry.shake(rpm=1500, shake_time=5, time_units='seconds')
    #upper_gantry.move_relative('down', 500000, velocity='fast')
    # *** POOLING ***
    logger.log('MESSAGE', 'Pooling')
    # Aspirate 1 mL of Sample.
    #upper_gantry.aspirate(950)
    # Predispense
    logger.log('MESSAGE', 'Predispense')
    #upper_gantry.move_pipettor('sample_loading_tray4')
    #upper_gantry.move_relative('up', 350000, velocity='fast')
    #delay(5, 'seconds')
    #upper_gantry.dispense(325)
    #delay(5, 'seconds')
    #upper_gantry.dispense(325)
    #delay(5, 'seconds')
    #upper_gantry.dispense(325)
    #upper_gantry.move_relative('right', 6000)
    # Move to the Mag Separator Row 1.
    #upper_gantry.move_pipettor('mag_separator_row1')
    # Dispense 1 mL of Sample.
    #upper_gantry.dispense(1000)
    # Allow Beads to bind.
    #delay(5, 'seconds')
    # Aspirate Supernatant.
    #upper_gantry.move_relative('up', 20000)
    #upper_gantry.aspirate(700)
    # Move to the Sample or Reagent Cartridge for Waste Disposal.
    #upper_gantry.move_pipettor('sample_loading_tray4')
    # Dispense Supernatant waste.
    #upper_gantry.dispense(750)
    #upper_gantry.tip_eject('tip_transfer_tray', 1)
    # ------------------------------------------------------------------------------
    # Pre-Amp (Minimal Showcase)
    # ------------------------------------------------------------------------------
    msg = """
        \n**************************************************************************
        Pre-Amp (Minimal Showcase)
        ******************************************************************************\n
    """
    logger.log('MESSAGE', msg)
    # Pickup 50 uL of tips.
    #upper_gantry.tip_pickup('A', 5)
    # Move to the Reagent Cartridge A Row X.
    #upper_gantry.move_pipettor('reagent_cartridge_tray4_row4', use_drip_plate=False)
    # Aspirate 15 uL of Water.
    #upper_gantry.aspirate(15)
    # Move to the Pre-Amp Thermocycler Row 1.
    #upper_gantry.move_pipettor('pcr_thermocycler_row1')
    # Dispense 15 uL of Water.
    #upper_gantry.dispense(20)
    # Move to the Mag Separator Row 1.
    #upper_gantry.move_pipettor('mag_separator_row1')
    # Aspirate 10 uL of cfDNA.
    #upper_gantry.aspirate(10)
    # Move to Pre-Amp Thermocycler Row 1.
    #upper_gantry.move_pipettor('pcr_thermocycler_row1')
    # Dispense 10 uL of cfDNA.
    #upper_gantry.dispense(15)
    # Mix 3-5 times.
    #upper_gantry.mix(50, 50, 3)
    # Tip eject in the Tip Transfer Tray.
    #upper_gantry.tip_eject('tip_transfer_tray', 2)
    # Pickup 50 uL tips.
    #upper_gantry.tip_pickup('A', 6)
    # Move to the Reagent Cartridge with Mineral Oil.
    #upper_gantry.move_pipettor('reagent_cartridge_tray4_row5', use_drip_plate=False)
    # Aspirate 25 uL of Mineral Oil.
    #upper_gantry.aspirate(25)
    # Move to Pre-Amp Thermocycler Row 1.
    #upper_gantry.move_pipettor('pcr_thermocycler_row1')
    # Dispense 25 uL of Mineral Oil slowly.
    #upper_gantry.dispense(30)
    # Thermocycler (5-7 Cycler).
    # Eject tips.
    #upper_gantry.tip_eject('tip_transfer_tray', 4)
    # ------------------------------------------------------------------------------
    # Droplet Generation  and Chip Loading(Minimal Showcase)
    # ------------------------------------------------------------------------------
    msg = """
        \n**************************************************************************
        Droplet Generation and Chip Loading (Minimal Showcase)
        ******************************************************************************\n
    """
    logger.log('MESSAGE', msg)
    # Generate Droplets.
    #dz = coordinates['deck_plate']['dg8']['dz']
    # Pickup 200 uL tips.
    #upper_gantry.tip_pickup('tip_transfer_tray', 5)
    # Aspirate 100 uL from Reagent Cartridge Row.
    #upper_gantry.move_pipettor('reagent_cartridge_tray4_row8', use_drip_plate=False, pipette_tip_type=200)
    #upper_gantry.aspirate(100)
    # Dispense 100 uL in the dg8 chip 100 channel
    #upper_gantry.move_pipettor('dg8_1000_100', use_drip_plate=False, pipette_tip_type=200)
    #upper_gantry.dispense(120)
    # Aspirate 24 uL from Reagent Cartridge Row.
    #upper_gantry.move_pipettor('reagent_cartridge_tray4_row8', use_drip_plate=False, pipette_tip_type=200)
    #upper_gantry.aspirate(24)
    # Dispense 24 uL in the dg8 chip 010 channel
    #upper_gantry.move_pipettor('dg8_1000_010', use_drip_plate=False, pipette_tip_type=200)
    #upper_gantry.dispense(31)
    #upper_gantry.tip_eject('tip_transfer_tray', 5)
    # Generate the droplets.
    #upper_gantry.move_pipettor('dg8_1000_001', use_drip_plate=False, pipette_tip_type=200)
    #upper_gantry.move_relative('down', dz)
    #upper_gantry.tip_pickup('tip_transfer_tray', 5)
    # Aspirate 40 uL from the dg8 001 channel.
    #upper_gantry.move_pipettor('dg8_1000_001', use_drip_plate=False, pipette_tip_type=200)
    # Aspirate 40 uL from the DG8 chips.
    #upper_gantry.aspirate(40)
    # Load the chip.
    #upper_gantry.move_pipettor('tray_out_location_tray1')
    #upper_gantry.dispense(50)
    #upper_gantry.tip_eject('tip_transfer_tray', 5)
    # ------------------------------------------------------------------------------
    # Chip Lidding.
    # ------------------------------------------------------------------------------
    msg = """
        \n**************************************************************************
        Chip Lidding
        ******************************************************************************\n
    """
    logger.log('MESSAGE', msg)
    # Move the lid to the chip.
    #upper_gantry.move_lid(4, 'D')
    # Get the pipettor out of the way.
    upper_gantry.move_pipettor('tip_trays_tray2_row1', use_drip_plate=False, use_z=False)
    # ------------------------------------------------------------------------------
    # Imaging (Minimal Showcase)
    # ------------------------------------------------------------------------------
    msg = """
        \n**************************************************************************
        Imaging (Minimal Showcase)
        ******************************************************************************\n
    """
    logger.log('MESSAGE', msg)
    # Close the tray.
    reader.close_tray('CD')
    # Lower the heater.
    reader.lower_heater('heater_d')
    # Move the imager.
    reader.move_reader('heater_d')
    # Image (Mock Showcase)
    reader.take_all_6_colors()
    timer_protocol.stop(__file__, __name__)