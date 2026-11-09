"""Read and write player profiles and completed matches in JSON files."""

import json
import os


class DataError(Exception):
    """A file could not be read or written safely."""


class DataManager:
    def __init__(self, folder=None):
        if folder is None:
            folder = os.path.join(os.path.dirname(__file__), "data")
        self.folder = folder
        self.player_file = os.path.join(folder, "players.json")
        self.history_file = os.path.join(folder, "history.json")
        try:
            os.makedirs(folder, exist_ok=True)
        except OSError as error:
            raise DataError("Cannot create the data folder.") from error

    def read_list(self, file_path):
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, ValueError) as error:
            raise DataError("Cannot read " + file_path) from error

        if not isinstance(data, list):
            raise DataError("Invalid data format in " + file_path)
        return data

    def write_list(self, file_path, data):
        """Write a temporary file first, to avoid damaging the old data."""
        temporary_file = file_path + ".tmp"
        try:
            with open(temporary_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            os.replace(temporary_file, file_path)
        except (OSError, TypeError, ValueError) as error:
            raise DataError("Cannot save " + file_path) from error

    def load_players(self):
        players = self.read_list(self.player_file)
        used_ids = []
        for item in players:
            if not isinstance(item, dict):
                raise DataError("Player data is not valid.")
            player_id = item.get("id")
            name = item.get("name")
            if (type(player_id) is not int or player_id < 1
                    or not isinstance(name, str) or not name.strip()
                    or player_id in used_ids):
                raise DataError("Player data is not valid.")
            used_ids.append(player_id)
        return players

    def save_players(self, players):
        self.write_list(self.player_file, players)

    def load_matches(self):
        matches = self.read_list(self.history_file)
        needed = (
            "match_id", "played_at", "player1_id", "player1_name",
            "player2_id", "player2_name", "winner_id", "winner_name",
            "stats",
        )
        for match in matches:
            if not isinstance(match, dict):
                raise DataError("Match history is not valid.")
            for field in needed:
                if field not in match:
                    raise DataError("Match history is missing information.")
            if not isinstance(match["stats"], dict):
                raise DataError("Match statistics are not valid.")
            for key in ("player1_id", "player2_id", "winner_id"):
                if type(match[key]) is not int:
                    raise DataError("Match player IDs are not valid.")
            for player_id in (match["player1_id"], match["player2_id"]):
                stat = match["stats"].get(str(player_id))
                if not isinstance(stat, dict):
                    raise DataError("Match statistics are incomplete.")
                for key in ("shots", "hits", "misses"):
                    if type(stat.get(key)) is not int or stat[key] < 0:
                        raise DataError("Match statistics are not valid.")
        return matches

    def add_match(self, match):
        matches = self.load_matches()
        matches.append(match)
        self.write_list(self.history_file, matches)
