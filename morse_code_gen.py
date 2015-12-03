#!/usr/bin/env python

from __future__ import absolute_import

import morse_talk as mtalk
import sys

FALSE = '0'
TRUE = '1'

import logging
logger = logging.getLogger(__name__)

class MorseGenerator(object):
    def __init__(self):
        self._on_callback = lambda *args: args
        self._off_callback = lambda *args: args
        #self._on_callback = lambda: None
        #self._off_callback = lambda: None

    def _feed(self, message):
        self.bin = mtalk.encode(message, encoding_type='binary')
        logger.debug(self.bin)
        self.lst_bits_nb = self._get_list_of_nb_of_same_bit(self.bin)
        self.lst_bits_ref = [bit for _, bit, _ in self._bit_generator(self.lst_bits_nb)]
        logger.debug(self.lst_bits_ref)
        logger.debug(self.lst_bits_nb)

    def _send(self):
        self._generate_signal(self.lst_bits_nb)    

    def send(self, message, *args, **kwargs):
        self._feed(message)
        self._send()

    def _get_list_of_nb_of_same_bit(self, s_bin):
        bit_prev = TRUE
        lst_bits_nb = []
        count = 0
        for i, bit in enumerate(s_bin):
            if bit == bit_prev:
                count += 1
            else:
                lst_bits_nb.append(count)
                count = 1
            bit_prev = bit
        lst_bits_nb.append(1)        
        return lst_bits_nb

    def _bit_generator(self, lst):
        for i, val in enumerate(lst):
            yield i, (i + 1) % 2, val

    def _generate_signal(self, lst_bits_nb, *args, **kwargs):
        for i, bit, nb_bits in self._bit_generator(lst_bits_nb):
            #print("%04d %d %03d" % (i, bit, nb_bits))
            if str(bit) == FALSE:
                #self.off(nb_bits, *args, **kwargs)
                self._off_callback(lst_bits_nb, nb_bits) #, *args, **kwargs)
            elif str(bit) == TRUE:
                #self.on(nb_bits, *args, **kwargs)
                self._on_callback(lst_bits_nb, nb_bits) #, *args, **kwargs)

    def set_callback_on(self, callback, *args, **kwargs):
        def callback_wrapper(*args, **kwargs):
            return callback(*args, **kwargs)
        self._on_callback = callback_wrapper

    def set_callback_off(self, callback, *args, **kwargs):
        def callback_wrapper(*args, **kwargs):
            return callback(*args, **kwargs)
        self._off_callback = callback_wrapper

"""
def on(self, nb, *args, **kwargs):
    for i in range(nb):
        sys.stdout.write(TRUE)

def off(self, nb, *args, **kwargs):
    for i in range(nb):
        sys.stdout.write(FALSE)

"""

"""
"""

def on(lst_bits_nb, nb):
    #print("on")
    #print("lst_bits_nb=%s" % lst_bits_nb)
    for k in range(nb):
        sys.stdout.write(TRUE)
    #print("")

def off(lst_bits_nb, nb):
    for k in range(nb):
        sys.stdout.write(FALSE)

def main(message="MORSE CODE"):
    logging.basicConfig(level=logging.DEBUG)

    import argparse

    parser = argparse.ArgumentParser(description='Send morse code')
    parser.add_argument('--msg', help='Message', default='MORSE CODE')
    args = parser.parse_args()
    message = args.msg


    morse_gen = MorseGenerator()
    morse_gen.set_callback_on(on, 'x', 'y', 'z')
    morse_gen.set_callback_off(off)

    logger.debug(message)
    logger.debug(mtalk.encode(message))
    morse_gen.send(message)
    
    print("")

if __name__ == '__main__':
    main()