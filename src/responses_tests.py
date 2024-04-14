import unittest
from responses import *

class TestResponses(unittest.TestCase):

    def test_initial_deck_size(self):
        games: dict[str, Game] = {}
        self.assertEqual(get_response('startgame 20 jonah bob', 'adenj', games), f"-----------------\n|GAME DETAILS|\n-----------------\nHost: Adenj\n\nPlayers:\nJonah is in for 20.0\nBob is in for 20.0\n\nMoney on Table: 40.0\n\n")
        self.assertEqual(get_response('cashout jonah5', 'adenj', games), f"-----------------\n|GAME DETAILS|\n-----------------\nHost: Adenj\n\nPlayers:\nJonah was in for 20.0 & cashed for 5.0 \n               (net: -15.0) Unpaid :(\nBob is in for 20.0\n\nMoney on Table: 35.0\n\n")
        self.assertEqual(get_response('cashout jonah5', 'adenj', games), f"-----------------\n|GAME DETAILS|\n-----------------\nHost: Adenj\n\nPlayers:\nJonah was in for 20.0 & cashed for 5.0 \n               (net: -15.0) Unpaid :(\nBob is in for 20.0\n\nMoney on Table: 35.0\n\njonah already cashed\n")
        
if __name__ == '__main__':

    unittest.main()
