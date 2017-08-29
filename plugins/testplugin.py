#!/usr/bin/env python3

# Python standard library imports
from enum import Enum
# Internal modules import
from footballscoreboard.plugin import Plugin
from footballscoreboard.app import PluginRegistry


class TestPlugin(Plugin):

    NAME = "Test Plugin"

    def __init__(self, args):
        super().__init__()
        print("Initializing {0} with arguments:".format(TestPlugin.NAME))
        print(args)

    def start(self, scoreboard, clock):
        print("{0} started".format(TestPlugin.NAME))

    @classmethod
    def print_entries(cls, entry_list):
        for entry in entry_list:
            print("{0} = {1}".format(entry.key, (entry.value.value if isinstance(entry.value, Enum) else entry.value)))

    def update(self, scoreboard, clock):
        print("================================================================================")
        print("All entries:")
        self.print_entries(scoreboard.get_all_entries())
        print("--------------------------------------------------------------------------------")
        print("Changed entries:")
        self.print_entries(scoreboard.get_changed_entries())

    def time_update(self, minute, second):
        self.print("Time update: {0:02d}:{1:02d}".format(minute, second))

    def stop(self, scoreboard, clock):
        print("{0} stopped".format(TestPlugin.NAME))
        pass

    @classmethod
    def get_help(cls):
        return "  This is a test plugin. It doesn't need any parameters, but it takes any\n" \
               "  parameter you throw at it. I prints all parameters on initialisation.\n" \
               "\n" \
               "  Usage pattern:\n" \
               "  " + TestPlugin.__name__ + "[:[PARAMETER1];[PARAMETER2];...[PARAMETERn]\n" \
               "  Example usage:\n" \
               "  " + TestPlugin.__name__ + "\n" \
               "  " + TestPlugin.__name__ + ":Test1\n" \
               "  " + TestPlugin.__name__ + ":Test1;2;3;4"

    @classmethod
    def register(cls):
        PluginRegistry.register_plugin(TestPlugin.__name__, TestPlugin)

# Register plugin
TestPlugin.register()
