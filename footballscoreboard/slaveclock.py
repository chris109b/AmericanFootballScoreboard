#!/usr/bin/env python3

# Python standard library imports

# Imports from external modules

# Internal modules import
from .clock import Clock


class SlaveClock(Clock):

    def __init__(self):
        super(SlaveClock, self).__init__()

    def update_clock_settings(self, mode, is_ticking, minutes, seconds):
        self._mode = mode
        self._is_ticking = is_ticking
        self._minutes = minutes
        self._seconds = seconds
        self.submit()

    def update_time(self, minutes, seconds):
        self._minutes = minutes
        self._seconds = seconds
        # Inform listeners
        for listener in self._event_listeners:
            listener.on_time_update(self._minutes, self._seconds)