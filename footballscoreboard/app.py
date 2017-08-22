#!/usr/bin/env python3

# Internal modules import
from .webserver import Webserver
from .slave import Slave
from .scoreboard import Scoreboard
from .plugin import PluginRegistry
from plugins import *


class App:

    def __init__(self):
        self.__scoreboard = Scoreboard()
        self.__webserver = None
        self.__web_client = None

    def initialize_master_mode(self):
        self.__webserver = Webserver(self.__scoreboard, None)

    def initialize_slave_mode(self):
        self.__web_client = Slave(self.__scoreboard)

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
        if self.__webserver is not None:
            self.__webserver.start()
        if self.__web_client is not None:
            self.__web_client.start()

    def exit(self):
        self.__scoreboard.stop()
        if self.__webserver is not None:
            self.__webserver.stop()
        if self.__web_client is not None:
            self.__web_client.stop()

    @classmethod
    def print_help(cls):
        print("This text does not help.")
