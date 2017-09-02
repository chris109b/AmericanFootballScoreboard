#!/usr/bin/env python3


class Core:
    KEY_VENDOR_NAME = 'vendor_name'
    KEY_VENDOR_URI = 'vendor_uri'
    KEY_PRODUCT_NAME = 'product_name'
    KEY_PRODUCT_URI = 'product_uri'
    KEY_PRODUCT_VERSION = 'product_version'
    KEY_API_INITIAL_DATA_PATH = 'api_initial_data_path'
    KEY_API_WEBSOCKET_PATH = 'api_websocket_path'

    DISPLAY_LIST_PATH = "/display-list.json"
    INITIAL_DATA_PATH = "/display.json"
    WEBSOCKET_PATH = "/websocket"

    DESCRIPTION = {KEY_VENDOR_NAME: 'Christian Beuschel',
                   KEY_VENDOR_URI: 'http://chris-macht-fotos.de',
                   KEY_PRODUCT_NAME: 'American Football Scoreboard',
                   KEY_PRODUCT_URI: 'http://chris-macht-fotos.de/products/american-football-scoreboard/',
                   KEY_PRODUCT_VERSION: 'DEFAULT 0.1',
                   KEY_API_INITIAL_DATA_PATH: INITIAL_DATA_PATH,
                   KEY_API_WEBSOCKET_PATH: WEBSOCKET_PATH}

    ENCODING = "utf-8"
    DATA_MIME_TYPE = "application/json"

    PARAMETERS_MASTER_MODE = ["-M", "--master"]
    PARAMETERS_SLAVE_MODE = ["-S", "--slave"]

    @classmethod
    def decode(cls, data):
        if isinstance(data, bytes):
            return data.decode(Core.ENCODING)
        if isinstance(data, dict):
            return dict(map(Core.decode, data.items()))
        if isinstance(data, tuple):
            return map(Core.decode, data)
        return data
