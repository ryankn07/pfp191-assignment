import unittest

from models import Board


def place_fleet(board):
    for name, coordinate in zip(board.fleet, ['A1', 'A2', 'A3', 'A4', 'A5']):
        board.place_ship(name, coordinate, 'H')


class BoardTests(unittest.TestCase):
    def test_placement_boundary_overlap_and_adjacent(self):
        board = Board()
        board.place_ship('Aircraft Carrier', 'F1', 'H')
        with self.assertRaises(ValueError):
            board.place_ship('Battleship', 'H2', 'H')
        with self.assertRaises(ValueError):
            board.place_ship('Battleship', 'F1', 'V')
        self.assertEqual(len(board.ships), 1)
        board.place_ship('Battleship', 'F2', 'H')
        self.assertEqual(len(board.ships), 2)


if __name__ == '__main__':
    unittest.main()
