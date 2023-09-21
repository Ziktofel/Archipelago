
import unittest
from ...sc2wol import Regions

class genntypes_tests(unittest.TestCase):
    def test_grid_sizes_meet_specs(self):
        self.assertEqual((2, 4, 1), Regions.get_grid_dimensions(7))
        self.assertEqual((2, 4, 0), Regions.get_grid_dimensions(8))
        self.assertEqual((3, 3, 0), Regions.get_grid_dimensions(9))
        self.assertEqual((2, 5, 0), Regions.get_grid_dimensions(10))
        self.assertEqual((3, 4, 1), Regions.get_grid_dimensions(11))
        self.assertEqual((3, 4, 0), Regions.get_grid_dimensions(12))
        self.assertEqual((3, 5, 0), Regions.get_grid_dimensions(15))
        self.assertEqual((4, 4, 0), Regions.get_grid_dimensions(16))
        self.assertEqual((4, 6, 0), Regions.get_grid_dimensions(24))
        self.assertEqual((5, 5, 0), Regions.get_grid_dimensions(25))
        self.assertEqual((5, 6, 1), Regions.get_grid_dimensions(29))
        self.assertEqual((5, 7, 2), Regions.get_grid_dimensions(33))

if __name__ == '__main__':
    unittest.main(verbosity=2)
