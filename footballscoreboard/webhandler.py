#!/usr/bin/env python3

# Python standard library imports
import urllib
import os
# Imports from external modules
from tornado.ioloop import IOLoop
from tornado.web import *
from tornado import gen
# Internal modules import
from .scoreboard import Scoreboard


class DefaultHandler(RequestHandler):

    ENCODING = "utf-8"
    HT_DOCUMENT_PATH = "htdocs"

    HT_TEMPLATES = {"/display.html": ("display.html", "text/html"),
                    "/remote.html": ("remote.html", "text/html")}

    HT_FILES = {"/index.html": ("index.html", "text/html"),
                "/css/index.css": ("index.css", "text/css"),
                "/js/display.js": ("display.js", "application/javascript"),
                "/js/jquery.js": ("jquery.js", "application/javascript"),
                "/css/remote.css": ("remote.css", "text/css"),
                "/css/display.css": ("display.css", "text/css"),
                "/favicon.ico": ("favicon.ico", "image/x-icon"),
                "/favicons/57.png": ("favicon_57.png", "image/png"),
                "/favicons/72.png": ("favicon_72.png", "image/png"),
                "/favicons/114.png": ("favicon_144.png", "image/png"),
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
                url = urllib.pathname2url(file_path)
                mime_type, encoding = mimetypes.guess_type(url)
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
                    game_clock_minutes=scoreboard.get(Scoreboard.KEY_GAME_CLOCK_MIN),
                    game_clock_seconds=scoreboard.get(Scoreboard.KEY_GAME_CLOCK_SEC))

    @gen.engine
    def send_display_json_data(self, client_update_count):
        scoreboard = self.__webserver.get_scoreboard()
        json_data = scoreboard.get_json_string()
        print(json_data)
        current_update_count = scoreboard.get_update_count()
        if client_update_count == current_update_count:
            yield gen.Task(IOLoop.instance().add_timeout, time.time() + 5)
        #    delay = 21.0
        #    notification_center = NotificationCenter.shared_instance()
        #    notification_center.wait_once_for_event_with_timeout(Notification.NOTIFY_SCOREBOARD_UPDATE.value, delay)
        json_data = scoreboard.get_json_string()
        self.set_header("Content-Type", "application/json")
        self.write(json_data)
        self.finish()
                
    def send_reply(self):
        path = self.request.path
        if path == "/":
            path = "/index.html"
        
        if path == "/display.json":
            print("/display.json")
            update_count = int(self.request.query_arguments['count'][0])
            self.send_display_json_data(update_count)
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

    @asynchronous
    def post(self, *args, **kwargs):
        arguments = self.request.body_arguments
        try:
            # Home teams
            home_team = arguments['home_team'][0].decode(DefaultHandler.ENCODING)
            home_score = int(arguments['home_score'][0].decode(DefaultHandler.ENCODING))
            home_timeouts_left = int(arguments['home_timeouts_left'][0].decode(DefaultHandler.ENCODING))
            # Guest team
            guest_team = arguments['guest_team'][0].decode(DefaultHandler.ENCODING)
            guest_score = int(arguments['guest_score'][0].decode(DefaultHandler.ENCODING))
            guest_timeouts_left = int(arguments['guest_timeouts_left'][0].decode(DefaultHandler.ENCODING))
            # Game phase
            game_phase = Scoreboard.GamePhase(arguments['game_phase'][0].decode(DefaultHandler.ENCODING))
            # Clock
            game_clock_minutes = int(arguments['game_clock_minutes'][0].decode(DefaultHandler.ENCODING))
            game_clock_seconds = int(arguments['game_clock_seconds'][0].decode(DefaultHandler.ENCODING))
            # Ball
            offencive_team = Scoreboard.OffenciveTeam(arguments['game_offencive_team'][0].decode(DefaultHandler.ENCODING))
            game_down = int(arguments['game_down'][0].decode(DefaultHandler.ENCODING))
            game_yards_to_go = int(arguments['game_yards_to_go'][0].decode(DefaultHandler.ENCODING))
            game_ball_on = int(arguments['game_ball_on'][0].decode(DefaultHandler.ENCODING))
            # Apply changes to scoreboard
            scoreboard = self.__webserver.get_scoreboard()
            # Home team
            scoreboard.set(Scoreboard.KEY_HOME_TEAM, home_team)
            scoreboard.set(Scoreboard.KEY_HOME_SCORE, home_score)
            scoreboard.set(Scoreboard.KEY_HOME_TIMEOUTS_LEFT, home_timeouts_left)
            # Guest team
            scoreboard.set(Scoreboard.KEY_GUEST_TEAM, guest_team)
            scoreboard.set(Scoreboard.KEY_GUEST_SCORE, guest_score)
            scoreboard.set(Scoreboard.KEY_GUEST_TIMEOUTS_LEFT, guest_timeouts_left)
            # Ball
            scoreboard.set(Scoreboard.KEY_GAME_OFFENCIVE_TEAM, offencive_team)
            scoreboard.set(Scoreboard.KEY_GAME_DOWN, game_down)
            scoreboard.set(Scoreboard.KEY_GAME_YARDS_TO_GO, game_yards_to_go)
            scoreboard.set(Scoreboard.KEY_GAME_BALL_ON, game_ball_on)
            # Game phase
            scoreboard.set(Scoreboard.KEY_GAME_PHASE, game_phase)
            # Clock
            scoreboard.set(Scoreboard.KEY_GAME_CLOCK_MIN, game_clock_minutes)
            scoreboard.set(Scoreboard.KEY_GAME_CLOCK_SEC, game_clock_seconds)
        except ValueError as e:
            self.send_common_error()
            return
        except TypeError as e:
            self.send_common_error()
            return
        finally:
            scoreboard.submit()
        self.send_reply()
