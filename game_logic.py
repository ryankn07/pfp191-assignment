"""Terminal interaction for ship placement and battles."""

from datetime import datetime
import os

from data_manager import DataError
from models import BOARD_SIZE, FLEET, Game, Player
from player_manager import print_players


class GameCanceled(Exception):
    """The player chose to leave a match before it finished."""


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def parse_coordinate(text):
    text = text.strip().upper().replace(" ", "")
    if len(text) < 2 or text[0] not in "ABCDEFGHIJ":
        raise ValueError("Use a coordinate from A1 to J10.")
    try:
        row = int(text[1:]) - 1
    except ValueError:
        raise ValueError("Use a coordinate from A1 to J10.")
    col = "ABCDEFGHIJ".index(text[0])
    if not 0 <= row < BOARD_SIZE:
        raise ValueError("Use a coordinate from A1 to J10.")
    return row, col


def ask_coordinate(message):
    text = input(message).strip()
    if text.upper() == "Q":
        raise GameCanceled()
    return parse_coordinate(text)


def pass_computer(player_name):
    clear_screen()
    print("=" * 40)
    print("            BATTLESHIP")
    print("=" * 40)
    print("Pass the computer to:", player_name)
    input("Press Enter when ready...")
    clear_screen()


def display_battle_boards(player, opponent):
    own_lines = player.board.display_lines(show_ships=True)
    enemy_lines = opponent.board.display_lines(show_ships=False)
    print("YOUR FLEET".ljust(30) + "ENEMY TARGET MAP")
    for own, enemy in zip(own_lines, enemy_lines):
        print(own.ljust(30) + enemy)
    print("S = Ship, X = Hit, O = Miss, ~ = Water, ? = Unknown")


def select_player(manager, message, excluded_id=None):
    while True:
        print_players(manager.all_players())
        text = input(message + " (or Q to cancel): ").strip()
        if text.upper() == "Q":
            raise GameCanceled()
        try:
            player_id = int(text)
        except ValueError:
            print("Please enter a player ID number.")
            continue
        if player_id == excluded_id:
            print("Please choose a different player.")
            continue
        profile = manager.find_player(player_id)
        if profile is not None:
            return Player(profile["id"], profile["name"])
        print("Player ID not found.")


def place_fleet(player):
    for ship_name, length in FLEET:
        while True:
            clear_screen()
            print("FLEET SETUP:", player.name)
            print("\n".join(player.board.display_lines(show_ships=True)))
            print(f"\nPlace {ship_name} ({length} cells)")
            print("H = Horizontal, V = Vertical")
            try:
                row, col = ask_coordinate("Starting coordinate (or Q): ")
                direction = input("Direction (H/V): ").strip().upper()
                if direction == "Q":
                    raise GameCanceled()
                player.board.place_ship(
                    ship_name, length, row, col, direction
                )
                break
            except ValueError as error:
                print("Invalid placement:", error)
                input("Press Enter to try again...")

    clear_screen()
    print("All ships placed for", player.name)
    print("\n".join(player.board.display_lines(show_ships=True)))
    input("Press Enter to hide your fleet...")
    clear_screen()


def play_match(manager, storage):
    if len(manager.all_players()) < 2:
        print("Create at least two player profiles first.")
        return

    try:
        print("\n=== NEW BATTLESHIP MATCH ===")
        player1 = select_player(manager, "Select Player 1")
        player2 = select_player(
            manager, "Select Player 2", excluded_id=player1.player_id
        )
        game = Game(player1, player2)

        for player in game.players:
            pass_computer(player.name)
            place_fleet(player)

        game.start()
        while game.status == "PLAYING":
            player = game.current_player()
            opponent = game.opponent()
            pass_computer(player.name)

            while True:
                print("\nPLAYER TURN:", player.name)
                display_battle_boards(player, opponent)
                try:
                    row, col = ask_coordinate("Attack coordinate (or Q): ")
                    result, ship_name = game.attack(row, col)
                    break
                except ValueError as error:
                    print("Invalid attack:", error)

            if result == "MISS":
                print("\nMISS! No enemy ship here.")
            elif result == "SUNK":
                print("\nSUNK!", ship_name, "has been sunk!")
            else:
                print("\nHIT! Enemy ship found.")

            input("Press Enter to end your turn...")
            clear_screen()

    except GameCanceled:
        clear_screen()
        print("Match canceled. No match result was saved.")
        return

    print("=" * 40)
    print("GAME OVER! WINNER:", game.winner.name)
    print("=" * 40)
    for player in game.players:
        stats = game.stats[player.player_id]
        print(f"{player.name}: {stats['shots']} shots, "
              f"{stats['hits']} hits, {stats['misses']} misses")

    try:
        match_id = len(storage.load_matches()) + 1
        played_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        storage.add_match(game.make_record(match_id, played_at))
        print("Match result saved successfully.")
    except DataError as error:
        print("Could not save the match result:", error)
