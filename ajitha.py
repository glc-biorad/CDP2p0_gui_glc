'''
'''

from utils import delay

class Ajitha():
    def __init__(self):
        a = 1

    def run(self, meerstetter, n_cycles=45):
        meerstetter.change_temperature(4, 84, block=False)
        delay(5, 'minutes')
        for i in range(n_cycles):
            meerstetter.change_temperature(4, 84, block=False)
            delay(40, 'seconds')
            meerstetter.change_temperature(4, 55, block=False)
            delay(80, 'seconds')
        meerstetter.change_temperature(4, 30, block=False)