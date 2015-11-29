#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
PY2 = sys.version_info[0] == 2
PY3 = (sys.version_info[0] >= 3)

import itertools as IT

if PY2:
    it_count_next = IT.count().next
else:
    it_count_next = IT.count().__next__ 
