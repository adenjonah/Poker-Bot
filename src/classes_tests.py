import unittest
from classes import *

class TestDeck(unittest.TestCase):

    def setUp(self):
        self.deck = Deck()

    def test_initial_deck_size(self):
        self.assertEqual(len(self.deck.cards), 52)

    def test_shuffle_preserves_deck_size(self):
        self.deck.shuffle()
        self.assertEqual(len(self.deck.cards), 52)

    def test_draw(self):
        drawn = self.deck.draw(5)
        self.assertEqual(len(drawn), 5)
        self.assertEqual(len(self.deck.cards), 47)

    def test_draw_with_invalid_number_raises_error(self):
        with self.assertRaises(ValueError):
            self.deck.draw(0)

    def test_draw_more_than_deck_size_raises_error(self):
        with self.assertRaises(ValueError):
            self.deck.draw(53)

    def test_reset(self):
        self.deck.draw(5)
        self.deck.reset()
        self.assertEqual(len(self.deck.cards), 52)

    def test_has_cards(self):
        self.assertTrue(self.deck.has_cards(5))
        self.assertFalse(self.deck.has_cards(53))

    def test_takeout(self):
        self.deck.takeout(['as', 'kh'])
        self.assertNotIn('as', self.deck.cards)
        self.assertNotIn('kh', self.deck.cards)
        self.assertEqual(len(self.deck.cards), 50)

    def test_takeout_with_not_enough_cards_raises_error(self):
        self.deck.draw(50)  # Leave 2 cards in deck
        with self.assertRaises(ValueError):
            self.deck.takeout(['as', 'kh', 'qc'])

    def test_shuffle_maintains_deck_size(self):
        original_size = len(self.deck.cards)
        self.deck.shuffle()
        shuffled_size = len(self.deck.cards)
        self.assertEqual(original_size, shuffled_size, "Shuffling should not change deck size")

    def test_reset_restores_original_deck_size(self):
        self.deck.draw(10)  # Draw some cards to change the deck size
        self.deck.reset()  # Reset should restore the deck to its original size
        reset_size = len(self.deck.cards)
        self.assertEqual(reset_size, 52, "Reset should restore the deck to the original size of 52")


class TestPokerFunctions(unittest.TestCase):

    def test_evaluate_straight_flush(self):
        hand = ['6s', '7s', '8s', '9s', 'ts']
        result = evaluate(hand, Deck())
        self.assertEqual(result[0], 9)  # 9 represents a Straight Flush

    def test_winner(self):
        hand1 = evaluate(['6s', '7s', '8s', '9s', 'ts'], Deck())
        hand2 = evaluate(['4s', '5s', '6s', '7s', '8s'], Deck())
        result = winner(hand1, hand2)
        self.assertEqual(result[0], 1)  # Hand1 wins

    def test_equity_basic_scenario(self):
        hero = ['as', 'ks']
        villain = ['qd', 'qh']
        board = ['2s', '3s', '4s']
        result = equity(hero, villain, board, runs=1000)
        # No specific assertion here due to randomness, but you could check result structure
        self.assertEqual(len(result), 3)  # Ensures we get hero win, villain win, and tie percentages

    def test_equity_with_invalid_input(self):
        #Raises wrong error
        hero = ['as', 'ks']
        villain = ['qd', 'qh']
        with self.assertRaises(ValueError):
            equity(hero, villain, board=['2s', '3s', '4s', '4s', '4s', '4s'])  # Invalid board length


if __name__ == '__main__':
    unittest.main()
