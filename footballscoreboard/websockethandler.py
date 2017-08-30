#!/usr/bin/env python3

# Python standard library imports
import json
from enum import Enum
# Imports from external modules
import tornado.websocket
# Internal modules import
from .scoreboard import Scoreboard
from .core import Core
from .masterclock import MasterClock
from .clock import ClockEventListener


class Event(Enum):

    CLOCK_UPDATE = "clock_update"
    TIME_UPDATE = "time_update"
    SCOREBOARD_UPDATE = "scoreboard_update"
    SHOW_IDENTIFICATION = "show_identification"
    CHANGE_APPEARANCE = "change_appearance"


class CommandLib:

    @classmethod
    def get_clock(cls, _, websocket_handler, webserver):
        clock = webserver.get_scoreboard().get_clock()
        websocket_handler.on_clock_update(clock)

    @classmethod
    def update_scoreboard(cls, parameters, _, webserver):
        keys_for_sting_values = [Scoreboard.KEY_HOME_TEAM,
                                 Scoreboard.KEY_GUEST_TEAM]
        # Apply changes to scoreboard
        scoreboard = webserver.get_scoreboard()
        try:
            for key, value in parameters.items():
                if key == Scoreboard.KEY_GAME_PHASE:
                    scoreboard.set(key, Scoreboard.GamePhase(value))
                elif key == Scoreboard.KEY_GAME_OFFENCIVE_TEAM:
                    scoreboard.set(key, Scoreboard.OffenciveTeam(value))
                elif key in keys_for_sting_values:
                    scoreboard.set(key, value)
                else:
                    scoreboard.set(key, int(value))
        except ValueError as e:
            print(e)
        except TypeError as e:
            print(e)
        finally:
            scoreboard.submit()

    @classmethod
    def update_clock_settings(cls, parameters, _, webserver):
        clock = webserver.get_scoreboard().get_clock()
        try:
            clock.set_mode(MasterClock.ClockMode(parameters['clock_mode']))
            clock.set_seconds(int(parameters['clock_seconds']))
            clock.set_minutes(int(parameters['clock_minutes']))
        except ValueError as e:
            print(e)
        except TypeError as e:
            print(e)
        finally:
            clock.submit()

    @classmethod
    def start_clock(cls, parameters, websocket_handler, webserver):
        clock = webserver.get_scoreboard().get_clock()
        clock.start()

    @classmethod
    def stop_clock(cls, parameters, websocket_handler, webserver):
        clock = webserver.get_scoreboard().get_clock()
        clock.stop()

    @classmethod
    def register_display(cls, parameters, websocket_handler, webserver):
        display_list = webserver.get_display_list()
        display_list.add_display(websocket_handler)

    @classmethod
    def change_display_appearance(cls, parameters, websocket_handler, webserver):
        display_list = webserver.get_display_list()
        appearance_id = parameters['appearance_id']
        display_list.set_appearance(websocket_handler, appearance_id)


class WebsocketHandler(tornado.websocket.WebSocketHandler, ClockEventListener):

    # MARK: Websocket live cycle

    def initialize(self, webserver):
        self.__webserver = webserver

    def open(self):
        scoreboard = self.__webserver.get_scoreboard()
        scoreboard.add_listener(self)
        clock = self.__webserver.get_scoreboard().get_clock()
        clock.add_listener(self)
        print("Socket open")

    def on_message(self, message):
        try:
            data = json.loads(message)
            command = data['command']
            parameters = data['parameters']
        except json.JSONDecodeError:
            print("Invalid message:", message)
        except ValueError:
            print("Invalid message:", message)
        else:
            self._execute_command(command, parameters)

    def on_close(self):
        scoreboard = self.__webserver.get_scoreboard()
        scoreboard.remove_listener(self)
        clock = self.__webserver.get_scoreboard().get_clock()
        clock.remove_listener(self)
        display_list = self.__webserver.get_display_list()
        display_list.remove_display(self)
        print("Socket closed")

    # MARK: Display functions

    def show_identification(self, id_string):
        message = '{"event": "%s", "data": {"id_string": %s}}' % (Event.SHOW_IDENTIFICATION.value, id_string)
        self.write_message(message)

    def change_appearance(self, appearance_id):
        message = '{"event": "%s", "data": {"appearance_id": %s}}' % (Event.CHANGE_APPEARANCE.value, appearance_id)
        self.write_message(message)

    # MARK:  GameClockEventListener

    def on_clock_update(self, clock):
        data = clock.get_json_string()
        message = '{"event": "%s", "data": %s}' % (Event.CLOCK_UPDATE.value, data)
        self.write_message(message)

    def on_time_update(self, minutes, seconds):
        message = '{"event": "%s", "data": {"minutes": %s, "seconds": %s}}' % (Event.TIME_UPDATE.value,
                                                                               minutes,
                                                                               seconds)
        self.write_message(message)

    # MARK: ScoreboardEventListener

    def on_scoreboard_update(self, scoreboard):
        data = scoreboard.get_json_string()
        message = '{ "event": "%s", "data": %s }' % (Event.SCOREBOARD_UPDATE.value, data)
        self.write_message(message)

    # MARK: Protected helper methods

    def _execute_command(self, command, parameters):
        try:
            method = getattr(CommandLib, command)
        except AttributeError:
            print("Unknown command:", command, parameters)
        else:
            method(parameters, self, self.__webserver)
