#!/usr/bin/env python3

# Python standard library imports
from enum import Enum
import json
# Imports from external modules
# Internal modules import
from .gameclock import GameClock, GameClockDelegate


class ScoreboardEventListener:

    def on_scoreboard_update(self, scoreboard):
        raise NotImplementedError

    def on_clock_update(self, entries, update_count, json_string):
        raise NotImplementedError


class ScoreboardEntry:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.has_changed = False

    def change(self, value):
        if value != self.value:
            self.value = value
            self.has_changed = True

    def submit(self):
        self.has_changed = False


class Scoreboard(object):

    KEY_HOME_TEAM = "home_team"
    KEY_HOME_SCORE = "home_score"
    KEY_HOME_TIMEOUTS_LEFT = "home_timeouts_left"

    KEY_GUEST_TEAM = "guest_team"
    KEY_GUEST_SCORE = "guest_score"
    KEY_GUEST_TIMEOUTS_LEFT = "guest_timeouts_left"

    KEY_GAME_PHASE = "game_phase"
    KEY_GAME_CLOCK_MIN = "game_clock_minutes"
    KEY_GAME_CLOCK_SEC = "game_clock_seconds"

    KEY_GAME_OFFENCIVE_TEAM = "game_offencive_team"

    KEY_GAME_DOWN = "game_down"
    KEY_GAME_YARDS_TO_GO = "game_yards_to_go"
    KEY_GAME_BALL_ON = "game_ball_on"

    class OffenciveTeam(Enum):
        HOME = "Home"
        GUEST = "Guest"

    class GamePhase(Enum):
        PRE_GAME = "Pre Game"
        QTR_1 = "1st Qtr."
        QTR_2 = "2nd Qtr."
        HALF_TIME = "Half Time"
        QTR_3 = "3rd Qtr."
        QTR_4 = "4th Qtr."
        END = "End"

    def __init__(self):
        self._minutes_entry = ScoreboardEntry(Scoreboard.KEY_GAME_CLOCK_MIN, 12)
        self._second_entry = ScoreboardEntry(Scoreboard.KEY_GAME_CLOCK_SEC, 0)
        self._entries = [ScoreboardEntry(Scoreboard.KEY_HOME_TEAM, "Home"),
                         ScoreboardEntry(Scoreboard.KEY_HOME_SCORE, 0),
                         ScoreboardEntry(Scoreboard.KEY_HOME_TIMEOUTS_LEFT, 3),
                         ScoreboardEntry(Scoreboard.KEY_GUEST_TEAM, "Guest"),
                         ScoreboardEntry(Scoreboard.KEY_GUEST_SCORE, 0),
                         ScoreboardEntry(Scoreboard.KEY_GUEST_TIMEOUTS_LEFT, 3),
                         ScoreboardEntry(Scoreboard.KEY_GAME_OFFENCIVE_TEAM, Scoreboard.OffenciveTeam.HOME),
                         ScoreboardEntry(Scoreboard.KEY_GAME_DOWN, 0),
                         ScoreboardEntry(Scoreboard.KEY_GAME_YARDS_TO_GO, 10),
                         ScoreboardEntry(Scoreboard.KEY_GAME_BALL_ON, 50),
                         ScoreboardEntry(Scoreboard.KEY_GAME_PHASE, Scoreboard.GamePhase.PRE_GAME),
                         self._minutes_entry,
                         self._second_entry]
        self._event_listeners = []
        self._plugins = []
        self._update_count = 0
        self._clock = GameClock(self)

    # MARK: Accessing Data

    def update_clock(self, minutes, seconds):
        # Update values
        self._minutes_entry.change(int(minutes))
        self._second_entry.change(int(seconds))
        self._update_count += 1
        # Create JSON string
        json_data = {'update_counter': self._update_count, 'scoreboard': {}}
        entries = [self._minutes_entry, self._second_entry]
        for entry in entries:
            json_data['scoreboard'][entry.key] = entry.value
        json_string = json.dumps(json_data)
        # Inform listeners
        for listener in self._event_listeners:
            listener.on_clock_update(entries, self._update_count, json_string)

    def get_clock(self):
        return self._clock

    def set(self, key, value):
        for entry in self._entries:
            if entry.key == key:
                entry.change(value)
                break

    def get(self, key):
        for entry in self._entries:
            if entry.key == key:
                return entry.value

    def get_all_entries(self):
        return self._entries

    def get_changed_entries(self):
        changed_entries = []
        for entry in self._entries:
            if entry.has_changed:
                changed_entries.append(entry)
        return changed_entries

    def get_update_count(self):
        return self._update_count

    def get_json_string(self):
        data = {'update_counter': self._update_count, 'scoreboard': {}}
        for entry in self._entries:
            value = (entry.value.value if isinstance(entry.value, Enum) else entry.value)
            data['scoreboard'][entry.key] = value
        return json.dumps(data)

    # MARK: Data live cycle

    def submit(self):
        self._update_count += 1
        for listener in self._event_listeners:
            listener.on_scoreboard_update(self)
        for plugin in self._plugins:
            plugin.update(self)
        for entry in self._entries:
            entry.submit()

    # MARK: Handling plugins

    def add_plugin(self, plugin):
        if not plugin.is_disabled():
            self._plugins.append(plugin)

    def start(self):
        for plugin in self._plugins:
            plugin.start(self)

    def stop(self):
        for plugin in self._plugins:
            plugin.stop(self)

    # MARK: Event listeners

    def add_listener(self, listener):
        self._event_listeners.append(listener)

    def remove_listener(self, listener):
        self._event_listeners.remove(listener)
