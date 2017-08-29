#!/usr/bin/env python3

# Python standard library imports

# Imports from external modules

# Internal modules import


class PluginRegistry:

    HELP_SEPARATOR = "\n--------------------------------------------------------------------------------\n"

    __plugins = {}

    @classmethod
    def register_plugin(cls, plugin_name, plugin_class):
        PluginRegistry.__plugins[plugin_name] = plugin_class

    @classmethod
    def load_plugin(cls, plugin_name, args):
        try:
            plugin = PluginRegistry.__plugins[plugin_name](args)
        except KeyError:
            print("There is no plugin named \"%s\"." % plugin_name)
            return None
        else:
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
