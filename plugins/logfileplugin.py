#!/usr/bin/env python3

# Python standard library imports
import os
import time
from enum import Enum
# Internal modules import
from footballscoreboard.plugin import Plugin
from footballscoreboard.app import PluginRegistry


class LogFilePlugin(Plugin):

    NAME = "Log File Plugin"

    def __init__(self, args):
        super().__init__()
        self._target_file_path = None
        # Parameter: Target File
        if len(args) == 1:
            self._target_file_path = args[0]
            self._target_file_path = os.path.abspath(self._target_file_path)
        else:
            message = "Missing parameter LOG_FILE_PATH"
            self.raise_parameter_error(LogFilePlugin.NAME, message)

    def start(self, scoreboard):
        with open(self._target_file_path, 'a') as fp:
            line = time.strftime("%Y-%m-%d %H:%M:%S > ") + "American Football Scoreboard " + self.NAME + " started"
            fp.write("========== " + line + " ==========\n")

    def update(self, scoreboard):
        with open(self._target_file_path, 'a') as fp:
            all_entries = scoreboard.get_all_entries()
            line = time.strftime("%Y-%m-%d %H:%M:%S > ")
            for entry in all_entries:
                value = (entry.value.value if isinstance(entry.value, Enum) else entry.value)
                line += str(entry.key) + "=" + str(value) + ";"
            fp.write(line + "\n")

    def stop(self, scoreboard):
        pass

    @classmethod
    def print_manual(cls):
        print("Log File Plugin Manual")
        pass

    @classmethod
    def register(cls):
        PluginRegistry.register_plugin(LogFilePlugin.__name__, LogFilePlugin)

# Register plugin
LogFilePlugin.register()
