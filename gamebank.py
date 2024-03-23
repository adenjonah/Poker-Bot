

class Game:

    def __init__(self):
        self.players = {}
        self.money_on_table = 0
        self.total_buyins = 0
        self.total_cashouts = 0
    
    def add_player(self, name: str, buyin: float):
        self.players[name] = Player(name, buyin)
        self.money_on_table += buyin
        self.total_buyins += buyin
    
    def remove_player(self, name: str, chips: float):
        owed = self.players[name].cashout(chips)
        if owed > 0:
            self.money_on_table -= owed
        self.total_cashouts += owed
        del(self.players[name])
    
    def chipcount(self):
        return self.money_on_table
    
    def rebuy(self, name: str, rebuy: float):
        self.players[name].rebuy(rebuy)
        self.total_buyins += rebuy

    def balance(self):
        bankererror = (self.total_cashouts)
        return -bankererror


class Player:

    def __init__(self, name: str, buyin: float):
        self.name = name
        self.buyin: float = buyin
        self.rebuys: float = 0
        self.cashoutchips: float = None
        self.owed: float = None
        self.history = [buyin]
    
    def in_for(self):
        return self.buyin + self.rebuys
    
    def rebuy(self, rebuy: float):
        round(rebuy, 2)
        if self.rebuys:
            self.rebuys += rebuy
        else:
            self.rebuys = rebuy
        
        self.history.append(rebuy)
    
    def cashout(self, chips: float):
        self.cashoutchips = chips
        self.owed = round(self.cashoutchips - self.in_for(), 2)
        self.history.append(-chips)
        return (round(self.owed, 2))
    
    def __str__(self):
        if self.cashoutchips:
            return f"Player: {self.name} was in for ${self.in_for()} and cashed out for ${self.cashoutchips}, netting {self.owed} dollars, here is their history: {self.history}"

#tests
if __name__ == '__main__':
    game = Game()
    print(game.chipcount())
    game.add_player('jonah', 20)
    game.add_player('josh', 30)
    print(game.chipcount())
    game.remove_player('josh', 26)
    print(game.chipcount())
    game.add_player('bob', 50)
    game.rebuy('jonah', 20)
    print(game.chipcount())
    game.remove_player('bob', 70)
    game.remove_player('jonah', 20)
    print(game.balance())
    print(game.total_buyins)
