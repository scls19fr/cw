#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import morse_talk as mtalk
from generator import (_get_element_duration, 
                        TRUE, FALSE, MorseCodeGenerator)

from abc import ABCMeta, abstractmethod

class SampleGeneratorApp(object):
    __metaclass__ = ABCMeta

    def __init__(self, message, element_duration, wpm):
        self.message = message
        self.element_duration = element_duration
        self.wpm = wpm

        print("text : %r" % message)
        print("morse: %s" % mtalk.encode(message))
        print("bin  : %s" % mtalk.encode(message, encoding_type='binary'))
        print("")

        self.t0 = datetime.datetime.utcnow()

        self._generator = MorseCodeGenerator()
        
        #self._generator.set_callback_on(on, [self.t0])
        #self._generator.set_callback_off(off, [self.t0])

        self._generator.set_callback_on(self.on_ON, [self.t0])
        self._generator.set_callback_off(self.on_OFF, [self.t0])

    @abstractmethod
    def on_ON(self, duration):
        pass

    @abstractmethod
    def on_OFF(self, duration):
        pass

    def run(self):
        self._generator.send(self.message, element_duration=self.element_duration, wpm=self.wpm)

class PrintableSampleGeneratorApp(SampleGeneratorApp):
    def __init__(self, *args, **kwargs):
        super(PrintableSampleGeneratorApp, self).__init__(*args, **kwargs)

    def on_ON(self, duration, t0):
        t = datetime.datetime.utcnow()
        td = t - t0
        state = TRUE
        print("%s %s %s" % (td, state, duration))

    def on_OFF(self, duration, t0):
        t = datetime.datetime.utcnow()
        td = t - t0
        state = FALSE
        print("%s %s %s" % (td, state, duration))

class ListenableSampleGeneratorApp(SampleGeneratorApp):
    def __init__(self, *args, **kwargs):
        super(ListenableSampleGeneratorApp, self).__init__(*args, **kwargs)
        print("sound enabled")
        print("")
        raise NotImplementedError("ToDo")

    def on_ON(self, duration, t0):
        t = datetime.datetime.utcnow()
        td = t - t0
        state = TRUE
        print("%s %s %s" % (td, state, duration))

    def on_OFF(self, duration, t0):
        t = datetime.datetime.utcnow()
        td = t - t0
        state = FALSE
        print("%s %s %s" % (td, state, duration))

class LedSampleGeneratorApp(SampleGeneratorApp):
    def __init__(self, *args, **kwargs):
        self._led = kwargs.pop('led')
        super(LedSampleGeneratorApp, self).__init__(*args, **kwargs)

    def on_ON(self, duration, t0):
        t = datetime.datetime.utcnow()
        td = t - t0
        state = TRUE
        print("%s %s %s" % (td, state, duration))
        self._led.on()

    def on_OFF(self, duration, t0):
        t = datetime.datetime.utcnow()
        td = t - t0
        state = FALSE
        print("%s %s %s" % (td, state, duration))
        self._led.off()

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

    if args.sound:
        app = ListenableSampleGeneratorApp(message, element_duration, wpm)
    elif args.led:
        import pingo
        from pingo.parts.led import Led
        board = pingo.detect.get_board()
        led_pin = board.pins[args.pin_out]
        led = Led(led_pin)
        app = LedSampleGeneratorApp(message, element_duration, wpm, led=led)
    else:
        app = PrintableSampleGeneratorApp(message, element_duration, wpm)
    app.run()


if __name__ == '__main__':
    main()