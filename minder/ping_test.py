#!/usr/bin/python3
# -*- coding: utf-8 -*-
from .base_test import BaseTest

class PingTest(BaseTest):
    """
The "ping test" is actually embedded into the base test so that the base_test.py
represents the entire code of a working example. Hence no extra code is required here!
N.B. The ping test does not figure in the performance tests (see ethernet_test.py for
the real thing).
    """
    pass