
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
        'dg8_left': {
            0: [-244650, -166000, -1459000, 0],
            1: [0,0,0,0],
            2: [0,0,0,0],
            3: [0,0,0,0]
            },
        'sample_loading' : {
            0 : [0,0,0,0],
            1 : [-271750,-1478750,-1100000,-370000], 
            2 : [-271750,-1068750,-1100000,-370000],
            3 : [-271750,-673750,-1100000,-370000]
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
                0 : [-251750,-1426000,-950000,-520000], # z = -950000
                1 : [-245250,-1426000,-950000,-520000], 
                2 : [-238750,-1426000,-850000,0],
                3 : [-233750,-1426000,-743000,0],
                4 : [-228250,-1426000,-743000,0],
                5 : [-223250,-1426000,-743000,0],
                6 : [-217750,-1426000,-743000,0],
                7 : [-212250,-1426000,-743000,0],
                8 : [-207250,-1426000,-743000,0],
                9 : [0,0,-850000,0],
                10 : [0,0,-950000,0],
                11 : [-188750,-1426000,-950000,-520000]
                },
            2 : { #B
                0 : [-251750,-1010000,-950000,-520000], # z = -950000
                1 : [-245250,-1010000,-950000,-520000], 
                2 : [0,0,0,0],
                3 : [0,0,0,0],
                4 : [0,0,0,0],
                5 : [0,0,0,0],
                6 : [0,0,0,0],
                7 : [0,0,0,0],
                8 : [0,0,0,0],
                9 : [0,0,0,0],
                10 : [0,0,0,0],
                11 : [-188750,-1010000,-950000,-520000]
                },
            3 : { #A
                0 : [0,0,0,0],
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
                0 : [-169750,-1431000,-1489000,0],
                1 : [-164250,-1431000,-1487000,0],
                2 : [-159250,-1431000,-1489000,0],
                3 : [-153750,-1431000,-1489000,0],
                4 : [-148250,-1431000,-1489000,0],
                5 : [-142750,-1431000,-1489000,0],
                6 : [-137250,-1431000,-1489000,0],
                7 : [-131750,-1431000,-1489000,0],
                8 : [-126250,-1431000,-1489000,0],
                9 : [-121250,-1431000,-1489000,0],
                10 : [-115750,-1431000,-1489000,0],
                11 : [-110250,-1431000,-1489000,0]
                },
            2 : { #B
                0 : [-169750,-1007000,-1489000,0], # <---------------------------------- HERE
                1 : [-164250,-1007000,-1489000,0],
                2 : [-159250,-1007000,-1489000,0],
                3 : [-153750,-1007000,-1487000,0],
                4 : [-148250,-1007000,-1489000,0],
                5 : [-142750,-1007000,-1489000,0],
                6 : [-137250,-1007000,-1489000,0],
                7 : [-131750,-1007000,-1489000,0],
                8 : [-126250,-1007000,-1489000,0],
                9 : [-121250,-1007000,-1488000,0],
                10 : [-115750,-1007000,-1489000,0],
                11 : [-110250,-1007000,-1489000,0]
                },
            3 : { #A
                0 : [-169750,-610750,-1489000,0],
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
            },
        'quant_strip' : {
            0 : [0,0,0,0],
            1 : [0,0,0,0],
            2 : [0,0,0,0],
            3 : [0,0,0,0]
            },
        'assay_strips' : {
            0 : [0,0,0,0],
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
            0 : [-390050,-902000,-605000,-490000], #(-396300, -936000, -605000, -510000)
            1 : [-373050,-902000,-605000,-490000], #(-379300, -936000, -605000, -510000)
            2 : [-354050,-902000,-605000,-490000],
            3 : [-337050,-902000,-605000,-490000],
            },
        'mag_separator' : {
            0 : [-392250,-1386000,-775000,0],
            1 : [-386250,-1386000,-775000,0],
            2 : [-380750,-1386000,-775000,0],
            3 : [-376250,-1386000,-775000,0], # drip plate = -600000
            4 : [-369750,-1386000,-775000,0],
            5 : [-364250,-1386000,-775000,0],
            6 : [-358750,-1386000,-775000,0],
            7 : [-353250,-1386000,-775000,0],
            8 : [-347750,-1386000,-775000,0],
            9 : [-342250,-1386000,-775000,0],
            10 : [-336750,-1386000,-775000,0],
            11 : [-331250,-1386000,-775000,0]
            },
        'tip_transfer_tray' : {
            0 : [-466750,-1403000,-1315000,0],
            1 : [-460750,-1403000,-1315000,0],
            2 : [0,0,0,0],
            3 : [0,0,0,0],
            4 : [0,0,0,0],
            5 : [0,0,0,0],
            6 : [0,0,0,0],
            7 : [0,0,0,0],
            'chips': {
                'microwells': {
                    0: [0,0,0,0],
                    1: [0,0,0,0],
                    2: [0,0,0,0],
                    3: [-428250,-1403000,-330000,-1198000],
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
            0 : [-446050,-296000,-890000,-370000],
            1 : [-440550,-296000,-890000,-370000],
            2 : [-435050,-296000,-890000,-370000],
            3 : [-429550,-296000,-890000,-370000],
            4 : [-424050,-296000,-890000,-370000],
            5 : [-418550,-296000,-890000,-370000],
            6 : [-413050,-296000,-890000,-370000],
            7 : [-407550,-296000,-890000,-370000],
            8 : [-402050,-296000,-890000,-370000],
            9 : [-396300,-296000,-890000,-370000],
            10 : [-391050,-296000,-890000,-370000],
            11 : [-386750,-296000,-890000,-370000]
            },
        'tray_out_location' : {
            0 : [0, -1739000, -716000,0], #(-2300, -1773000, -716000, 0), #[-1800, -1775000, -707000,0]
            1 : [0,-1275000,-749000,0],
            2 : [0,0,0,0],
            3 : [0,0,0,0],
            'chips': {
                    0: [-12250,-1747850,-552000,-1198000], # Tray CD (D)
                    1: [0,0,0,0], # Tray CD (C)
                    2: [0,0,0,0], # Tray AB (B)
                    3: [0,0,0,0], # Tray AB (A)
                },
            },
        'tray_in_location' : {},
        'lid_tray': {
            0: [-428450,-936000,-235000,-1198000],
            1: [-428450,-936000,-265000,-1198000],
            2: [-428450,-936000,-295000,-1198000],
            3: [-428450,-936000,-325000,-1198000],
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
    'heater_4'
    ]