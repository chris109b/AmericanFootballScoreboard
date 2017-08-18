#!/usr/bin/env python3


class PluginRegistry:

    plugins = {}

    @classmethod
    def register_plugin(cls, plugin_name, plugin_class):
        PluginRegistry.plugins[plugin_name] = plugin_class

    @classmethod
    def load_plugin(cls, plugin_name, args):
        plugin = PluginRegistry.plugins[plugin_name](args)
        return plugin


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


