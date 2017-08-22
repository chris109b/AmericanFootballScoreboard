#!/usr/bin/env python3

# Python standard library imports
import socket
import subprocess
from enum import Enum
# Imports from external modules
import netifaces
from zeroconf import ServiceInfo, Zeroconf


class ZeroConfServiceRegistration:

    class ServiceType(Enum):
        HTTP = "_http._tcp.local."

    def __init__(self):
        self._service_list = []
        self._zeroconf = Zeroconf()

    def _get_unique_name(self, name):
        name_candidate = None
        for index in range(0, 9999):
            if index == 0:
                name_candidate = name
            else:
                name_candidate = "{} ({})".format(name, index)
            name_already_exists = False
            for _, service_name, _, _, _ in self._service_list:
                if name_candidate == service_name:
                    name_already_exists = True
                    break
            if name_already_exists is False:
                break
        return name_candidate

    @classmethod
    def _get_network_interfaces(cls):
        interface_list = []
        for network_interface in netifaces.interfaces():
            addresses = netifaces.ifaddresses(network_interface)
            try:
                ip4_address = addresses[2][0]['addr']
            except KeyError:
                continue
            if ip4_address != '127.0.0.1':
                interface_list.append((network_interface, ip4_address))
        return interface_list

    @classmethod
    def _get_unique_port(cls):
        s = socket.socket()
        s.bind(('0.0.0.0', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    @classmethod
    def _get_hostname(cls):
        full_qualified_domain_name = socket.gethostname()
        hostname = full_qualified_domain_name.split('.')[0]
        return hostname

    def register_service(self, service_type, service_name, port=None, description=None):
        if description is None:
            description = {}
        if port is None:
            port = ZeroConfServiceRegistration._get_unique_port()
        hostname = ZeroConfServiceRegistration._get_hostname()
        network_interface_list = ZeroConfServiceRegistration._get_network_interfaces()
        for interface_name, ip_address in network_interface_list:
            service_name = self._get_unique_name(service_name)
            info = ServiceInfo(service_type.value,
                               service_name + "." + service_type.value,
                               socket.inet_aton(ip_address), port, 0, 0,
                               description, hostname)
            self._service_list.append((service_type, service_name, ip_address, port, info))
            self._zeroconf.register_service(info)
        return port

    def remove_service(self, port_to_remove):
        for _, _, _, port, info in self._service_list:
            if port == port_to_remove:
                self._zeroconf.unregister_service(info)

    def stop(self):
        for _, _, _, _, info in self._service_list:
            self._zeroconf.unregister_service(info)

    def print_service_urls(self):
        for service_type, service_name, ip_address, port, _ in self._service_list:
            if service_type == ZeroConfServiceRegistration.ServiceType.HTTP:
                protocol = "http"
            else:
                protocol = None
            if protocol is not None:
                uri = "{0}://{1}:{2}/".format(protocol, ip_address, port)
                print("\n{}".format(service_name))
                try:
                    subprocess.run(['qrencode', '--type=UTF8', '--output=-', uri])
                except FileNotFoundError:
                    print("Error: Command not found: qrencode")
                print("{}\n".format(uri))