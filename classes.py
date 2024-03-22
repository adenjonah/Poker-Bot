import random
import time
from itertools import combinations

suits = ['c', 's', 'h', 'd']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
showdown_ranks = {1: "High Card", 2 : "One Pair", 3 : "Two Pair", 4 : "Three of a Kind", 5 : "Straight", 6: "Flush", 7 : "Full House", 8 : "Quads", 9 : "Straight Flush"}

class Deck:
    cards = []
    used = []

    def __init__(self):
        self.cards.clear()
        self.used.clear()
        for suit in suits:
            for rank in ranks:
                card = rank + suit
                self.cards.append(card)

    def __str__(self):
        return f"{self.cards}"
    
    def shuffle(self, shuffles=1):
        self.cards += self.used
        self.used = []
        for i in range(shuffles):
            random.shuffle(self.cards)

    def count(self):
        return len(self.cards)
    
    def hascards(self, num=1):
        return (num <= (len(self.cards) - len(self.used)))
    
    def draw(self, num=1):
        if(num <= 0):
            raise ValueError("Must draw at least 1 card")
        if(not self.hascards(num)):
            raise ValueError("Not enough cards in deck")

        drawn = []
        for i in range(num):
            card = self.cards.pop()
            drawn.append(card)
            self.used.append(card)
        return drawn
    
    def reset(self):
        self.__init__()
    
    def takeout(self, removals=[]):
        if(not self.hascards(len(removals))):
           raise ValueError("Not enough cards in deck")
        if(len(removals) != 0):
            for card in removals:
                self.cards.remove(card)

def evaluate(cards, deck):
    card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    rev_values = {value: key for key, value in card_values.items()}
    rev_values[1] = 'A'
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

def equity(hero=[], villian=[], board=[], runs=10000, print=False):
    result = 0
    herowins = 0
    villianwins = 0
    
    ties = 0
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

            while len(herohand) < 2:
                herohand.append(deck.draw()[0])
            while len(vilhand) < 2:
                vilhand.append(deck.draw()[0])
            while len(boardinstance) < 5:
                boardinstance.append(deck.draw()[0])

            herohand = list(combinations(herohand + boardinstance, 5))

            vilhand = list(combinations(vilhand + boardinstance, 5))

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
    
    return (f"\n\
        Results:\n\
        Board: {' '.join(board) if board != [] else '?????'}\n\
        Hero ({' '.join(hero) if hero != [] else '??'}):    {100 * (herowins / runs):.1f}%\n\
        Villain ({' '.join(villian) if villian != [] else '??'}): {100 * (villianwins / runs):.1f}%\n\
        Ties:       {100 *(ties / runs):.1f}%")