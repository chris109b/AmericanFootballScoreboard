#!/usr/bin/env python3

# Python standard library imports
import time
# Imports from external modules
from tornado.ioloop import PeriodicCallback
# Internal modules import
from .clock import Clock


class MasterClock(Clock):

    def __init__(self):
        super(MasterClock, self).__init__()
        self._start_timestamp = None
        self._last_update_timestamp = None
        self._periodic_callback = PeriodicCallback(self.tick, 200)

    def tick(self):
        timestamp = int(time.time())
        if timestamp != self._last_update_timestamp:
            time_delta = timestamp - self._last_update_timestamp
            if self._mode == self.ClockMode.INCREMENTING:
                if self._seconds < (60 - time_delta):
                    self._seconds += time_delta
                else:
                    self._minutes += 1
                    self._seconds = (time_delta - 1)
            elif self._mode == self.ClockMode.DECREMENTING:
                if (self._seconds - time_delta) > 0:
                    self._seconds -= time_delta
                else:
                    if self._minutes > 0:
                        self._minutes -= 1
                        self._seconds = (60 - time_delta)
                    else:
                        self.stop()
            else:
                self.stop()
            self._last_update_timestamp = timestamp
            # Inform listeners
            for listener in self._event_listeners:
                listener.on_time_update(self._minutes, self._seconds)

    def start(self):
        timestamp = int(time.time())
        self._last_update_timestamp = timestamp
        self._is_ticking = True
        self._periodic_callback.start()
        self.submit()

    def stop(self):
        self._is_ticking = False
        self._periodic_callback.stop()
        self.submit()
