#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import morse_talk as mtalk
from generator import (PrintableSampleGeneratorApp,
                       LedSampleGeneratorApp,
                       ListenableSampleGeneratorApp)
from generator import _get_element_duration

def main():
    parser = argparse.ArgumentParser(description='Send morse code')
    parser.add_argument('-m', '--message', help='Message', default='SOS')
    parser.add_argument('-d', '--duration', help='Element duration', default=None, type=float)
    parser.add_argument('-s', '--speed', help="Speed in wpm (Words per minutes)", default=None, type=float)
    parser.add_argument('--with-sound', dest='sound', help="With sound", action='store_true')
    parser.add_argument('--with-led', dest='led', help="With LED connected to GPIO", action='store_true')
    parser.add_argument('--pin-out', dest='pin_out', help="GPIO pin number on which LED is connected", default=13, type=int)

    args = parser.parse_args()
    message = args.message
    element_duration = args.duration
    wpm = args.speed

    print("text : %r" % message)
    print("morse: %s" % mtalk.encode(message))
    print("bin  : %s" % mtalk.encode(message, encoding_type='binary'))
    print("")

    element_duration = _get_element_duration(element_duration, wpm)

    if args.sound:
        app = ListenableSampleGeneratorApp(message, element_duration)
    elif args.led:
        import pingo
        from pingo.parts.led import Led
        board = pingo.detect.get_board()
        led_pin = board.pins[args.pin_out]
        led = Led(led_pin)
        app = LedSampleGeneratorApp(message, element_duration, led=led)
    else:
        app = PrintableSampleGeneratorApp(message, element_duration)
    app.run()


if __name__ == '__main__':
    main()