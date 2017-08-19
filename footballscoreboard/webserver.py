#!/usr/bin/env python3

# Imports from external modules
import tornado.web
import tornado.ioloop
# Internal modules import
from .servicemanager import ServiceManager
from .webhandler import DefaultHandler
from .websockethandler import WebSocketHandler


class Webserver(object):

    def __init__(self, scoreboard, ssl_cert_path):
        # Application info
        self.__vendor_name = 'Christian Beuschel'
        self.__product_name = 'FootballScoreboard'
        self.__version_string = '0.1'
        # Server configuration
        self.__ssl_cert_path = ssl_cert_path
        # Other parts of the application
        self.__scoreboard = scoreboard
        # Actual network services
        self.__service_manager = None
        self.__web_service = None

    def get_scoreboard(self):
        return self.__scoreboard

    def log(self, message):
        print(message)

    def start(self):
        # Publishing services
        self.__service_manager = ServiceManager()
        self.__service_manager.start_service()
        # Executing server
        handlers = [(r'/websocket', WebSocketHandler, dict(webserver=self)),
                    (r'.*', DefaultHandler, dict(webserver=self))]
        self.__web_service = tornado.web.Application(handlers)
        self.__web_service.listen(self.__service_manager.get_port())
        tornado.ioloop.IOLoop.instance().start()

    def stop(self):
        tornado.ioloop.IOLoop.current().stop()
        self.__web_service = None
        self.__service_manager.stop_service()
