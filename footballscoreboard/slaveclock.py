#!/usr/bin/env python3

# Python standard library imports

# Imports from external modules

# Internal modules import
from .clock import Clock


class SlaveClock(Clock):

    def __init__(self):
        super(SlaveClock, self).__init__()

