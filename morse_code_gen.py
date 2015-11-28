#!/usr/bin/env python

import morse_talk as mtalk
import sys

FALSE = '0'
TRUE = '1'

class MorseGenerator(object):
    def __init__(self):
        pass

    def on(self, nb, *args, **kwargs):
        for i in range(nb):
            sys.stdout.write(TRUE)

    def off(self, nb, *args, **kwargs):
        for i in range(nb):
            sys.stdout.write(FALSE)

    def _feed(self, message):
        self.bin = mtalk.encode(message, encoding_type='binary')
        self.lst_bits_nb = self._get_list_of_nb_of_same_bit(self.bin)
        self.lst_bits_ref = [bit for _, bit, _ in self._bit_generator(self.lst_bits_nb)]

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
                self.off(nb_bits, *args, **kwargs)
            elif str(bit) == TRUE:
                self.on(nb_bits, *args, **kwargs)

class LightingMorseGenerator(MorseGenerator):
    def __init__(self, *args, **kwargs):
        super(LightingMorseGenerator, self).__init__(*args, **kwargs)
        self.board = ...

    def on(self, nb, *args, **kwargs):
        pass

    def off(self, nb, *args, **kwargs):
        pass

    def close(self):
        self.board = ...

def main(message="MORSE CODE"):
    print(message)
    morse_gen = MorseGenerator()
    print(mtalk.encode(message))
    morse_gen._feed(message)
    print(morse_gen.bin)
    print(morse_gen.lst_bits_ref)
    print(morse_gen.lst_bits_nb)
    morse_gen._send()
    print("")

if __name__ == '__main__':
    main()