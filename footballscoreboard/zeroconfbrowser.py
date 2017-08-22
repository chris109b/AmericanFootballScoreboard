#!/usr/bin/env python3

# Python standard library imports
import weakref
import time
# Imports from external modules
from zeroconf import ServiceBrowser, Zeroconf
# Internal modules import
from .zeroconfserviceregistration import ZeroConfServiceRegistration


class ZeroconfListener(object):

    def __init__(self, browser):
        self.__browser_ref = weakref.ref(browser)

    def add_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        self.__browser_ref().add_service(info)

    def remove_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        self.__browser_ref().remove_service(info)


class ZeroconfBrowser:

    def __init__(self, delegate=None):
        self.__zeroconf = None
        self.__listener = None
        self.__browser = None
        self.__service_list = []
        self.__observer_list = []
        self.__delegate = delegate

    def add_observer(self, observer):
        self.__observer_list.append(weakref.ref(observer))

    def remove_observer(self, observer):
        observer_ref_to_remove = None
        for observer_ref in self.__observer_list:
            if observer == observer_ref():
                observer_ref_to_remove = observer_ref
                break
        if observer_ref_to_remove is not None:
            self.__observer_list.remove(observer_ref_to_remove)

    def start(self, protocol=ZeroConfServiceRegistration.ServiceType.HTTP):
        self.__zeroconf = Zeroconf()
        self.__listener = ZeroconfListener(self)
        self.__browser = ServiceBrowser(self.__zeroconf, protocol.value, self.__listener)

    def stop(self):
        self.__zeroconf.close()
        self.__zeroconf = None
        self.__listener = None
        self.__browser = None

    def get_service_list(self):
        return self.__service_list

    def add_service(self, info):
        if self.__delegate is not None and self.__delegate.is_service_valid(info) == False:
            return
        self.__service_list.append(info)
        for observer_ref in self.__observer_list:
            observer_ref().on_did_update_service_list(self)

    def remove_service(self, info):
        self.__service_list.remove(info)
        for observer_ref in self.__observer_list:
            observer_ref().on_did_update_service_list(self)
