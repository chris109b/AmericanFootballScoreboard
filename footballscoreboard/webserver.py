#!/usr/bin/env python3

# Imports from external modules
import tornado.web
import tornado.ioloop
# Internal modules import
from .zeroconfserviceregistration import ZeroConfServiceRegistration
from .webhandler import DefaultHandler
from .websockethandler import WebsocketHandler
from .core import Core


class Webserver(object):

    def __init__(self, scoreboard, ssl_cert_path):
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
        self.__service_manager = ZeroConfServiceRegistration()
        port = self.__service_manager.register_service(ZeroConfServiceRegistration.ServiceType.HTTP,
                                                       Core.DESCRIPTION[Core.KEY_PRODUCT_NAME],
                                                       description=Core.DESCRIPTION)
        self.__service_manager.print_service_urls()
        # Executing server
        handlers = [(r'/websocket', WebsocketHandler, dict(webserver=self)),
                    (r'.*', DefaultHandler, dict(webserver=self))]
        self.__web_service = tornado.web.Application(handlers)
        self.__web_service.listen(port)
        tornado.ioloop.IOLoop.current().start()

    def stop(self):
        tornado.ioloop.IOLoop.current().stop()
        self.__web_service = None
        self.__service_manager.stop()
