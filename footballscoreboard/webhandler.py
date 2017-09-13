#!/usr/bin/env python3

# Python standard library imports
import urllib
import os
# Imports from external modules
from tornado.web import *
from tornado import gen
# Internal modules import
from .scoreboard import Scoreboard
from .core import Core
from .masterclock import MasterClock

class DefaultHandler(tornado.web.RequestHandler):

    HT_DOCUMENT_PATH = "htdocs"

    HT_TEMPLATES = {"/display_simple.html": ("display_simple.html", "text/html"),
                    "/display_american_football.html": ("display_american_football.html", "text/html"),
                    "/remote.html": ("remote.html", "text/html"),
                    "/remote_control_interface.html": ("remote_control_interface.html", "text/html")}

    HT_FILES = {"/index.html": ("index.html", "text/html"),
                "/css/index.css": ("index.css", "text/css"),
                "/js/remote_control_interface.js": ("remote_control_interface.js", "application/javascript"),
                "/js/display.js": ("display.js", "application/javascript"),
                "/js/jquery.js": ("jquery.js", "application/javascript"),
                "/css/remote.css": ("remote.css", "text/css"),
                "/css/remote_control_interface.css": ("remote_control_interface.css", "text/css"),
                "/css/display_american_football.css": ("display_american_football.css", "text/css"),
                "/img/display_american_football.png": ("display_american_football.png", "image/png"),
                "/css/display_simple.css": ("display_simple.css", "text/css"),
                "/img/display_simple.png": ("display_simple.png", "image/png"),
                "/favicon.ico": ("favicon.ico", "image/x-icon"),
                "/netapp.json": ("netapp.json", "application/javascript"),
                "/netapp_48.png": ("netapp_48.png", "image/png"),
                "/netapp_64.png": ("netapp_64.png", "image/png"),
                "/netapp_96.png": ("netapp_96.png", "image/png"),
                "/netapp_128.png": ("netapp_128.png", "image/png"),
                "/netapp_192.png": ("netapp_192.png", "image/png"),
                "/favicons/57.png": ("favicon_57.png", "image/png"),
                "/favicons/72.png": ("favicon_72.png", "image/png"),
                "/favicons/114.png": ("favicon_144.png", "image/png"),
                "/img/hide_keyboard.png": ("hide_keyboard.png", "image/png"),
                "/football_icon.png": ("football_icon.png", "image/png")}

    def log(self, message):
        self.__webserver.log(message)

    def send_file_not_found_error(self):
        message = "Error: 404 File Not Found: {0}".format(self.request.path)
        self.log(message)
        raise HTTPError(404)

    def send_common_error(self):
        message = "Error: 500 Internal error"
        self.log(message)
        raise HTTPError(500)

    def send_data(self, data, mime_type):
        if data is None:
            self.send_file_not_found_error()
            return
        if mime_type is None:
            mime_type = "application/octet-stream"
        self.set_header("Content-Type", mime_type)
        self.write(data)
        self.finish()

    def send_file_at_path(self, file_path, mime_type=None):
        file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), file_path))
        try:
            if mime_type is None:
                file_url = urllib.pathname2url(file_path)
                mime_type, encoding = mimetypes.guess_type(file_url)
            if mime_type is None:
                mime_type = "application/octet-stream"
            f = open(file_path, mode='rb')
            self.set_header("Content-Type", mime_type)
            self.write(f.read())
            f.close()
            self.finish()
        except IOError:
            self.send_file_not_found_error()

    def initialize(self, webserver):
        self.__webserver = webserver

    def send_page(self, file_path):
        scoreboard = self.__webserver.get_scoreboard()
        clock = self.__webserver.get_scoreboard().get_clock()
        # HTML rendering
        self.render(file_path,
                    offence_home_value=Scoreboard.OffenciveTeam.HOME.value,
                    offence_guest_value=Scoreboard.OffenciveTeam.GUEST.value,
                    game_phase_list=[element.value for element in Scoreboard.GamePhase],
                    game_phase=scoreboard.get(Scoreboard.KEY_GAME_PHASE),
                    home_team=scoreboard.get(Scoreboard.KEY_HOME_TEAM),
                    home_score=scoreboard.get(Scoreboard.KEY_HOME_SCORE),
                    home_timeouts_left=scoreboard.get(Scoreboard.KEY_HOME_TIMEOUTS_LEFT),
                    guest_team=scoreboard.get(Scoreboard.KEY_GUEST_TEAM),
                    guest_score=scoreboard.get(Scoreboard.KEY_GUEST_SCORE),
                    guest_timeouts_left=scoreboard.get(Scoreboard.KEY_GUEST_TIMEOUTS_LEFT),
                    game_offencive_team=scoreboard.get(Scoreboard.KEY_GAME_OFFENCIVE_TEAM),
                    game_down=scoreboard.get(Scoreboard.KEY_GAME_DOWN),
                    game_yards_to_go=scoreboard.get(Scoreboard.KEY_GAME_YARDS_TO_GO),
                    game_ball_on=scoreboard.get(Scoreboard.KEY_GAME_BALL_ON),
                    game_clock_minutes=scoreboard.get_clock().get_minutes(),
                    game_clock_seconds=scoreboard.get_clock().get_seconds(),
                    clock_mode_list=[element.value for element in MasterClock.ClockMode],
                    clock_mode=clock.get_mode(),
                    clock_minutes=clock.get_minutes(),
                    clock_seconds=clock.get_seconds(),
                    clock_is_ticking=clock.is_ticking())

    def send_display_json_data(self):
        scoreboard = self.__webserver.get_scoreboard()
        json_data = scoreboard.get_json_string()
        self.set_header("Content-Type", Core.DATA_MIME_TYPE)
        self.write(json_data)
        self.finish()

    def send_display_list_json_data(self):
        display_list = self.__webserver.get_display_list()
        json_data = display_list.get_json_data()
        self.set_header("Content-Type", Core.DATA_MIME_TYPE)
        self.write(json_data)
        self.finish()
                
    def send_reply(self):
        path = self.request.path
        if path == "/":
            path = "/index.html"
        if path == Core.DISPLAY_LIST_PATH:
            self.send_display_list_json_data()
            return
        if path == Core.INITIAL_DATA_PATH:
            self.send_display_json_data()
            return
        if path in self.HT_TEMPLATES.keys():
            file_name, mime_type = self.HT_TEMPLATES[path]
            file_path = os.path.join(DefaultHandler.HT_DOCUMENT_PATH, file_name)
            self.send_page(file_path)
            return
        if path in self.HT_FILES.keys():
            file_name, mime_type = self.HT_FILES[path]
            file_path = os.path.join(DefaultHandler.HT_DOCUMENT_PATH, file_name)
            self.send_file_at_path(file_path, mime_type)
            return
        self.send_file_not_found_error()

    @asynchronous
    def get(self):
        self.send_reply()
