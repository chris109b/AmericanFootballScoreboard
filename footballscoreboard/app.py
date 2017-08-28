#!/usr/bin/env python3

# Python standard library imports
import sys
# Internal modules import
from .webserver import Webserver
from .slave import Slave
from .scoreboard import Scoreboard
from .plugin import PluginRegistry
from .core import Core
from .masterclock import MasterClock
from .slaveclock import SlaveClock
from plugins import *


class App:

    def __init__(self):
        self.__scoreboard = None
        self.__webserver = None
        self.__web_client = None

    def initialize_master_mode(self):
        self.__scoreboard = Scoreboard(MasterClock())
        self.__webserver = Webserver(self.__scoreboard, None)

    def initialize_slave_mode(self):
        self.__scoreboard = Scoreboard(SlaveClock())
        self.__web_client = Slave(self.__scoreboard)

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
            if plugin is not None:
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
        print("\n--------------------------------------------------------------------------------")
        print("\nAmerican Football Scoreboard"
              "\n============================"
              "\n"
              "\nUsage"
              "\n-----"
              "\n"
              "\n  " + sys.argv[0] + " <MODE> [PLUGIN PARAMETER]..."
              "\n"
              "\nModes"
              "\n-----"
              "\n"
              "\n  " + "{:<18}".format(", ".join(Core.PARAMETERS_MASTER_MODE)) + ""
              "Master mode is for standalone operation and to control\n"
              "                    an entire network."
              "\n"
              "\n  " + "{:<18}".format(", ".join(Core.PARAMETERS_SLAVE_MODE)) + ""
              "Slave mode doesn't provide an interface on it's own.\n"
              "                    Instead it connects to the first master it can find\n"
              "                    on the local network and replicates it's data in\n"
              "                    real time. Therefore you ca use output plugins on\n"
              "                    a different host and you can connect any device \n"
              "                    over network."
              "\n"
              "\nPlugin parameters"
              "\n-----------------"
              "\n"
              "\n  The pattern for activating plugins looks like this:"
              "\n  <PLUGIN_NAME>[:[PARAMETER1];[PARAMETER2];...[PARAMETERn]"
              "\n"
              "\n  Here are some examples:"
              "\n  TestPlugin"
              "\n  TestPlugin:Test1"
              "\n  TestPlugin:Test1;2;3;4")

        PluginRegistry.print_help()
