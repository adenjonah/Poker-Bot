import random
import time
from itertools import combinations

suits = ['c', 's', 'h', 'd']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 't', 'j', 'q', 'k', 'a']
showdown_ranks = {1: "High Card", 2 : "One Pair", 3 : "Two Pair", 4 : "Three of a Kind", 5 : "Straight", 6: "Flush", 7 : "Full House", 8 : "Quads", 9 : "Straight Flush"}

class Deck:
    def __init__(self):
        # Initialize the deck of cards; this creates a new, full deck ready for use.
        # The 'cards' list contains all cards in the deck, and 'used' contains cards that have been drawn.
        self.cards = [rank + suit for suit in suits for rank in ranks]
        self.used = []

    def __str__(self):
        # Provide a string representation of the current state of the deck, showing remaining and used cards.
        return f"Cards in deck: {self.cards}\nUsed cards: {self.used}"
    
    def shuffle(self, shuffles=1):
        # Shuffle the deck, combining used and remaining cards, then randomizing the order.
        # The 'shuffles' parameter indicates how many times the deck should be shuffled.
        self.cards += self.used
        self.used.clear()
        for i in range(shuffles):
            random.shuffle(self.cards)

    def count(self):
        # Return the total number of cards in the deck, including both used and remaining cards.
        return len(self.cards) + len(self.used)
    
    def has_cards(self, num=1):
        # Check if there are enough remaining cards in the deck for a given number 'num'.
        return num <= (len(self.cards) - len(self.used))
    
    def draw(self, num=1):
        # Draw 'num' number of cards from the deck, removing them from the remaining cards,
        # and adding them to the used cards list. Raises an error if there aren’t enough cards to draw.
        if num <= 0:
            raise ValueError("Must draw at least 1 card")
        if not self.has_cards(num):
            raise ValueError("Not enough cards in deck")
        drawn = [self.cards.pop() for _ in range(num)]
        self.used.extend(drawn)
        return drawn
    
    def reset(self):
        # Reset the deck to its original state, with all cards being available to draw again.
        self.__init__()
    
    def takeout(self, removals=None):
        # Remove specific cards from the deck, typically used to simulate specific scenarios or hands.
        # 'removals' is a list of cards to be removed from the deck.
        if removals is None:
            removals = []
        if not self.has_cards(len(removals)):
            raise ValueError("Not enough cards in deck")
        for card in removals:
            self.cards.remove(card)

def evaluate(cards, deck):
    card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 't': 10, 'j': 11, 'q': 12, 'k': 13, 'a': 14}
    
    flush = len({card[-1] for card in cards}) == 1
    straight = False
    ranks = {card_values[card[:-1]] for card in cards}
    sortedcards = sorted([card_values[card[:-1]] for card in cards])
    rankscount = {}
    for rank in sortedcards:
        rankscount[rank] = rankscount.get(rank, 0) + 1
    if len(ranks) == 5:
        if sortedcards == [2, 3, 4, 5, 14]:
            straight = True
            sortedcards = [1, 2, 3, 4, 5]
        elif sortedcards[-1] - sortedcards[0] == 4:
            straight = True
        elif not flush:
            return [1] + sortedcards[::-1]
    if flush and straight:
        return [9, sortedcards[-1]]
    if flush:
        return [6, sortedcards[-1]]
    if straight:
        return [5, sortedcards[-1]]
    if len(ranks) == 4:
        pair = next(key for key, value in rankscount.items() if value == 2)
        kickers = [x for x in sortedcards if x != pair]
        return [2, pair] + kickers[::-1]
    if len(ranks) == 3:
        trips = next((key for key, value in rankscount.items() if value == 3), False)
        if trips:
            kickers = [x for x in sortedcards if x != trips]
            return [4, trips] + kickers[::-1]
        else:
            twopair = [key for key, value in rankscount.items() if value == 2]
            kickers = [x for x in sortedcards if ((x != twopair[0]) and (x != twopair[1]))]
            return [3, max(twopair), min(twopair)] + kickers[::-1]
    if len(ranks) == 2:
        quads = next((key for key, value in rankscount.items() if value == 4), False)
        if quads:
            return [8, quads, next(key for key, value in rankscount.items() if value == 1)]
        else:
            return [7, next(key for key, value in rankscount.items() if value == 3), next(key for key, value in rankscount.items() if value == 2)]
    raise ValueError(f'Cards in the hand are not possible: {cards}')

def winner(hand1, hand2):
    #Compares two hand rankings, starting with the hand rank and then kickers if they are tied
    answer = [0,0]
    for elem1, elem2 in zip(hand1, hand2):
        if elem1 > elem2:
            answer = [1, hand1]
            return answer
        elif elem1 < elem2:
            answer = [0, hand2]
            return answer
    answer = [-1, hand1]
    return answer

def format_card(card):
    #Makes face cards, aces, and 10s uppercase before returning
    face_cards = {'t': 'T', 'j': 'J', 'q': 'Q', 'k': 'K', 'a': 'A'}
    return face_cards.get(card[0], card[0].upper()) + card[1]

def get_formatted_cards(cards):
    #Makes a string of formatted cards
    return ' '.join([format_card(card) for card in cards])


def equity(hero=[], villian=[], board=[], runs=1000, print=False):
    #Calculates and returns probability of wins and ties for 2 player NLH
    result = 0
    herowins = 0
    villianwins = 0
    ties = 0

    #Initializes a deck and removes inputted cards from the deck
    deck = Deck()
    deck.takeout(hero + villian + board)
    try:
        for run in range(runs):
            herohand = []
            vilhand = []
            heromax = []
            vilmax = []

            deck.shuffle()

            herohand = hero.copy()
            vilhand = villian.copy()
            boardinstance = board.copy()

            #Fills hands until each player has 2 cards and the board has 5 cards
            while len(herohand) < 2:
                herohand.append(deck.draw()[0])
            while len(vilhand) < 2:
                vilhand.append(deck.draw()[0])
            while len(boardinstance) < 5:
                boardinstance.append(deck.draw()[0])

            #Created a list of all combinations of 5 cards from the 7 cards inputted
            herohand = list(combinations(herohand + boardinstance, 5))
            vilhand = list(combinations(vilhand + boardinstance, 5))

            #Finds the hero and villains best hands
            heromax = [0, 0]
            for cards in herohand:
                heromax = winner(heromax, evaluate(cards, deck))[1]
            vilmax = [0, 0]
            for cards in vilhand:
                vilmax = winner(vilmax, evaluate(cards, deck))[1]
            
            result = winner(heromax, vilmax)[0]

            if result == 1:
                herowins += 1
            elif result == 0:
                villianwins += 1
            else:
                ties += 1
            herohand.clear()
            vilhand.clear()
            boardinstance.clear()
    except ValueError as e:
        return f"Exception raised: {e}. Deck content: {deck}"
    deck.reset()
    if not print:
        return [round(100*(herowins/runs), 2), round(100*(villianwins/runs), 2), round(100*(ties/runs), 2)]
    
    return (
    f"Results:\n"
    f"Board: {get_formatted_cards(board) if board else '?????'}\n"
    f"Hero ({get_formatted_cards(hero) if hero else '??'}): "
    f"{100 * (herowins / runs):6.1f}%\n"
    f"Villain ({get_formatted_cards(villian) if villian else '??'}): "
    f"{100 * (villianwins / runs):6.1f}%\n"
    f"Ties: {100 * (ties / runs):6.1f}%"
    )


if __name__ == '__main__':
    print(equity(['as','kc'], print=True))