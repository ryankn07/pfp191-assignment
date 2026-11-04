"""Battleship rules and in-memory match state; no terminal or file access."""

FLEET = {
    'Aircraft Carrier': 5,
    'Battleship': 4,
    'Cruiser': 3,
    'Submarine': 3,
    'Destroyer': 2,
}


def parse_coordinate(text):
    text = text.strip().upper()
    if len(text) < 2 or text[0] not in 'ABCDEFGHIJ':
        raise ValueError('Use a coordinate from A1 to J10.')
    if text[1:] not in [str(number) for number in range(1, 11)]:
        raise ValueError('Use a coordinate from A1 to J10.')
    return int(text[1:]) - 1, ord(text[0]) - ord('A')


class Ship:
    def __init__(self, name, length, positions):
        self.name = name
        self.length = length
        self.positions = set(positions)
        self.hit_positions = set()

    def is_sunk(self):
        return len(self.hit_positions) == self.length


class Board:
    def __init__(self):
        self.fleet = FLEET.copy()
        self.grid = [['~' for _ in range(10)] for _ in range(10)]
        self.ships = []
        self.shots = {}

    def place_ship(self, name, coordinate, direction):
        if name not in self.fleet:
            raise ValueError('Unknown ship.')
        if any(ship.name == name for ship in self.ships):
            raise ValueError('This ship is already placed.')
        direction = direction.strip().upper()
        if direction not in ('H', 'V'):
            raise ValueError('Direction must be H or V.')
        row, column = parse_coordinate(coordinate)
        positions = []
        for offset in range(self.fleet[name]):
            r = row + (offset if direction == 'V' else 0)
            c = column + (offset if direction == 'H' else 0)
            if r >= 10 or c >= 10:
                raise ValueError('Ship extends beyond the board.')
            if self.grid[r][c] != '~':
                raise ValueError('Ships cannot overlap.')
            positions.append((r, c))
        self.ships.append(Ship(name, self.fleet[name], positions))
        for r, c in positions:
            self.grid[r][c] = 'S'
