#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

def mlength(message, word_spaced=True):
    """
    Returns Morse length

    >>> message = "PARIS"
    >>> mlength(message)
    50
    """
    if word_spaced:
        message = message + " E"
    lst_bin = _encode_binary(message)
    N = len(lst_bin)
    if word_spaced:
        N -= 1
    return N

def main():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()