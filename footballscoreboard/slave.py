#!/usr/bin/env python3

# Python standard library imports
import json
# Imports from external modules
import tornado
# Internal modules import
from .zeroconfbrowser import ZeroconfBrowser
from .websocketclient import WebsocketClient
from .core import Core
from .scoreboard import Scoreboard


class Slave:

    def __init__(self, scoreboard, clock):
        # Application info
        self.__vendor_name = 'Christian Beuschel'
        self.__product_name = 'American Football Scoreboard'
        self.__version_string = '0.1'
        # Other parts of the application
        self.__scoreboard = scoreboard
        self.__clock = clock
        # Actual network services
        self.__zeroconf_browser = None
        self.__websocket_client = None
        self.__master_service = None

    def start(self):
        self.__zeroconf_browser = ZeroconfBrowser(delegate=self)
        self.__zeroconf_browser.add_observer(self)
        self.__zeroconf_browser.start()
        tornado.ioloop.IOLoop.instance().start()

    def stop(self):
        self.__zeroconf_browser.start()
        if self.__websocket_client is not None:
            self.__websocket_client.disconnect()

    def log(self, message):
        print(message)

    def is_service_valid(self, info):
        properties = Core.decode(info.properties)
        try:
            if properties[Core.KEY_VENDOR_NAME] != Core.DESCRIPTION[Core.KEY_VENDOR_NAME]:
                raise KeyError
            if properties[Core.KEY_PRODUCT_NAME] != Core.DESCRIPTION[Core.KEY_PRODUCT_NAME]:
                raise KeyError
            if properties[Core.KEY_PRODUCT_VERSION] != Core.DESCRIPTION[Core.KEY_PRODUCT_VERSION]:
                raise KeyError
        except KeyError:
            return False
        else:
            return True

    def on_did_update_service_list(self, browser):
        service_list = browser.get_service_list()
        first_service = service_list[0]
        if len(service_list) == 0:
            if self.__websocket_client is not None:
                self.__websocket_client.disconnect()
            self.__websocket_client = None
        elif self.__master_service != first_service:
            if self.__websocket_client is not None:
                self.__websocket_client.disconnect()
            self.__master_service = first_service
            ipv4_address = '.'.join(map(str, self.__master_service.address))
            port = self.__master_service.port
            initial_data_url = "http://{0}:{1}{2}".format(ipv4_address, port, Core.INITIAL_DATA_PATH)
            websocket_url = "ws://" + ipv4_address + ":" + str(port) + Core.WEBSOCKET_PATH
            self.__websocket_client = WebsocketClient(initial_data_url, websocket_url, self)
            self.log("Connecting to master: http://{0}:{1}".format(ipv4_address, port))
            self.__websocket_client.connect()

    def receive_scoreboard_update(self, payload):
        values = payload['scoreboard']
        # Home Team
        home_team = values['home_team']
        home_score = int(values['home_score'])
        home_timeouts_left = int(values['home_timeouts_left'])
        # Guest team
        guest_team = values['guest_team']
        guest_score = int(values['guest_score'])
        guest_timeouts_left = int(values['guest_timeouts_left'])
        # Game phase
        game_phase = Scoreboard.GamePhase(values['game_phase'])
        # Ball
        game_offencive_team = Scoreboard.OffenciveTeam(values['game_offencive_team'])
        game_down = int(values['game_down'])
        game_yards_to_go = int(values['game_yards_to_go'])
        game_ball_on = int(values['game_ball_on'])
        # Apply changes to scoreboard
        # Home team
        self.__scoreboard.set(Scoreboard.KEY_HOME_TEAM, home_team)
        self.__scoreboard.set(Scoreboard.KEY_HOME_SCORE, home_score)
        self.__scoreboard.set(Scoreboard.KEY_HOME_TIMEOUTS_LEFT, home_timeouts_left)
        # Guest team
        self.__scoreboard.set(Scoreboard.KEY_GUEST_TEAM, guest_team)
        self.__scoreboard.set(Scoreboard.KEY_GUEST_SCORE, guest_score)
        self.__scoreboard.set(Scoreboard.KEY_GUEST_TIMEOUTS_LEFT, guest_timeouts_left)
        # Ball
        self.__scoreboard.set(Scoreboard.KEY_GAME_OFFENCIVE_TEAM, game_offencive_team)
        self.__scoreboard.set(Scoreboard.KEY_GAME_DOWN, game_down)
        self.__scoreboard.set(Scoreboard.KEY_GAME_YARDS_TO_GO, game_yards_to_go)
        self.__scoreboard.set(Scoreboard.KEY_GAME_BALL_ON, game_ball_on)
        # Game phase
        self.__scoreboard.set(Scoreboard.KEY_GAME_PHASE, game_phase)
        # Submit updates
        self.__scoreboard.submit()

    def receive_clock_update(self, payload):
        seconds = payload["seconds"]
        minutes = payload["minutes"]
        mode = payload["mode"]
        is_ticking = payload["is_ticking"]
        self.__clock.update_clock_settings(mode, is_ticking, minutes, seconds)

    def receive_time_update(self, payload):
        seconds = int(payload["seconds"])
        minutes = int(payload["minutes"])
        self.__clock.update_time(minutes, seconds)

    def process_json_data(self, data):
        data = json.loads(data)
        event = data["event"]
        if event == "time_update":
            payload = data["data"]
            self.receive_time_update(payload)
        elif event == "clock_update":
            payload = data["data"]
            self.receive_clock_update(payload)
        elif event == "scoreboard_update":
            payload = data["data"]
            self.receive_scoreboard_update(payload)
        else:
            print("Unknown event:", event)

