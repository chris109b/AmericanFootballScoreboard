#!/usr/bin/env python3

# Internal modules import
from .webserver import Webserver
from .scoreboard import Scoreboard
from .plugin import PluginRegistry
from plugins import *


class App:

    def __init__(self):
        self.__scoreboard = Scoreboard()
        self.__webserver = Webserver(self.__scoreboard, None)

    def load_plugins(self, args):
        for argument in args:
            self._load_plugin(argument)

    def _load_plugin(self, argument):
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
            self.__scoreboard.add_plugin(plugin)

    def run(self):
        self.__scoreboard.start()
        self.__webserver.start()

    def exit(self):
        self.__scoreboard.stop()
        self.__webserver.stop()
