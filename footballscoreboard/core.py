#!/usr/bin/env python3


class Core:
    KEY_NET_APP_VENDOR_UUID = 'net_app_vendor_uuid'
    KEY_NET_APP_META_PATH = 'net_app_info_path'
    KEY_API_ID = 'api_id'
    KEY_API_INITIAL_DATA_PATH = 'api_initial_data_path'
    KEY_API_WEBSOCKET_PATH = 'api_websocket_path'

    PRODUCT_NAME = 'American Football Scoreboard'

    DISPLAY_LIST_PATH = "/display-list.json"
    INITIAL_DATA_PATH = "/display.json"
    WEBSOCKET_PATH = "/websocket"

    DESCRIPTION = {KEY_NET_APP_VENDOR_UUID: "chris109@web.de",
                   KEY_NET_APP_META_PATH: "/netapp.json",
                   KEY_API_ID: "Scoreboard 0.1",
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
