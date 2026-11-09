"""Start the two-player Battleship terminal application."""

from data_manager import DataError, DataManager
from game_logic import play_match
from player_manager import PlayerManager, player_menu
from reports import report_menu


def main():
    try:
        storage = DataManager()
        manager = PlayerManager(storage)
    except DataError as error:
        print("Cannot open player data:", error)
        print("Please fix the data file before starting the game.")
        return

    while True:
        print("\n" + "=" * 36)
        print("          BATTLESHIP")
        print("=" * 36)
        print("1. Player Management")
        print("2. New Game")
        print("3. History and Reports")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            player_menu(manager)
        elif choice == "2":
            play_match(manager, storage)
        elif choice == "3":
            report_menu(manager, storage)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")
