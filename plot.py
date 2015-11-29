#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A Morse Binary CLI plotter

Copyright (C) 2015 by
Sébastien Celles <s.celles@gmail.com>
All rights reserved.

Usage:
$ python plot.py --msg "MORSE CODE"
"""

import plotter
import argparse

import matplotlib.pyplot as plt
import morse_talk as mtalk

def main():
    parser = argparse.ArgumentParser(description='Send morse code')
    parser.add_argument('--msg', help='Message', default='MORSE CODE')
    args = parser.parse_args()
    message = args.msg

    print(message)
    print(mtalk.encode(message))
    print(mtalk.encode(message, encoding_type='binary'))

    ax = plotter.plot(message)
    plt.show()

if __name__ == '__main__':
    main()
