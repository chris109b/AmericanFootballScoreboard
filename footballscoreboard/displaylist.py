#!/usr/bin/env python3

# Python standard library imports
import json
# Imports from external modules
# Internal modules import


class DisplayList:

    __APPEARANCES = {"display_simple": "Simple Scoreboard",
                     "display_american_football": "American Football Scoreboard"}

    def __init__(self):
        self.__display_dict = {}

    def add_display(self, display, display_id):
        try:
            display_id = int(display_id)
        except TypeError:
            display_id = 0
        while ("%d" % display_id) in self.__display_dict.keys():
            display_id += 1
        id_string = "%d" % display_id
        self.__display_dict[id_string] = display
        display.show_identification(id_string)

    def remove_display(self, display_to_remove):
        filtered_list = {key: value for key, value in self.__display_dict.items() if value is not display_to_remove}
        self.__display_dict = filtered_list

    def set_appearance(self, display_id, appearance_id):
        if appearance_id in self.__APPEARANCES.keys():
            display = self.__display_dict[display_id]
            display.change_appearance(display_id, appearance_id)

    def show_all_display_identifications(self):
        for display_id, display in self.__display_dict.items():
            display.show_identification(display_id)

    def show_identification(self, display_id):
        display = self.__display_dict[display_id]
        display.show_identification(display_id)

    def get_all_display_ids(self):
        return list(self.__display_dict.keys())

    def get_all_appearances(self):
        return self.__APPEARANCES

    def get_json_data(self):
        display_list = list(self.__display_dict.keys())
        appearance_dict = self.__APPEARANCES
        data = {'display_list': display_list,
                'appearance_dict': appearance_dict}
        json_data = json.dumps(data)
        return json_data
