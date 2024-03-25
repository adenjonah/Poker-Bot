import unittest
from main import *
from responses import *

class TestEquity(unittest.TestCase):
    def test_hero(self):
        self.assertTrue(80 < equity(['as','ad'])[0] < 90, "Should be about 85")
        self.assertTrue(45 < equity(['qs','7d'])[0] < 55, "Should be about 85")

    def test_twoplayer(self):
        results = equity(['ac','ad'],['7c','2d'])
        self.assertTrue((8 < results[1] < 13) and (85 < results[0] < 92), "Should be about 88")

if __name__ == '__main__':
    unittest.main()