#!/usr/bin/env python3


class PluginRegistry:

    HELP_SEPARATOR = "\n--------------------------------------------------------------------------------\n"

    __plugins = {}

    @classmethod
    def register_plugin(cls, plugin_name, plugin_class):
        PluginRegistry.__plugins[plugin_name] = plugin_class

    @classmethod
    def load_plugin(cls, plugin_name, args):
        plugin = PluginRegistry.__plugins[plugin_name](args)
        return plugin

    @classmethod
    def __underline(cls, string):
        line = ""
        for i in range(0, len(string)):
            line += "-"
        return line

    @classmethod
    def print_help(cls):
        for plugin_name in PluginRegistry.__plugins:
            headline = "Plugin: %s" % plugin_name
            print("\n" + headline + "\n" + PluginRegistry.__underline(headline) + "\n")
            print(PluginRegistry.__plugins[plugin_name].get_help())
        print("")


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

    def start(self, scoreboard):
        pass

    def update(self, scoreboard):
        pass

    def stop(self, scoreboard):
        pass

    def register(self):
        pass

    @classmethod
    def get_help(cls):
        return "There is no users manual implemented for this plugin."
