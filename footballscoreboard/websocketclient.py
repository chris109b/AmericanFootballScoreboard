#!/usr/bin/env python3

# Python standard library imports
import weakref
# Imports from external modules
from tornado import escape
from tornado import gen
from tornado import httpclient
from tornado import httputil
from tornado import ioloop
from tornado import websocket
# Internal modules import
from .core import Core


class WebsocketClient:

    CONNECT_TIMEOUT = 60
    REQUEST_TIMEOUT = 60

    def __init__(self, initial_data_url, websocket_url, delegate):
        self.__initial_data_url = initial_data_url
        self.__websocket_url = websocket_url
        self.__delegate_ref = weakref.ref(delegate)
        self.__websocket = None

    def _fetch_initial_data(self):
        data = None
        headers = httputil.HTTPHeaders({'Content-Type': Core.DATA_MIME_TYPE})
        http_client = httpclient.HTTPClient()
        try:
            response = http_client.fetch(self.__initial_data_url, headers=headers)
            data = response.body
        except httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            print("Error: " + str(e))
        except Exception as e:
            # Other errors are possible, such as IOError.
            print("Error: " + str(e))
        finally:
            http_client.close()
        return data.decode(Core.ENCODING)

    def _open_websocket_connection(self):
        headers = httputil.HTTPHeaders({'Content-Type': Core.DATA_MIME_TYPE})
        request = httpclient.HTTPRequest(url=self.__websocket_url,
                                         connect_timeout=WebsocketClient.CONNECT_TIMEOUT,
                                         request_timeout=WebsocketClient.REQUEST_TIMEOUT,
                                         headers=headers)
        connection = websocket.WebSocketClientConnection(ioloop.IOLoop.current(), request)
        connection.connect_future.add_done_callback(self._on_websocket_connection_established)

    def _on_websocket_connection_established(self, future):
        if future.exception() is None:
            self.__websocket = future.result()
            self._on_connection_success()
            self._read_messages()
        else:
            self._on_connection_error(future.exception())

    @gen.coroutine
    def _read_messages(self):
        while True:
            data = yield self.__websocket.read_message()
            if data is None:
                self._on_connection_close()
                break
            self._on_message(data)

    def _on_message(self, data):
        self.__delegate_ref().process_json_data(data)

    def _on_connection_success(self):
        pass

    def _on_connection_close(self):
        pass

    def _on_connection_error(self, exception):
        raise exception

    def connect(self):
        data = self._fetch_initial_data()
        if data is not None:
            self.__delegate_ref().process_json_data(data)
        self._open_websocket_connection()

    def send(self, data):
        if not self.__websocket:
            raise RuntimeError('Web socket connection is closed.')
        self.__websocket.write_message(escape.utf8(data))

    def disconnect(self):
        if not self.__websocket:
            raise RuntimeError('Web socket connection is already closed.')
        self.__websocket.close()
