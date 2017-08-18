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

    def start(self, scoreboard):
        print("Test Plugin started")
        pass

    @classmethod
    def print_entries(cls, entry_list):
        for entry in entry_list:
            print("{0} = {1}".format(entry.key, (entry.value.value if isinstance(entry.value, Enum) else entry.value)))


    def update(self, scoreboard):
        print("================================================================================")
        print("All entries:")
        self.print_entries(scoreboard.get_all_entries())
        print("--------------------------------------------------------------------------------")
        print("Changed entries:")
        self.print_entries(scoreboard.get_changed_entries())

    def stop(self, scoreboard):
        print("Test Plugin stopped")
        pass

    @classmethod
    def print_manual(cls):
        print("Test Plugin Manual")
        pass

    @classmethod
    def register(cls):
        PluginRegistry.register_plugin(TestPlugin.__name__, TestPlugin)

# Register plugin
TestPlugin.register()
