BOARD_SIZE=10

class Ship:
    def __init__(self,name,length,positions):
        self.name=name
        delf.length=length
        self.positons=positions
        self.hit=[]
    
    def is_sunk(self):
        return len(self.hit)==len(self.positions)


class Board:
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.ships = []
        self.ship_at = {}
        self.shots = {}

    def is_inside(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def place_ship(self, name, length, row, col, direction):
        if direction not in ("H", "V"):
            raise ValueError("Direction must be H or V.")
        if not isinstance(length, int) or length < 1:
            raise ValueError("Ship length must be a positive integer.")
        if not self.is_inside(row, col):
            raise ValueError("Starting coordinate is outside the board.")

        positions = []
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
        for position in positions:
            self.ship_at[position] = ship
        return ship

    def receive_attack(self, row, col):
        if not self.is_inside(row, col):
            raise ValueError("Attack coordinate is outside the board.")
        if (row, col) in self.shots:
            raise ValueError("This coordinate has already been attacked.")

        ship = self.ship_at.get((row, col))
        if ship is None:
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
        column_names = " ".join("ABCDEFGHIJ"[:self.size])
        lines = ["   " + column_names]

        for row in range(self.size):
            cells = []
            for col in range(self.size):
                coordinate = (row, col)
                if coordinate in self.shots:
                    mark = self.shots[coordinate]
                elif show_ships and coordinate in self.ship_at:
                    mark = "S"
                elif show_ships:
                    mark = "~"
                else:
                    mark = "?"
                cells.append(mark)
            lines.append(f"{row + 1:>2} " + " ".join(cells))
        return lines
        
class Player:
    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name