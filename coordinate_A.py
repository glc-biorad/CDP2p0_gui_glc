'''
DESCRIPTION:
This module contains Coordinate.

NOTES:

AUTHOR:
G.LC

AFFILIATION:
Bio-Rad, CDG, Advanced-Tech Team

CREATED ON:
8/30/2022
'''

import sys

class Coordinate():
    # Public variables.
    x = None
    y = None
    z = None

    # Private variables.

    def __init__(self, location):
        if type(location) == list:
            self.x = location[0]
            self.y = location[1]
            self.z = location[2]

    def move(self, location):
        if type(location) == list:
            self.x = location[0]
            self.y = location[1]
            self.z = location[2]

# The coordinates are in units of microSteps
coordinates = {
    'reader' : {
        'heater_1' : [-300000,-1100000,-300000,0],
        'heater_2' : [-300000,-850000,-295000,0],
        'heater_3' : [0,0,0,0],
        'heater_4' : [0,0,0,0],
        'filter_wheel_home': [0,0,0,0],
        'filter_wheel_alexa405': [0,0,0,-47000],
        'filter_wheel_cy55': [0,0,0,-4000], 
        'filter_wheel_cy5': [0,0,0,-13000],
        'filter_wheel_atto': [0,0,0,-21000], #21500
        'filter_wheel_hex': [0,0,0,-30000],
        'filter_wheel_fam': [0,0,0,-37000],
        },
    'deck_plate' : {
        'custom': [-396300,-936000,-605000,0],  # (-396300, -936000, -605000, -510000)
        'test_0' : [-2500, -1775000, 0, 0],
        'test_1' : [-140000, -337000, -300000, 0],
        'dg8': {
            'dz' : 362000,
            0: {
                0: [-259900,-200000,-1076000,0],
                1: [-255400,-200000,-1095000,0],
                2: [-250900,-200000,-1096000,0], #[-250900, -200000, -1459000, 0], comment out is position without tips, only heads
                },
            1: {
                0: [-241400,-200000,-1076000,0],
                1: [-236900,-200000,-1095000,0],
                2: [-232400,-200000,-1096000,0]
                },
            2: {
                0: [-222900,-200000,-1076000,0],
                1: [-218900,-200000,-1095000,0],
                2: [-214400,-200000,-1096000,0]
                },
            3: {
                0: [0,0,0,0],
                1: [0,0,0,0],
                2: [0,0,0,0]
                },
            },
        'dg8_left': {
            0: [-250900, -200000, -1459000, 0], #[-250900,-200000,-775000,0] # commented is 1000 uL
            1: [0,0,0,0],
            2: [0,0,0,0],
            3: [0,0,0,0]
            },
        'sample_loading' : {
            0 : [0,0,0,0],
            1 : [-278000,-1485000,-1100000,-400000], 
            2 : [-278000,-1075000,-1100000,-400000],
            3 : [-278000,-680000,-1100000,-400000]
            },
        'reagent_cartridge' : {
            0 : { # reagent cartridge #D
                0 : [0,0,0,0], # reagent cartridge 0 row 0 [x,y,z,drip_plate]
                1 : [0,0,0,0],
                2 : [0,0,0,0],
                3 : [0,0,0,0],
                4 : [0,0,0,0],
                5 : [0,0,0,0],
                6 : [0,0,0,0],
                7 : [0,0,0,0],
                8 : [0,0,0,0],
                9 : [0,0,0,0],
                10 : [0,0,0,0],
                11 : [0,0,0,0]
                },
            1 : { # reagent cartridge front 2 #C
                0 : [-258000,-1460000,-950000,-550000], # z = -950000
                1 : [-251500,-1460000,-950000,-550000], 
                2 : [-245000,-1460000,-850000,0],
                3 : [-241000,-1460000,-755000,0],
                4 : [-235600,-1460000,-755000,0],
                5 : [-230200,-1460000,-755000,0],
                6 : [-224800,-1460000,-755000,0],
                7 : [-219400,-1460000,-755000,0],
                8 : [-214000,-1460000,-755000,0],
                9 : [208600,-1460000,-850000,0],
                10 : [0,-1460000,-950000,0],
                11 : [-195000,-1460000,-950000,-550000]
                },
            2 : { #B
                0 : [-258000,-1045000,-950000,-550000], # z = -950000
                1 : [-251500,-1045000,-950000,-550000], 
                2 : [0,0,0,0],
                3 : [0,0,0,0],
                4 : [0,0,0,0],
                5 : [0,0,0,0],
                6 : [0,0,0,0],
                7 : [0,0,0,0],
                8 : [0,0,0,0],
                9 : [0,0,0,0],
                10 : [0,0,0,0],
                11 : [0,0,0,0]
                },
            3 : { # A
                0 : [-258000,-630000,-947000,-550000], # z = -950000
                1 : [-251500,-630000,-947000,-550000], 
                2 : [-245000,-630000,-847000,0],
                3 : [-240800,-630000,-745500,0],
                4 : [-235600,-630000,-761500,0],
                5 : [-230700,-630000,-745500,0],
                6 : [-225300,-630000,-745500,0],
                7 : [-219900,-630000,-745500,0],
                8 : [-214500,-630000,-745500,0],
                9 : [-208600,-630000,-847000,0],
                10 : [-201500,-630000,-947000,0],
                11 : [-195000,-630000,-947000,-550000]
                },
            },
        'tip_trays' : {
            0 : { # tip tray 0 (D)
                0 : [0,0,0,0], # tip tray 0 row 0 [x,y,z,drip_plate]
                1 : [0,0,0,0],
                2 : [0,0,0,0],
                3 : [0,0,0,0],
                4 : [0,0,0,0],
                5 : [0,0,0,0],
                6 : [0,0,0,0],
                7 : [0,0,0,0],
                8 : [0,0,0,0],
                9 : [0,0,0,0],
                10 : [0,0,0,0],
                11 : [0,0,0,0]
                },
            1 : { #C
                0 : [-176000,-1465000,-1479000,0],
                1 : [-170500,-1465000,-1477000,0],
                2 : [-165500,-1465000,-1479000,0],
                3 : [-160000,-1465000,-1479000,0],
                4 : [-154500,-1465000,-1479000,0],
                5 : [-149000,-1465000,-1479000,0],
                6 : [-143500,-1465000,-1479000,0],
                7 : [-138000,-1465000,-1479000,0],
                8 : [-132500,-1465000,-1479000,0],
                9 : [-127500,-1465000,-1479000,0],
                10 : [-122000,-1465000,-1479000,0],
                11 : [-116500,-1465000,-1479000,0]
                },
            2 : { #B
                0 : [-176300,-1041000,-1479000,0], # <---- HERE
                1 : [-170800,-1041000,-1479000,0],
                2 : [-165300,-1041000,-1479000,0],
                3 : [-159800,-1041000,-1477000,0],
                4 : [-154300,-1041000,-1479000,0],
                5 : [-148800,-1041000,-1479000,0],
                6 : [-143800,-1041000,-1479000,0],
                7 : [-138300,-1041000,-1479000,0],
                8 : [-132800,-1041000,-1479000,0],
                9 : [-127300,-1041000,-1478000,0],
                10 : [-121800,-1041000,-1479000,0],
                11 : [-116300,-1041000,-1479000,0]
                },
            3 : { #A
                0 : [-176050,-628000,-1516000,0],
                1 : [-170550,-628000,-1516000,0],
                2 : [-165050,-628000,-1516000,0],
                3 : [-159550,-628000,-1516000,0],
                4 : [-154250,-628000,-1516000,0],
                5 : [-148950,-628000,-1516000,0],
                6 : [-143650,-628000,-1516000,0],
                7 : [-138150,-628000,-1516000,0],
                8 : [-132750,-628000,-1516000,0],
                9 : [-127350,-628000,-1516000,0],
                10 : [-121950,-628000,-1516000,0],
                11 : [-116550,-628000,-1516000,0],
                },
            },
        'quant_strip' : {
            0 : [0,0,0,0],
            1 : [0,0,0,0],
            2 : [0,0,0,0],
            3 : [0,0,0,0]
            },
        'assay_strip' : {
            0 : [-477750,-1887000,-702000,0],
            1 : [0,0,0,0],
            2 : [0,0,0,0],
            3 : [0,0,0,0],
            4 : [0,0,0,0],
            5 : [0,0,0,0],
            6 : [0,0,0,0],
            7 : [0,0,0,0]
            },
        'staging_deck' : {},
        'rear_space_1' : {},
        'heater_shaker' : {
            0 : [-396300,-943000,-631000,-490000], #(-396300, -936000, -605000, -510000)
            1 : [-379300,-943000,-631000,-490000], #(-379300, -936000, -605000, -510000)
            2 : [-360300,-943000,-631000,-490000],
            3 : [-343300,-943000,-631000,-490000],
            },
        'mag_separator' : {
            0 : [-398900,-1420000,-775000,0],
            1 : [-393500,-1420000,-775000,0],
            2 : [-388100,-1420000,-775000,0],
            3 : [-382700,-1420000,-775000,0], # drip plate = -600000
            4 : [-377300,-1420000,-775000,0],
            5 : [-371900,-1420000,-775000,0],
            6 : [-366500,-1420000,-775000,0],
            7 : [-361100,-1420000,-775000,0],
            8 : [-355700,-1420000,-775000,0],
            9 : [-350300,-1420000,-775000,0],
            10 : [-344900,-1420000,-775000,0],
            11 : [-339500,-1420000,-775000,0]
            },
        'tip_transfer_tray' : {
            0 : [-473000,-1437000,-1280000,0],
            1 : [-467600,-1437000,-1280000,0],
            2 : [-462200,-1437000,-1280000,0],
            3 : [-456800,-1437000,-1280000,0],
            4 : [-451400,-1437000,-1280000,0],
            5 : [-446000,-1437000,-1280000,0],
            6 : [-440600,-1437000,-1280000,0],
            7 : [-435200,-1437000,-1280000,0],
            'chips': {
                'microwells': {
                    0: [0,0,0,0],
                    1: [0,0,0,0],
                    2: [0,0,0,0],
                    3: [-434500,-1437000,-340000,-1198000], #330000
                    },
                'droplets': {
                    0: [0,0,0,0],
                    1: [0,0,0,0],
                    2: [0,0,0,0],
                    3: [0,0,0,0],
                    },
                }
            },
        'chiller' : {},
        'pre_amp' : {},
        'rna_heater' : {
            0 : [0,0,0,0],
            1 : [0,0,0,0],
            2 : [0,0,0,0],
            3 : [0,0,0,0]
            },
        'pcr_thermocycler' : {
            0 : [-452300,-330000,-890000,-400000],
            1 : [-446800,-330000,-890000,-400000],
            2 : [-441300,-330000,-890000,-400000],
            3 : [-435800,-330000,-890000,-400000],
            4 : [-430300,-330000,-890000,-400000],
            5 : [-424800,-330000,-890000,-400000],
            6 : [-419300,-330000,-890000,-400000],
            7 : [-413800,-330000,-890000,-400000],
            8 : [-408300,-330000,-890000,-400000],
            9 : [-402800,-330000,-890000,-400000],
            10 : [-397300,-330000,-890000,-400000],
            11 : [-393000,-330000,-890000,-400000]
            },
        'tray_out_location' : {
            0 : [-68500,-1778500,-750000,0], #[-2300, -1773000, -716000,0] <-- Droplets , [-65300,-1773000,-700000,0] <-- microweels
            1 : [-2302,-1758500,-750000,0],
            2 : [0,0,0,0],
            3 : [0,0,0,0],
            'nipt': {
                'D': [-68500,-1778500,-750000,0],
                },
            'quant': {
                'D': [-2502,-1778500,-750000,0],
                },
            'ff': {
                'D': [-2302,-1758500,-750000,0],
                },
            'chips': {
                    0: [-18500,-1781750,-552000,-1198000], # Tray CD (D)
                    1: [0,0,0,0], # Tray CD (C)
                    2: [0,0,0,0], # Tray AB (B)
                    3: [0,0,0,0], # Tray AB (A)
                },
            },
        'tray_in_location' : {},
        'lid_tray': {
            0: [-435300,-970000,-235000,-1198000],
            1: [-435300,-970000,-265000,-1198000],
            2: [-435300,-970000,-295000,-1198000],
            3: [-435300,-970000,-328000,-1198000],
            }
        }
    }

