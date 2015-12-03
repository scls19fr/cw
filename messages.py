#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some Python classes to manage (parse and format)
 - Text message
 - Morse code message
 - Binary morse code message

A message is composed of:
 - sentences (which are composed of)
   - words (which are composed of)
     - characters (which are composed of)
       - elements (which are composed of) - Morse code - elements are DIT . or DAH -
         - bits - Binary morse code - bits are 1 or 0

Copyright (C) 2015 by
Sébastien Celles <s.celles@gmail.com>
All rights reserved.
"""

import abc # Abstract base class

class Message(object):
    __metaclass__ = abc.ABCMeta

    """
    An abstract class for Message
    """
    def __init__(self, sep=None, *args, **kwargs):
        pass

    @abc.abstractmethod
    def format(self, lst_message):
        """Returns formatted message"""
        pass

    @abc.abstractmethod
    def parse(self, message):
        """Returns parsed message"""
        pass

    def _split(self, s, separator):
        """Splits string s using 'separator'
        if separator is an empty string
        a list of characters is returned

        >>> message = Message()
        >>> message._split("abcd" , '')
        ['a', 'b', 'c', 'd']

        >>> message._split("a b c d" , ' ')
        ['a', 'b', 'c', 'd']
        """
        if separator != '':
            return s.split(separator)
        else:
            return list(s)

class SEP(object):
    pass

class TEXT_SEP(SEP):
    char = ''
    word = ' '

class MORSE_SEP(SEP):
    elt = ''
    char = ' '
    word = ' '

class BIN_MORSE_SEP(SEP):
    bit = ''
    elt = ''
    char = ''
    word = ''

class SEP_NB(object):
    pass

class TEXT_SEP_NB(SEP_NB):
    char = 1
    word = 1

class MORSE_SEP_NB(SEP_NB):
    elt = 1
    char = 1
    word = 1

class BIN_MORSE_SEP_NB(SEP_NB):
    bit = 1
    elt = 1
    char = 1
    word = 1

class _Entity(object):
    def __init__(self, sep, sep_nb, *args, **kwargs):
        self.sep = sep # character to separate each char of a word
        self.sep_nb = sep_nb # nb of such character

    def parse(self, entity):
        return self._split(entity, self.sep)

    def format(self, entity):
        return self.sep.join(entity)

    def _split(self, s, separator):
        """Splits string s using 'separator'
        if separator is an empty string
        a list of characters is returned

        >>> message = Message()
        >>> message._split("abcd" , '')
        ['a', 'b', 'c', 'd']

        >>> message._split("a b c d" , ' ')
        ['a', 'b', 'c', 'd']
        """
        if separator != '':
            return s.split(separator)
        else:
            return list(s)

class _TextWord(_Entity):
    """
    A text word entity class
    a word is composed of characters
    separate by a `sep_nb` of `sep`

    >>> entity = _TextWord()

    >>> msg = 'HELLO'
    >>> entity.parse(msg)
    ['H', 'E', 'L', 'L', 'O']

    >>> entity.format(['H', 'E', 'L', 'L', 'O'])
    'HELLO'

    """
    def __init__(self, *args, **kwargs):
        super(_TextWord, self).__init__(sep='', sep_nb=1, *args, **kwargs)

class _TextSentence(_Entity):
    """

    >>> entity = _TextSentence()
    >>> entity.format(['HELLO', 'WORLD'])
    'HELLO WORLD'

    >>> entity = _TextSentence()
    >>> entity.parse('HELLO WORLD')
    ['HELLO', 'WORLD']
    """
    def __init__(self, *args, **kwargs):
        super(_TextSentence, self).__init__(sep=' ', sep_nb=1, *args, **kwargs)


"""
ToFix
=====

TextMessage should now use _TextWord and _TextSentence classes
TextMessage should inherit from _Entity



"""

class TextMessage(Message):
    """
    A text message class

    >>> message = TextMessage()
    >>> text = 'HELLO WORLD'
    >>> lst_text = message.parse(text)
    >>> lst_text
    [['H', 'E', 'L', 'L', 'O'], ['W', 'O', 'R', 'L', 'D']]
    >>> message.format(lst_text)
    'HELLO WORLD'
    """

    def __init__(self, sep=None, *args, **kwargs):
        super(TextMessage, self).__init__(sep, *args, **kwargs)
        if sep is None:
            sep = TEXT_SEP
        self.sep = sep

    def format(self, lst_text):
        """Returns formatted text message
        """
        return self._format_sentence(map(self._format_word, lst_text))

    def _format_word(self, word):
        """
        >>> message = TextMessage()
        >>> message._format_word(['H', 'E', 'L', 'L', 'O'])
        'HELLO'
        """
        return self.sep.char.join(word)

    def _format_sentence(self, sentence):
        """
        >>> message = TextMessage()
        >>> message._format_sentence(['HELLO', 'WORLD'])
        'HELLO WORLD'
        """
        return self.sep.word.join(sentence)

    def parse(self, message):
        """Returns parsed text message
        """
        return list(map(self._parse_word, self._parse_sentence(message)))

    def _parse_word(self, word):
        """
        >>> message = TextMessage()
        >>> message._parse_word('HELLO')
        ['H', 'E', 'L', 'L', 'O']
        """
        return self._split(word, self.sep.char)

    def _parse_sentence(self, sentence):
        """
        >>> message = TextMessage()
        >>> message._parse_sentence('HELLO WORLD')
        ['HELLO', 'WORLD']
        """
        return sentence.split(self.sep.word)

class MorseCodeMessage(Message):
    """
    A Morse code message class

    >>> message = MorseCodeMessage()
    >>> import morse_talk as mtalk
    >>> text = "MORSE CODE"
    >>> code = mtalk.encode(text)
    >>> code
    '--   ---   .-.   ...   .       -.-.   ---   -..   .'
    >>> message.format(code)

    """

    def format(self, lst_message):
        return

    def _format_char(self, char):
        return

    def _format_word(self, word):
        return

    def _format_sentence(self, sentence):
        return

    def parse(self, message):
        return

    def _parse_char(self, char):
        return

    def _parse_word(self, word):
        return

    def _parse_sentence(self, sentence):
        return

class BinaryMorseCodeMessage(Message):
    """
    A binary Morse code message class

    >>> message = MorseCodeMessage()
    >>> import morse_talk as mtalk
    >>> text = "MORSE CODE"
    >>> bin_code = mtalk.encode(text, encoding_type='binary')
    >>> bin_code
    '11101110001110111011100010111010001010100010000000111010111010001110111011100011101010001'
    """

    def format(self, lst_message):
        return

    def _format_bit(self, bit):
        return

    def _format_element(self, element):
        return

    def _format_char(self, char):
        return

    def _format_word(self, word):
        return

    def _format_sentence(self, sentence):
        return

    def parse(self, message):
        return

    def _parse_bit(self, bit):
        return

    def _parse_element(self, element):
        return

    def _parse_char(self, char):
        return

    def _parse_word(self, word):
        return

    def _parse_sentence(self, sentence):
        return


def main():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()