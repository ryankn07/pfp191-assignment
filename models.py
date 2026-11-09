"""The main objects used by the Battleship game."""

FLEET = [
    ("Aircraft Carrier", 5),
    ("Battleship", 4),
    ("Cruiser", 3),
    ("Submarine", 3),
    ("Destroyer", 2),
]

# Kich thuoc ban co mac dinh. Co the doi thanh 40, 100, ... khi can.
BOARD_SIZE = 30


def column_name(index):
    """Convert a zero-based column index to an Excel-style name.

    Examples: 0 -> A, 25 -> Z, 26 -> AA, 27 -> AB.
    """
    if not isinstance(index, int) or index < 0:
        raise ValueError("Column index must be a non-negative integer.")

    name = ""
    while index >= 0:
        index, remainder = divmod(index, 26)
        name = chr(ord("A") + remainder) + name
        index -= 1

    return name


def column_index(name):
    """Convert an Excel-style column name to a zero-based index.

    Examples: A -> 0, Z -> 25, AA -> 26, AB -> 27.
    """
    name = name.strip().upper()
    if not name:
        raise ValueError("Column name cannot be empty.")

    index = 0
    for letter in name:
        if letter < "A" or letter > "Z":
            raise ValueError("Column name must contain letters A-Z only.")
        index = index * 26 + ord(letter) - ord("A") + 1

    return index - 1


class Ship:
    def __init__(self, name, positions):
        self.name = name
        self.positions = positions #vị trí (row,clo)
        self.hits = [] #tàu đã bị địch bắn

    def is_sunk(self): #kiểm tra xem đã chìm chưa
        return len(self.hits) == len(self.positions)


class Board:
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.ships = [] #danh sách tàu đặt lên bàn 
        self.ship_at = {}  # map (row,col)
        self.shots = {}   #Dictionary lưu các phát bắn đã thực hiện trên bàn cờ này theo dạng (row, col): "X" (trúng) hoặc (row, col): "O"

    def is_inside(self, row, col):  #kiểm tra tính hợp lệ của tọa độ
        return 0 <= row < self.size and 0 <= col < self.size

    def place_ship(self, name, length, row, col, direction):
        if direction not in ("H", "V"):
            raise ValueError("Direction must be H or V.")
        if not isinstance(length, int) or length < 1:  
            raise ValueError("Ship length must be a positive integer.")
        if not self.is_inside(row, col):  
            raise ValueError("Starting coordinate is outside the board.")

        positions = []  #danh sasch tọa độ tàu
        for step in range(length):
            new_row = row + step if direction == "V" else row
            new_col = col + step if direction == "H" else col

            if not self.is_inside(new_row, new_col):
                raise ValueError("The ship would extend outside the board.")
            if (new_row, new_col) in self.ship_at:
                raise ValueError("The ship would overlap another ship.")
            positions.append((new_row, new_col))

        ship = Ship(name, positions)
        self.ships.append(ship)
        for position in positions: #đăng kí tạo độ cho từng tàu
            self.ship_at[position] = ship
        return ship

    def receive_attack(self, row, col): #attack
        if not self.is_inside(row, col):
            raise ValueError("Attack coordinate is outside the board.")
        if (row, col) in self.shots:
            raise ValueError("This coordinate has already been attacked.")

        ship = self.ship_at.get((row, col))
        if ship is None:  #ko có tàu thì đánh dấu miss"
            self.shots[(row, col)] = "O" 
            return "MISS", None

        self.shots[(row, col)] = "X"   
        ship.hits.append((row, col))
        if ship.is_sunk():
            return "SUNK", ship.name
        return "HIT", ship.name

    def all_sunk(self):
        if not self.ships:
            return False
        for ship in self.ships:
            if not ship.is_sunk():
                return False
        return True

    def display_lines(self, show_ships):
        """Return the board as text without revealing hidden enemy ships."""
        # Generate column labels automatically: A, B, ..., Z, AA, AB, ...
        columns = [column_name(col) for col in range(self.size)]

        # Keep column and row labels aligned for boards of different sizes.
        column_width = max(2, max(len(name) for name in columns))
        row_width = len(str(self.size))
        header = " " * (row_width + 1) + " ".join(
            f"{name:>{column_width}}" for name in columns
        )
        lines = [header]

        for row in range(self.size):
            cells = []
            for col in range(self.size):
                coordinate = (row, col)
                if coordinate in self.shots:
                    mark = self.shots[coordinate]
                elif show_ships and coordinate in self.ship_at:
                    mark = "S"   #ô của mình
                elif show_ships:
                    mark = "~"    # ô trống
                else:
                    mark = "?"
                cells.append(mark)

            row_label = f"{row + 1:>{row_width}}"
            cell_text = " ".join(
                f"{mark:>{column_width}}" for mark in cells
            )
            lines.append(row_label + " " + cell_text)

        return lines


class Player:
    def __init__(self, player_id, name, board_size=BOARD_SIZE):
        self.player_id = player_id
        self.name = name
        self.board = Board(board_size)


class MatchRecord:  #lưu trữ kết quả
    def __init__(self, match_id, player1, player2, winner, stats, played_at):
        self.match_id = match_id
        self.player1 = player1
        self.player2 = player2
        self.winner = winner
        self.stats = stats
        self.played_at = played_at

    def to_dict(self):
        return {
            "match_id": self.match_id,
            "played_at": self.played_at,
            "player1_id": self.player1.player_id,
            "player1_name": self.player1.name,
            "player2_id": self.player2.player_id,
            "player2_name": self.player2.name,
            "winner_id": self.winner.player_id,
            "winner_name": self.winner.name,
            "stats": self.stats,
        }


class Game: #quản lí luồng game
    def __init__(self, player1, player2):
        if player1.player_id == player2.player_id:
            raise ValueError("A player cannot play against themselves.")
        self.players = [player1, player2]
        self.current_turn = 0  #danh sách lượt chơi
        self.status = "SETUP"
        self.winner = None
        self.stats = {
            player1.player_id: {"shots": 0, "hits": 0, "misses": 0},
            player2.player_id: {"shots": 0, "hits": 0, "misses": 0},
        }

    def current_player(self):
        return self.players[self.current_turn]

    def opponent(self):
        return self.players[1 - self.current_turn]

    def start(self):
        for player in self.players:
            actual = [(ship.name, len(ship.positions))
                      for ship in player.board.ships]
            if actual != FLEET:
                raise ValueError("Both players must place the complete fleet.")
        self.status = "PLAYING"

    def attack(self, row, col):  # cơ chế tấn công
        if self.status != "PLAYING":
            raise ValueError("There is no active match.")

        attacker = self.current_player()
        defender = self.opponent()
        result, ship_name = defender.board.receive_attack(row, col)

        record = self.stats[attacker.player_id]
        record["shots"] += 1
        if result == "MISS":
            record["misses"] += 1
        else:
            record["hits"] += 1

        if defender.board.all_sunk():  #kiểm tra hạm đội chìm chưa
            self.status = "FINISHED"
            self.winner = attacker
        else:
            self.current_turn = 1 - self.current_turn

        return result, ship_name

    def make_record(self, match_id, played_at):  #ghi kết quả
        if self.status != "FINISHED":
            raise ValueError("Cannot record an unfinished match.")
        player1, player2 = self.players
        stats_for_file = {}
        for player_id, counts in self.stats.items():
            stats_for_file[str(player_id)] = counts.copy()
        record = MatchRecord(
            match_id, player1, player2, self.winner,
            stats_for_file, played_at
        )
        return record.to_dict()
