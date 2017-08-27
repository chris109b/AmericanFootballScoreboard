#!/usr/bin/env python3

# Python standard library imports

# Imports from external modules
import tornado.websocket
# Internal modules import
from .scoreboard import ScoreboardEventListener


class WebSocketHandler(tornado.websocket.WebSocketHandler, ScoreboardEventListener):

    def initialize(self, webserver):
        self.__webserver = webserver

    def on_scoreboard_update(self, scoreboard):
        data = scoreboard.get_json_string()
        self.write_message(data)

    def on_clock_update(self, entries, update_count, json_string):
        self.write_message(json_string)

    def open(self):
        scoreboard = self.__webserver.get_scoreboard()
        scoreboard.add_listener(self)

    def on_message(self, message):
        self.write_message(u"Your message was: " + message)

    def on_close(self):
        scoreboard = self.__webserver.get_scoreboard()
        scoreboard.remove_listener(self)
