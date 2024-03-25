

class Game:

    def __init__(self, host: str):
        self.host = host
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
        self.money_on_table -= chips
        self.total_cashouts += owed
    
    def player_paid(self, name: str):
        self.players[name].pay()
    
    def chipcount(self):
        return self.money_on_table
    
    def rebuy(self, name: str, rebuy: float):
        self.players[name].rebuy(rebuy)
        self.money_on_table += rebuy
        self.total_buyins += rebuy

    def balance(self):
        bankererror = (self.total_cashouts)
        return -bankererror
    
    def gamestatus(self):
        statusUpdate = f'-----------------\n'
        statusUpdate += f'|GAME DETAILS|\n'
        statusUpdate += f'-----------------\n'
        statusUpdate += f'Host: {self.host.capitalize()}\n\n'
        statusUpdate += f'Players:\n'
        over = True
        for keyname in self.players:
            player = self.players[keyname]
            if player.cashed:
                statusUpdate += f'{player.name.capitalize()} was in for ${player.in_for()} & cashed for ${player.cashoutchips} \n               (net: {"+" if (player.owed > 0) else ""}${player.owed}) {"Paid!" if player.paid else "Unpaid :("}\n'
            else:
                statusUpdate += f'{player.name.capitalize()} is in for ${player.in_for()}\n'
                over = False
        statusUpdate += f'\nMoney on Table: ${self.money_on_table}\n\n'

        if over:
            statusUpdate += f'Game is over, all players are cashed out\nBanker balance is ${self.money_on_table}'
        return statusUpdate


class Player:

    def __init__(self, name: str, buyin: float):
        self.paid: bool = False
        self.cashed: bool = False
        self.name: str = name
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
        self.cashed = True
        return (round(self.owed, 2))
    
    def pay(self):
        self.paid = True
    
    def __str__(self):
        if self.cashoutchips:
            return f"Player: {self.name} was in for ${self.in_for()} and cashed out for ${self.cashoutchips}, netting {self.owed} dollars, here is their history: {self.history}"

#tests
if __name__ == '__main__':
    game = Game('jonah')
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
