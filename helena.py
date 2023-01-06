'''
'''

from reader import Reader
from logger import Logger
from utils import delay

def take_6_color_image(reader, filename):
    logger = Logger(__file__, __name__)
    logger.log('LOG-START', "Taking a 6 color image for Helena, we assume the chip is in focus for this.")
    # Alexa405
    logger.log('MESSAGE', "Taking the image with Alexa405")
    reader.filter_wheel_test(color='ALEXA405', exposure=999999, filename=filename)
    # Cy5
    logger.log('MESSAGE', "Taking the image with Cy5")
    reader.filter_wheel_test(color='CY5', exposure=999999, filename=filename)
    # Cy55
    logger.log('MESSAGE', "Taking the image with Cy55")
    reader.filter_wheel_test(color='CY55', exposure=999999, filename=filename)
    # Fam
    logger.log('MESSAGE', "Taking the image with FAM")
    reader.filter_wheel_test(color='FAM', exposure=999999, filename=filename)
    # Hex
    logger.log('MESSAGE', "Taking the image with HEX")
    reader.filter_wheel_test(color='HEX', exposure=999999, filename=filename)
    # Atto
    logger.log('MESSAGE', "Taking the image with Atto")
    reader.filter_wheel_test(color='ATTO', exposure=999999, filename=filename)
    logger.log('LOG-END', "Took images.")