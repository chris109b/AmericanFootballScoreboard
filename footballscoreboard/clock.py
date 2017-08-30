#!/usr/bin/env python3

# Python standard library imports
from enum import Enum
import json
# Imports from external modules

# Internal modules import


class ClockEventListener:

    def on_clock_update(self, clock):
        raise NotImplementedError

    def on_time_update(self, minutes, seconds):
        raise NotImplementedError


class Clock:

    class ClockMode(Enum):
        INCREMENTING = "Incrementing"
        DECREMENTING = "Decrementing"

    def __init__(self):
        self._mode = self.ClockMode.DECREMENTING
        self._is_ticking = False
        self._minutes = 12
        self._seconds = 0
        self._event_listeners = []

    def set_mode(self, mode):
        self._mode = mode

    def get_mode(self):
        return self._mode

    def set_seconds(self, seconds):
        self._seconds = seconds

    def get_seconds(self):
        return self._seconds

    def set_minutes(self, minutes):
        self._minutes = minutes

    def get_minutes(self):
        return self._minutes

    def submit(self):
        for listener in self._event_listeners:
            listener.on_clock_update(self)

    def get_json_string(self):
        json_data = {'mode': self._mode.value,
                     'is_ticking': self._is_ticking,
                     'minutes': self._minutes,
                     'seconds': self._seconds}
        return json.dumps(json_data)

    def start(self):
        pass

    def stop(self):
        pass

    def is_ticking(self):
        return self._is_ticking

    # MARK: Event listeners

    def add_listener(self, listener):
        self._event_listeners.append(listener)

    def remove_listener(self, listener):
        self._event_listeners.remove(listener)
