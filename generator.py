#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sched, time
import datetime

import morse_talk as mtalk
from morse_talk.utils import wpm_to_duration, WORD
from abc import ABCMeta, abstractmethod

TRUE = 1
FALSE = 0


def _get_list_of_nb_of_same_bit(s_bin, on_value, off_value):
    """
    Calculate number of consecutive elements with same bit value

    >>> lst_bin = [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1]
    >>> _get_list_of_nb_of_same_bit(lst_bin, 1, 0)
    [1, 1, 1, 1, 1, 3, 3, 1, 3, 1, 3, 3, 1, 1, 1, 1, 1]
    """
    bit_prev = on_value
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


def _generate_events(lst_nb, element_duration, offset=1, on_value=TRUE, off_value=FALSE):
    """
    Generate events
    """
    total_elements = 0
    for i, nb in enumerate(lst_nb + [on_value]):
        bit = (i + offset) % 2
        yield bit, nb * element_duration, total_elements * element_duration
        total_elements += nb


def _get_element_duration(element_duration, wpm):
    """
    Returns element duration when element_duration and/or code speed is given

    >>> _get_element_duration(0.2, None)
    0.2

    >>> _get_element_duration(None, 15)
    0.08

    >>> _get_element_duration(None, None)
    1
    """
    if element_duration is None and wpm is None:
        return 1
    elif element_duration is not None and wpm is None:
        return element_duration
    elif element_duration is None and wpm is not None:
        return wpm_to_duration(wpm, output='float', word=WORD) / 1000.0
    else:
        raise NotImplementedError("Can't set both element_duration and wpm")


class MorseCodeGenerator(object):
    def __init__(self):
        self._on_callback = None
        self._on_callback_args = []
        self._on_callback_kwargs = {}

        self._off_callback = None
        self._off_callback_args = []
        self._off_callback_kwargs = {}

        self._on_value = TRUE
        self._off_value = FALSE

        self._s = None #  scheduler
    
    def _init_scheduler(self, s, lst_bin, element_duration):
        """
        Initialize scheduler
        """
        lst_nb = _get_list_of_nb_of_same_bit(lst_bin, self._on_value, self._off_value)
        priority = 1
        for bit, duration, total_delay in _generate_events(lst_nb, element_duration):
            if bit == self._off_value:
                if self._off_callback is not None:
                    s.enter(total_delay, priority, self._off_callback, [duration])
            elif bit == self._on_value:
                if self._on_callback is not None:
                    s.enter(total_delay, priority, self._on_callback, [duration])
            else:
                raise NotImplementedError("'%s' is not a bit" % bit)
            #priority += 1

    def _schedule(self, message, element_duration):
        """
        Schedule on / off events according message
        """
        lst_bin = mtalk.encoding._encode_binary(message)
        self._s = sched.scheduler(time.time, time.sleep)
        self._init_scheduler(self._s, lst_bin, element_duration=element_duration)

    def _send(self):
        self._s.run()

    def send(self, message, element_duration=None):
        self._schedule(message, element_duration)
        self._send()

    def _wrap_callback(self, callback, args, kwargs):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        def callback_wrapper(duration):
            return callback(duration, *args, **kwargs)
        return callback_wrapper
        
    def set_callback_on(self, callback, args=None, kwargs=None):
        self._on_callback = self._wrap_callback(callback, args, kwargs)

    def set_callback_off(self, callback, args=None, kwargs=None):
        self._off_callback = self._wrap_callback(callback, args, kwargs)


class SampleGeneratorApp(object):
    """
    An abstract class for morse generator application
    """
    
    __metaclass__ = ABCMeta

    def __init__(self, message, element_duration):
        self.message = message

        self._generator = MorseCodeGenerator()
        
        self.element_duration = element_duration
        
        #self._generator.set_callback_on(on, [self.t0])
        #self._generator.set_callback_off(off, [self.t0])

    @abstractmethod
    def on_ON(self, duration):
        pass

    @abstractmethod
    def on_OFF(self, duration):
        pass

    def run(self):
        self.t0 = datetime.datetime.utcnow()
        self._generator.set_callback_on(self.on_ON, [self.t0])
        self._generator.set_callback_off(self.on_OFF, [self.t0])
        self._generator.send(self.message, element_duration=self.element_duration)


class PrintableSampleGeneratorApp(SampleGeneratorApp):
    """
    A class to print 1 or 0 on console 
    according a text message encoded to morse code
    """
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
    """
    A class to send a sound at a given frequency 
    according a text message encoded to morse code
    """
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
    """
    A class to switch ON or OFF a led
    according a text message encoded to morse code
    
    A computer with GPIO is required 
    (or a computer connected to a board with GPIO such as Arduino boards)

    Pingo is also required 
        http://www.pingo.io/
        https://github.com/pingo-io/pingo-py
    """
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
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()
