#!/usr/bin/env python3

# Python standard library imports
import sys
# Internal modules import
from .webserver import Webserver
from .slave import Slave
from .scoreboard import Scoreboard
from .pluingregistry import PluginRegistry
from .pluginmager import PluginManager
from .core import Core
from .masterclock import MasterClock
from .slaveclock import SlaveClock
from .displaylist import DisplayList

class App:

    def __init__(self):
        self.__plugin_manager = None
        self.__clock = None
        self.__scoreboard = None
        self.__webserver = None
        self.__web_client = None
        self.__display_list = None

    def initialize_master_mode(self):
        self.__clock = MasterClock()
        self.__scoreboard = Scoreboard(self.__clock)
        self.__display_list = DisplayList()
        self.__plugin_manager = PluginManager(self.__scoreboard, self.__clock)
        self.__webserver = Webserver(self.__scoreboard, self.__display_list, None)

    def initialize_slave_mode(self):
        self.__clock = SlaveClock()
        self.__scoreboard = Scoreboard(self.__clock)
        self.__web_client = Slave(self.__scoreboard)

    def load_plugins(self, args):
        if self.__plugin_manager is not None:
            self.__plugin_manager.load_plugins(args)

    def start(self):
        if self.__plugin_manager is not None:
            self.__plugin_manager.start()
        if self.__webserver is not None:
            self.__webserver.start()
        if self.__web_client is not None:
            self.__web_client.start()

    def stop(self):
        if self.__plugin_manager is not None:
            self.__plugin_manager.stop()
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
