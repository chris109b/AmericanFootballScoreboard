#!/usr/bin/env python3

# Python standard library imports
import os
from enum import Enum
# Internal modules import
from footballscoreboard.plugin import Plugin
from footballscoreboard.app import PluginRegistry


class OBSStudioPlugin(Plugin):

    NAME = "OBS Studio Plugin"

    def __init__(self, args):
        super().__init__()
        # Parameter: Target Directory
        self._target_directory = "./"
        if len(args) == 1:
            directory = args[0]
            if os.path.isdir(directory):
                self._target_directory = os.path.abspath(directory)
            else:
                message = "\"{0}\" is not a valid directory!".format(directory)
                self.raise_parameter_error(OBSStudioPlugin.NAME, message)

    def write_entries(self, entry_list):
        for entry in entry_list:
            value = (entry.value.value if isinstance(entry.value, Enum) else entry.value)
            file_name = str(entry.key) + ".txt"
            file_path = os.path.join(self._target_directory, file_name)
            with open(file_path, 'w') as fp:
                fp.write(str(value))

    def start(self, scoreboard):
        print("OBS Studio Plugin started")
        self.write_entries(scoreboard.get_all_entries())

    def update(self, scoreboard):
        self.write_entries(scoreboard.get_changed_entries())

    def stop(self, scoreboard):
        print("OBS Studio Plugin stopped")
        pass

    @classmethod
    def print_manual(cls):
        pass

    @classmethod
    def register(cls):
        PluginRegistry.register_plugin(OBSStudioPlugin.__name__, OBSStudioPlugin)

# Register plugin
OBSStudioPlugin.register()
