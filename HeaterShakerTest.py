import serial
import time
from qinstruments import BioShake3000T

if __name__ == '__main__':
    print("Testing BioShake 3000-T elm")

    # Initialize the Heater/Shaker object.
    bs3000T = BioShake3000T()

    # Initialization Tests
    run_test = True if input("\n\aWould you like to test Initialization [y/n]?\n") == 'y' else False
    if run_test:
        print("Info: {0}".format(bs3000T.info()))
        print("Version: {0}".format(bs3000T.getVersion()))
        print("Description: {0}".format(bs3000T.getDescription()))
        print("Reset Device:")
        bs3000T.resetDevice()
        print("Get Error List: {0}".format(bs3000T.getErrorList()))
        print("\nDisabling LED:")
        bs3000T.disableCLED()
        print("\nEnabling LED:")
        bs3000T.enableCLED()

    # ECO mode Tests
    run_test = True if input("\n\aWould you like to test ECO mode [y/n/]?\n") == 'y' else False
    if run_test:
        print("\nSet ECO mode:")
        bs3000T.setEcoMode()
        print("\nLeave ECO mode:")
        bs3000T.leaveEcoMode()

    # Shaking & Homing Tests
    run_test = True if input("\n\aWould you like to test shaking [y/n]?\n") == 'y' else False
    if run_test:
        print("Shake for 3 seconds:\n")
        bs3000T.shakeOn(mixing_speed_rpm=50)
        time.sleep(3)
        print("Shaking will now stop (takes 6 seconds)...\n")
        bs3000T.shakeOff()
        print("Shake for 2 seconds:\n")
        bs3000T.shakeOnWithRuntime(runtime=2, mixing_speed_rpm=50)
        print("Shake Go Home:\n")
        bs3000T.shakeGoHome()

    # Temperature Control Tests
    run_test = True if input("\n\aWould you like to test temperature control [y/n]?\n") == 'y' else False
    if run_test:
        print("Current Temperature Target ({0}C): {1}\n".format(u"\u00b0", bs3000T.getTempTarget()))
        bs3000T.tempOn()
        print("Temp Control: ON")
        print("Temp State (int): {0}".format(bs3000T.getTempState()))
        print("Temp State (string): {0}\n".format(bs3000T.getTempStateAsString()))
        bs3000T.tempOff()
        print("Temp Control: OFF")
        print("Temp State (int): {0}".format(bs3000T.getTempState()))
        print("Temp State (string): {0}\n".format(bs3000T.getTempStateAsString()))
        print("Changing temperature to 30 " + u"\u00b0" + "C\n")
        bs3000T.changeTemp(temp=30)
        print("Holding temperature at 30 " + u"\u00b0" + "C for 1 minute...\n")
        for i in range(6):
            time.sleep(10)
            print("\tCurrent Temperature ({0}C): {1}".format(u"\u00b0", bs3000T.getTempActual()))
            print(f"\t{60-(i+1)*10} seconds left")
            print("\tTemp State (string): {0}\n".format(bs3000T.getTempStateAsString()))
        print("Changing temperature to 28 " + u"\u00b0" + "C\n")
        bs3000T.changeTemp(temp=28)

    # ELM Control Tests
    run_test = True if input("\n\aWould you like to run ELM control tests [y/n]?\n") == 'y' else False
    if run_test:
        print(f"Current ELM State (int): {bs3000T.getElmState()}")
        print(f"Current ELM State (string): {bs3000T.getElmStateAsString()}\n")
        print("Setting ELM to it's Locked State:")
        bs3000T.setElmLockPos()
        print(f"Current ELM State (int): {bs3000T.getElmState()}")
        print(f"Current ELM State (string): {bs3000T.getElmStateAsString()}\n")
        print("Setting ELM to it's Unlocked State:")
        bs3000T.setElmUnlockPos()
        print(f"Current ELM State (int): {bs3000T.getElmState()}")
        print(f"Current ELM State (string): {bs3000T.getElmStateAsString()}\n")