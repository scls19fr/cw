#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some Morse code functions

Copyright (C) 2015 by
Sébastien Celles <s.celles@gmail.com>
All rights reserved.

"""

WORD = 'PARIS'  # Reference word for code speed
# http://www.kent-engineers.com/codespeed.htm

import morse_talk as mtalk

def _encode_morse(message):
    """
    >>> message = "SOS"
    >>> _encode_morse(message)
    ['...', '---', '...']
    """
    return [mtalk.encoding.morsetab.get(c.upper(), '?') for c in message]

def _encode_binary(message, on=1, off=0):
    """
    >>> message = "SOS"
    >>> _encode_binary(message)
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1]

    >>> _encode_binary(message, on='1', off='0')
    ['1', '0', '1', '0', '1', '0', '0', '0', '1', '1', '1', '0', '1', '1', '1', '0', '1', '1', '1', '0', '0', '0', '1', '0', '1', '0', '1']
    """
    l = _encode_morse(message)
    s = ' '.join(l)
    l = list(s)
    bin_conv = { '.': [on], '-': [on]*3, ' ': [off]}
    l = map(lambda symb: [off] + bin_conv[symb], l)
    lst = [item for sublist in l for item in sublist] # flatten list
    return lst[1:]

def _repeat_word(word, N):
    """
    >>> word = "PARIS"
    >>> _repeat_word(word, 5)
    'PARIS PARIS PARIS PARIS PARIS'
    """
    message = (" " + word) * N
    message = message[1:]
    return message

def mlength(message, N=1, word_spaced=True):
    """
    Returns Morse length

    >>> message = "PARIS"
    >>> mlength(message)
    50
    >>> mlength(message, 5)
    250
    """
    message = _repeat_word(message, N)
    if word_spaced:
        message = message + " E"
    lst_bin = _encode_binary(message)
    N = len(lst_bin)
    if word_spaced:
        N -= 1
    return N

def wpm_to_ms(wpm, word=WORD, use_decimal=True):
    """
    Convert from WPM (word per minutes) to 
    element duration (in ms)

    >>> wpm_to_ms(5)
    Decimal('240')

    >>> wpm_to_ms(5, use_decimal=False)
    240.0
    """
    N = mlength(_repeat_word(word, wpm))
    if use_decimal:
        import decimal
        ms = 60 * 1000 / decimal.Decimal(N)
    else: # use float
        ms = 60 * 1000 / float(N)
    return ms

def main():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()