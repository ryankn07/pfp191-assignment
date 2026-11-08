"""Manage player profiles (create, list, search, edit and delete)."""

from data_manager import DataError


class PlayerManager:
    def __init__(self, storage):
        self.storage = storage
        self.players = storage.load_players()

    def all_players(self):
        return self.players[:]

    def find_player(self, player_id):
        for player in self.players:
            if player["id"] == player_id:
                return player
        return None

    def validate_name(self, name, ignore_id=None):
        name = name.strip()
        if not name or len(name) > 30:
            raise ValueError("Name must contain 1 to 30 characters.")
        for player in self.players:
            if player["name"].lower() == name.lower():
                if player["id"] != ignore_id:
                    raise ValueError("This player name already exists.")
        return name

    def add_player(self, name):
        name = self.validate_name(name)
        new_id = max([player["id"] for player in self.players], default=0) + 1
        new_player = {"id": new_id, "name": name}
        updated = self.players + [new_player]
        self.storage.save_players(updated)
        self.players = updated
        return new_player

    def edit_player(self, player_id, new_name):
        if self.find_player(player_id) is None:
            raise ValueError("Player not found.")
        name = self.validate_name(new_name, ignore_id=player_id)
        updated = []
        for player in self.players:
            if player["id"] == player_id:
                updated.append({"id": player_id, "name": name})
            else:
                updated.append(player.copy())
        self.storage.save_players(updated)
        self.players = updated

    def delete_player(self, player_id):
        if self.find_player(player_id) is None:
            raise ValueError("Player not found.")

        for match in self.storage.load_matches():
            if (match.get("player1_id") == player_id
                    or match.get("player2_id") == player_id):
                raise ValueError("Cannot delete a player in match history.")

        updated = [p for p in self.players if p["id"] != player_id]
        self.storage.save_players(updated)
        self.players = updated

    def search_players(self, keyword):
        return [p for p in self.players
                if keyword.strip().lower() in p["name"].lower()]


def print_players(players):
    if not players:
        print("No players found.")
    else:
        print("ID   NAME")
        print("------------------------------")
        for player in players:
            print(f"{player['id']:<4} {player['name']}")


def ask_player_id():
    try:
        return int(input("Player ID: ").strip())
    except ValueError:
        raise ValueError("Player ID must be a number.")


def player_menu(manager):
    while True:
        print("\n=== PLAYER MANAGEMENT ===")
        print("1. View players")
        print("2. Add player")
        print("3. Edit player")
        print("4. Delete player")
        print("5. Search players")
        print("0. Back")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                print_players(manager.all_players())
            elif choice == "2":
                name = input("New player name: ")
                player = manager.add_player(name)
                print("Added player with ID", player["id"])
            elif choice == "3":
                player_id = ask_player_id()
                name = input("New name: ")
                manager.edit_player(player_id, name)
                print("Player updated.")
            elif choice == "4":
                player_id = ask_player_id()
                confirm = input("Delete this player? (Y/N): ").upper()
                if confirm == "Y":
                    manager.delete_player(player_id)
                    print("Player deleted.")
            elif choice == "5":
                keyword = input("Search name: ")
                print_players(manager.search_players(keyword))
            elif choice == "0":
                return
            else:
                print("Invalid menu option.")
        except (ValueError, DataError) as error:
            print("Error:", error)
