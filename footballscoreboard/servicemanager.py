#!/usr/bin/env python3

# Python standard library imports
import socket
import subprocess
# Imports from external modules
import netifaces
import zeroconf


class ServiceManager(object):

    def __init__(self):
        self.__port = None
        self.__full_qualified_domain_name = None
        self.__hostname = None
        self.__ip4_address_list = []
        self.__port = None
        self.__service_info_list = []

        self.__zeroconf = zeroconf.Zeroconf()
        self.__service_name = 'Football Scoreboard'
        self.__service_description = {'service': 'Football Scoreboard', 'version': '1.0.0'}

    def _get_free_port(self):
        self.__full_qualified_domain_name = socket.gethostname()
        self.__hostname = self.__full_qualified_domain_name.split('.')[0]
        self.__ip4_address = socket.gethostbyname(self.__full_qualified_domain_name)
        s = socket.socket()
        s.bind(('0.0.0.0', 0))
        self.__port = s.getsockname()[1]
        s.close()
        for network_interface in netifaces.interfaces():
            addresses = netifaces.ifaddresses(network_interface)
            try:
                ip4_address = addresses[2][0]['addr']
            except KeyError:
                continue
            if ip4_address != '127.0.0.1':
                self.__ip4_address_list.append(ip4_address)
                uri = "http://{0}:{1}/".format(ip4_address, self.__port)
                subprocess.run(['qrencode', '--type=UTF8', '--output=-', uri])
                print(uri)

    def get_port(self):
        return self.__port

    def start_service(self):
        self._get_free_port()
        for ip4_address in self.__ip4_address_list:
            service_info = zeroconf.ServiceInfo('_http._tcp.local.',
                                                self.__hostname + ' ' + self.__service_name + '._http._tcp.local.',
                                                socket.inet_aton(ip4_address), self.__port, 0, 0,
                                                self.__service_description, self.__hostname + '.local.')
            self.__service_info_list.append(service_info)
        for service_info in self.__service_info_list:
            try:
                self.__zeroconf.register_service(service_info)
            except zeroconf.NonUniqueNameException:
                print("Warning service has already been announced via zeroconf.")

    def stop_service(self):
        for service_info in self.__service_info_list:
            self.__zeroconf.unregister_service(service_info)
