#!/usr/bin/env python

from __future__ import absolute_import

from morse_code_gen import MorseGenerator

import pingo
from pingo.parts.led import Led
import time

class LightingMorseGenerator(MorseGenerator):
    def __init__(self, *args, **kwargs):
        super(LightingMorseGenerator, self).__init__(*args, **kwargs)
        self.board = pingo.detect.get_board()

        led_pin = self.board.pins[13]
        self.led = Led(led_pin)
        self.led.off()

        self.unit = 0.1

    def on(self, nb, *args, **kwargs):
        self.led.on()
        time.sleep(nb * self.unit)

    def off(self, nb, *args, **kwargs):
        self.led.off()
        time.sleep(nb * self.unit)

    def close(self):
        self.board.cleanup()

def main(message="MORSE CODE"):
    print(message)
    morse_gen = LightingMorseGenerator()
    morse_gen.send(message)
    print("")

if __name__ == '__main__':
    main()