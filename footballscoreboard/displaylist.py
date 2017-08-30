#!/usr/bin/env python3

# Python standard library imports
# Imports from external modules
# Internal modules import


class DisplayList:

    __APPEARANCES = {"simple_scoreboard": "Simple Scoreboard",
                     "american_football_scoreboard": "American Football Scoreboard"}

    def __init__(self):
        self.__display_dict = {}

    def add_display(self, display):
        display_id = len(self.__display_list)
        while ("%d" % display_id) in self.__display_dict.keys():
            display_id += 1
        id_string = "%d" % display_id
        self.__display_dict[id_string] = display
        display.show_identification(id_string)

    def remove_display(self, display_to_remove):
        filtered_list = {key: value for key, value in self.__display_dict.items() if value is not display_to_remove}
        self.__display_dict = filtered_list

    def set_appearance(self, display, appearance_id):
        if appearance_id in self.__APPEARANCES.keys():
            display.change_appearance(appearance_id)

    def show_identification(self, display_id):
        display = self.__display_dict[display_id]
        display.show_id(display_id)

    def get_all_display_ids(self):
        return self.__display_dict.keys()

    def get_all_appearances(self):
        return self.__APPEARANCES
