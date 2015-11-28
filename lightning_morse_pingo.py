#!/usr/bin/env python

from __future__ import absolute_import

from morse_code_gen import MorseGenerator

#import atexit

import pingo
from pingo.parts.led import Led
import time

import logging

class LightingMorseGenerator(MorseGenerator):
    def __init__(self, *args, **kwargs):
        super(LightingMorseGenerator, self).__init__(*args, **kwargs)
        self.board = pingo.detect.get_board()
        #atexit.register(self.board.cleanup)

        led_pin = self.board.pins[13]
        self.led = Led(led_pin)
        self.led.off()

        self.unit = 0.3

    def on(self, nb, *args, **kwargs):
        self.led.on()
        time.sleep(nb * self.unit)

    def off(self, nb, *args, **kwargs):
        self.led.off()
        time.sleep(nb * self.unit)

    def close(self):
        self.led.off()
        self.board.cleanup()

def main():
    logging.basicConfig(level=logging.DEBUG)

    import argparse

    parser = argparse.ArgumentParser(description='Send morse code')
    parser.add_argument('--msg', help='Message', default='MORSE CODE')
    args = parser.parse_args()
    message = args.msg
    
    morse_gen = LightingMorseGenerator()
    morse_gen.send(message)
    morse_gen.close()
    print("")

if __name__ == '__main__':
    main()