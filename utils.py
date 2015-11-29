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

def wpm_to_duration(wpm, output='timedelta', word=WORD):
    """
    Convert from WPM (word per minutes) to 
    element duration

    Parameters
    ----------
    wpm : int or float - word per minute
    output : String - type of output
        'timedelta'
        'float'
        'decimal'
    word : String - reference word (PARIS by default)

    Returns
    -------
    duration : timedelta or float or decimal.Decimal - duration of an element

    >>> wpm_to_duration(5, output='decimal')
    Decimal('240')

    >>> wpm_to_duration(5, output='float')
    240.0

    >>> wpm_to_duration(5, output='timedelta')
    datetime.timedelta(0, 0, 240000)

    >>> wpm_to_duration(13, output='decimal')
    Decimal('92.30769230769230769230769231')

    >>> wpm_to_duration(5.01, output='timedelta')
    datetime.timedelta(0, 0, 239521)
    """
    N = mlength(word) * wpm
    output = output.lower()
    allowed_output = ['decimal', 'float', 'timedelta']
    if output == 'decimal':
        import decimal
        duration = 60 * 1000 / decimal.Decimal(N)
    elif output == 'float':
        duration = 60 * 1000 / float(N)
    elif output == 'timedelta':
        import datetime
        duration = datetime.timedelta(seconds=(60 / float(N)))
    else:
        raise NotImplementedError("output must be in %s" % allowed_output)
    return duration

def main():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()