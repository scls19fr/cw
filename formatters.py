#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some formatters for
 - Text
 - Morse code
 - Binary morse code

Copyright (C) 2015 by
Sébastien Celles <s.celles@gmail.com>
All rights reserved.
"""

# import abc # Abstract base class

class Formatter(object):
    """
    A base class for Formatter
    """
    def __init__(self, *args, **kwargs):
        pass

    def format(self, message):
        raise NotImplementedError

class TEXT_SEP(object):
    CHAR = ''
    WORD = ' '

class TextFormatter(Formatter):
    """
    A text formatter

    >>> formatter = TextFormatter()
    >>> msg = 'HELLO WORLD'
    >>> msg = list(map(list, msg.split(' ')))
    >>> msg
    [['H', 'E', 'L', 'L', 'O'], ['W', 'O', 'R', 'L', 'D']]
    >>> formatter.format(msg)
    'HELLO WORLD'
    """

    def __init__(self, *args, **kwargs):
        super(TextFormatter, self).__init__(*args, **kwargs)

    def format(self, msg):
        return self._format_sentence(map(self._format_word, msg))

    def _format_word(self, word):
        """
        >>> formatter = TextFormatter()
        >>> formatter._format_word(['H', 'E', 'L', 'L', 'O'])
        'HELLO'
        """
        return TEXT_SEP.CHAR.join(word)

    def _format_sentence(self, sentence):
        """
        >>> formatter = TextFormatter()
        >>> formatter._format_sentence(['HELLO', 'WORLD'])
        'HELLO WORLD'
        """
        return TEXT_SEP.WORD.join(sentence)

class MorseCodeFormatter(Formatter):
    """
    A Morse code formatter

    >>> formatter = MorseCodeFormatter()
    >>> import morse_talk as mtalk
    >>> code = mtalk.encode("MORSE CODE")
    >>> code
    ''
    >>> formatter.format(code)
    ''
    """

class BinaryMorseCodeFormatter(Formatter):
    """
    A binary Morse code formatter
    """


def main():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()