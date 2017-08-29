#!/usr/bin/env python3

# Python standard library imports

# Imports from external modules

# Internal modules import
from .scoreboard import ScoreboardEventListener
from .clock import ClockEventListener
from .pluingregistry import PluginRegistry
from plugins import *


class PluginManager(ScoreboardEventListener, ClockEventListener):

    def __init__(self, scoreboard, clock):
        scoreboard.add_listener(self)
        clock.add_listener(self)
        self.__scoreboard = scoreboard
        self.__clock = clock
        self.__plugins = []

    # MARK: Live cycle

    def start(self):
        for plugin in self.__plugins:
            plugin.start(self.__scoreboard, self.__clock)
        self.__scoreboard.add_listener(self)
        self.__clock.add_listener(self)

    def stop(self):
        for plugin in self.__plugins:
            plugin.start(self.__scoreboard, self.__clock)
        self.__scoreboard.remove_listener(self)
        self.__clock.remove_listener(self)

    # MARK: ScoreboardEventListener

    def on_scoreboard_update(self, scoreboard):
        for plugin in self.__plugins:
            plugin.update(self.__scoreboard, self.__clock)

    # MARK: ClockEventListener

    def on_clock_update(self, clock):
        for plugin in self.__plugins:
            plugin.update(self.__scoreboard, self.__clock)

    def on_time_update(self, minutes, seconds):
        for plugin in self.__plugins:
            plugin.time_update(minutes, seconds)

    # MARK: Plugin management

    def load_plugins(self, args):
        for argument in args:
            self._load_one_plugin(argument)

    def _load_one_plugin(self, argument):
        try:
            plugin_name, plugin_args_string = argument.split(":")
        except ValueError:
            plugin_name = argument
            plugin_args_string = None
        if plugin_name is not None:
            plugin_args_list = None
            if plugin_args_string is not None:
                try:
                    plugin_args_list = plugin_args_string.split(";")
                except ValueError:
                    plugin_args_list = [plugin_args_string]
            plugin = PluginRegistry.load_plugin(plugin_name, plugin_args_list)
            if plugin is not None and not plugin.is_disabled():
                self.__plugins.append(plugin)
