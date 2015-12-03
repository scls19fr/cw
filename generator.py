#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sched, time
import datetime

import morse_talk as mtalk
from morse_talk.utils import wpm_to_duration, WORD

TRUE = 1
FALSE = 0

def on(t0):
    """
    Default on function
    
    Parameters
    ----------
    t0 : datetime of first element

    """
    t = datetime.datetime.utcnow()
    td = t - t0
    state = TRUE
    print("%s %s" % (td, state))

def off(t0):
    """
    Default off function
    
    Parameters
    ----------
    t0 : datetime of first element

    """
    t = datetime.datetime.utcnow()
    td = t - t0
    state = FALSE
    print("%s %s" % (td, state))

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
    
def _init_scheduler(s, lst_bin, element_duration, 
        on_func, off_func, on_value, off_value, 
        func_args, func_kwargs):
    """
    Initialize scheduler
    """
    lst_nb = _get_list_of_nb_of_same_bit(lst_bin, on_value, off_value)
    priority = 1
    for bit, duration, total_delay in _generate_events(lst_nb, element_duration):
        if bit == off_value:
            s.enter(total_delay, priority, off_func, func_args, func_kwargs)
        elif bit == on_value:
            s.enter(total_delay, priority, on_func, func_args, func_kwargs)
        else:
            raise NotImplementedError("'%s' is not a bit" % bit)
        #priority += 1

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

def schedule(message, element_duration=None, wpm=None, 
        on_func=on, off_func=off, on_value=TRUE, off_value=FALSE,
        func_args=None, func_kwargs=None):
    """
    Schedule on / off events according message
    """
    if func_args is None:
        func_args = []
    if func_kwargs is None:
        func_kwargs = {}
    element_duration = _get_element_duration(element_duration, wpm)
    lst_bin = mtalk.encoding._encode_binary(message)
    s = sched.scheduler(time.time, time.sleep)
    _init_scheduler(s, lst_bin, element_duration=element_duration, 
        on_func=on_func, off_func=off_func, 
        on_value=on_value, off_value=off_value,
        func_args=func_args, func_kwargs=func_kwargs)
    return s

def main():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()