coordinate_names = [
    'home',
    'custom',
    'test_0',
    'test_1',
    'microwells_chip_1',
    'microwells_chip_2',
    'microwells_chip_3',
    'microwells_chip_4',
    'droplets_chip_1',
    'droplets_chip_2',
    'droplets_chip_3',
    'droplets_chip_4',
    'tip_trays_trayA_row1',
    'tip_trays_trayA_row2',
    'tip_trays_trayA_row3',
    'tip_trays_trayA_row4',
    'tip_trays_trayA_row5',
    'tip_trays_trayA_row6',
    'tip_trays_trayA_row7',
    'tip_trays_trayA_row8',
    'tip_trays_trayA_row9',
    'tip_trays_trayA_row10',
    'tip_trays_trayA_row11',
    'tip_trays_trayA_row12',
    'tip_trays_tray1_row1',
    'tip_trays_tray1_row2',
    'tip_trays_tray1_row3',
    'tip_trays_tray1_row4',
    'tip_trays_tray1_row5',
    'tip_trays_tray1_row6',
    'tip_trays_tray1_row7',
    'tip_trays_tray1_row8',
    'tip_trays_tray1_row9',
    'tip_trays_tray1_row10',
    'tip_trays_tray1_row11',
    'tip_trays_tray1_row12',
    'tip_trays_tray2_row1',
    'tip_trays_tray2_row2',
    'tip_trays_tray2_row3',
    'tip_trays_tray2_row4',
    'tip_trays_tray2_row5',
    'tip_trays_tray2_row6',
    'tip_trays_tray2_row7',
    'tip_trays_tray2_row8',
    'tip_trays_tray2_row9',
    'tip_trays_tray2_row10',
    'tip_trays_tray2_row11',
    'tip_trays_tray2_row12',
    'tip_trays_tray3_row1',
    'tip_trays_tray3_row2',
    'tip_trays_tray3_row3',
    'tip_trays_tray3_row4',
    'tip_trays_tray3_row5',
    'tip_trays_tray3_row6',
    'tip_trays_tray3_row7',
    'tip_trays_tray3_row8',
    'tip_trays_tray3_row9',
    'tip_trays_tray3_row10',
    'tip_trays_tray3_row11',
    'tip_trays_tray3_row12',
    'tip_trays_tray4_row1',
    'tip_trays_tray4_row2',
    'tip_trays_tray4_row3',
    'tip_trays_tray4_row4',
    'tip_trays_tray4_row5',
    'tip_trays_tray4_row6',
    'tip_trays_tray4_row7',
    'tip_trays_tray4_row8',
    'tip_trays_tray4_row9',
    'tip_trays_tray4_row10',
    'tip_trays_tray4_row11',
    'tip_trays_tray4_row12',
    'tip_transfer_tray_row1',
    'tip_transfer_tray_row2',
    'tip_transfer_tray_row3',
    'tip_transfer_tray_row4',
    'tip_transfer_tray_row5',
    'tip_transfer_tray_row6',
    'tip_transfer_tray_row7',
    'tip_transfer_tray_row8',
    'reagent_cartridge_tray1_row1',
    'reagent_cartridge_tray1_row2',
    'reagent_cartridge_tray1_row3',
    'reagent_cartridge_tray1_row4',
    'reagent_cartridge_tray1_row5',
    'reagent_cartridge_tray1_row6',
    'reagent_cartridge_tray1_row7',
    'reagent_cartridge_tray1_row8',
    'reagent_cartridge_tray1_row9',
    'reagent_cartridge_tray1_row10',
    'reagent_cartridge_tray1_row11',
    'reagent_cartridge_tray1_row12',
    'reagent_cartridge_tray2_row1',
    'reagent_cartridge_tray2_row2',
    'reagent_cartridge_tray2_row3',
    'reagent_cartridge_tray2_row4',
    'reagent_cartridge_tray2_row5',
    'reagent_cartridge_tray2_row6',
    'reagent_cartridge_tray2_row7',
    'reagent_cartridge_tray2_row8',
    'reagent_cartridge_tray2_row9',
    'reagent_cartridge_tray2_row10',
    'reagent_cartridge_tray2_row11',
    'reagent_cartridge_tray2_row12',
    'reagent_cartridge_tray3_row1',
    'reagent_cartridge_tray3_row2',
    'reagent_cartridge_tray3_row3',
    'reagent_cartridge_tray3_row4',
    'reagent_cartridge_tray3_row5',
    'reagent_cartridge_tray3_row6',
    'reagent_cartridge_tray3_row7',
    'reagent_cartridge_tray3_row8',
    'reagent_cartridge_tray3_row9',
    'reagent_cartridge_tray3_row10',
    'reagent_cartridge_tray3_row11',
    'reagent_cartridge_tray3_row12',
    'reagent_cartridge_tray4_row1',
    'reagent_cartridge_tray4_row2',
    'reagent_cartridge_tray4_row3',
    'reagent_cartridge_tray4_row4',
    'reagent_cartridge_tray4_row5',
    'reagent_cartridge_tray4_row6',
    'reagent_cartridge_tray4_row7',
    'reagent_cartridge_tray4_row8',
    'reagent_cartridge_tray4_row9',
    'reagent_cartridge_tray4_row10',
    'reagent_cartridge_tray4_row11',
    'reagent_cartridge_tray4_row12',
    'heater_shaker_row1',
    'heater_shaker_row2',
    'heater_shaker_row3',
    'heater_shaker_row4',
    'mag_separator_row1',
    'mag_separator_row2',
    'mag_separator_row3',
    'mag_separator_row4',
    'mag_separator_row5',
    'mag_separator_row6',
    'mag_separator_row7',
    'mag_separator_row8',
    'tray_out_location_tray1',
    'tray_out_location_tray2',
    'tray_out_location_tray3',
    'tray_out_location_tray4',
    'tray_out_location_chip1',
    'tray_out_location_chip2',
    'tray_out_location_chip3',
    'tray_out_location_chip4',
    'pcr_thermocycler_row1',
    'pcr_thermocycler_row2',
    'pcr_thermocycler_row3',
    'pcr_thermocycler_row4',
    'pcr_thermocycler_row5',
    'pcr_thermocycler_row6',
    'pcr_thermocycler_row7',
    'pcr_thermocycler_row8',
    'pcr_thermocycler_row9',
    'pcr_thermocycler_row10',
    'pcr_thermocycler_row11',
    'pcr_thermocycler_row12',
    'sample_loading_tray1',
    'sample_loading_tray2',
    'sample_loading_tray3',
    'sample_loading_tray4',
    'lid1',
    'lid2',
    'lid3',
    'lid4',
    'heater_1',
    'heater_2',
    'heater_3',
    'heater_4',
    'dg8_1000_100',
    'dg8_1000_010',
    'dg8_1000_001',
    'dg8_0100_100',
    'dg8_0100_010',
    'dg8_0100_001',
    'dg8_0010_100',
    'dg8_0010_010',
    'dg8_0010_001',
    'dg8_0001_100',
    'dg8_0001_010',
    'dg8_0001_001',
    'assay_strip_row1',
    'assay_strip_row2',
    'assay_strip_row3',
    'assay_strip_row4',
    'assay_strip_row5',
    'assay_strip_row6',
    'assay_strip_row7',
    'assay_strip_row8',
    'tray_out_location_nipt_D',
    'tray_out_location_ff_D',
    'tray_out_location_quant_D',
    ]