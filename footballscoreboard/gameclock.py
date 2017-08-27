#!/usr/bin/env python3

# Python standard library imports
import weakref
from enum import Enum
import time
import json
# Imports from external modules
from tornado.ioloop import PeriodicCallback
# Internal modules import


class GameClockEventListener:

    def on_clock_update(self, clock):
        raise NotImplementedError

    def on_time_update(self, minutes, seconds):
        raise NotImplementedError


class GameClockDelegate:

    def update_clock(self, minutes, seconds):
        raise NotImplementedError


class GameClock:

    class ClockMode(Enum):
        INCREMENTING = "Incrementing"
        DECREMENTING = "Decrementing"

    def __init__(self, delegate):
        self.__mode = self.ClockMode.DECREMENTING
        self.__is_ticking = False
        self.__minutes = 0
        self.__seconds = 0
        self.__delegate_ref = weakref.ref(delegate)
        self.__start_timestamp = None
        self.__last_update_timestamp = None
        self.__periodic_callback = PeriodicCallback(self.tick, 200)
        self._event_listeners = []

    def set_mode(self, mode):
        self.__mode = mode

    def get_mode(self):
        return self.__mode

    def set_seconds(self, seconds):
        self.__seconds = seconds

    def get_seconds(self):
        return self.__seconds

    def set_minutes(self, minutes):
        self.__minutes = minutes

    def get_minutes(self):
        return self.__minutes

    def submit(self):
        for listener in self._event_listeners:
            listener.on_clock_update(self)

    def tick(self):
        timestamp = int(time.time())
        if timestamp != self.__last_update_timestamp:
            time_delta = timestamp - self.__last_update_timestamp
            if self.__mode == self.ClockMode.INCREMENTING:
                if self.__seconds < (60 - time_delta):
                    self.__seconds += time_delta
                else:
                    self.__minutes += 1
                    self.__seconds = (time_delta - 1)
            elif self.__mode == self.ClockMode.DECREMENTING:
                if (self.__seconds - time_delta) > 0:
                    self.__seconds -= time_delta
                else:
                    if self.__minutes > 0:
                        self.__minutes -= 1
                        self.__seconds = (60 - time_delta)
                    else:
                        self.stop()
            else:
                self.stop()
            self.__last_update_timestamp = timestamp
            # Inform listeners
            for listener in self._event_listeners:
                listener.on_time_update(self.__minutes, self.__seconds)
            # Inform delegate
            self.__delegate_ref().update_clock(self.__minutes, self.__seconds)

    def get_json_string(self):
        json_data = {'mode': self.__mode.value,
                     'is_ticking': self.__is_ticking,
                     'minutes': self.__minutes,
                     'seconds': self.__seconds}
        return json.dumps(json_data)

    def start(self):
        timestamp = int(time.time())
        self.__start_timestamp = timestamp
        self.__last_update_timestamp = timestamp
        self.__is_ticking = True
        self.__periodic_callback.start()
        self.submit()

    def stop(self):
        self.__is_ticking = False
        self.__periodic_callback.stop()
        self.submit()

    def is_ticking(self):
        return self.__is_ticking

    # MARK: Event listeners

    def add_listener(self, listener):
        self._event_listeners.append(listener)

    def remove_listener(self, listener):
        self._event_listeners.remove(listener)
