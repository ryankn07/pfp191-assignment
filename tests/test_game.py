import unittest

from models import Board


class BoardTests(unittest.TestCase):
    def test_placement_boundary_overlap_and_adjacent(self):
        board = Board()
        board.place_ship('Aircraft Carrier', 5, 0, 5, 'H')
        with self.assertRaises(ValueError):
            board.place_ship('Battleship', 4, 1, 7, 'H')
        with self.assertRaises(ValueError):
            board.place_ship('Battleship', 4, 0, 5, 'V')
        self.assertEqual(len(board.ships), 1)
        board.place_ship('Battleship', 4, 1, 5, 'H')
        self.assertEqual(len(board.ships), 2)

    def test_ship_sinks_after_all_its_cells_are_hit(self):
        board = Board()
        board.place_ship('Destroyer', 2, 0, 0, 'H')

        self.assertEqual(board.receive_attack(0, 0), ('HIT', 'Destroyer'))
        self.assertFalse(board.all_sunk())
        self.assertEqual(board.receive_attack(0, 1), ('SUNK', 'Destroyer'))
        self.assertTrue(board.all_sunk())


if __name__ == '__main__':
    unittest.main()
