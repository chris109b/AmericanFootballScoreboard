#!/usr/bin/env python3

# Python standard library imports

# Imports from external modules

# Internal modules import


class Plugin:

    def __init__(self):
        self._disabled = False

    def raise_parameter_error(self, plugin_name, message):
        print("{0} Configuration Error:", plugin_name)
        print("    {0}", message)
        print("    This plugin remains disabled.")
        self._disabled = True

    def is_disabled(self):
        return self._disabled

    def start(self, scoreboard, clock):
        pass

    def time_update(self, minute, second):
        pass

    def update(self, scoreboard, clock):
        pass

    def stop(self, scoreboard, clock):
        pass

    def register(self):
        pass

    @classmethod
    def get_help(cls):
        return "There is no users manual implemented for this plugin."
