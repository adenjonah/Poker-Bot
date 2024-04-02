from random import choice, randint
from classes import *
from gamebank import *
import re

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def add(game: Game, content) -> str:
    errormsg = '\n'
    if is_float(content[0]):
        buyin = float(content[0])
        for player in content[1:]:
            game.add_player(player, buyin)
        return game.gamestatus()
    for player in content:
        match = re.match(r'([a-zA-Z]+)(\d+)', player)
        if match:
            name = match.group(1)
            buyin = float(match.group(2))
        if game.players.get(name, 0):
            errormsg += f'{name} is already in the game, add chips to them with !rebuy'
            continue
        game.add_player(name, buyin)
    return game.gamestatus() + errormsg

def cashout(game: Game, content) -> str:
    if is_float(content[0]):
        cashoutchips = float(content[0])
        for player in content[1:]:
            game.remove_player(player, cashoutchips)
        return game.gamestatus()
    for player in content:
        match = re.match(r'([a-zA-Z]+)(\d+(\.\d+)?)', player)
        if match:
            name = match.group(1)
            cashoutchips = float(match.group(2))
        game.remove_player(name, cashoutchips)
    return game.gamestatus()

def rebuy(game: Game, content) -> str:
    errors = ''
    if is_float(content[0]):
        rebuy = float(content[0])
        for player in content[1:]:
            game.rebuy(player, rebuy)
        return game.gamestatus()
    for player in content:
        match = re.match(r'([a-zA-Z]+)(\d+)', player)
        if match:
            name = match.group(1)
            rebuy = float(match.group(2))
        if game.players[name].cashed:
            errors += f'Errors:\n{name.capitalize()} already cashed, add them using a new name with !add\n'
            continue
        game.rebuy(name, rebuy)
    return game.gamestatus() + '\n\n' + errors

def paying(game: Game, content) -> str:
    for player in content:
        print(player)
        game.player_paid(player)
    return game.gamestatus()

def get_response(user_input: str, username: str, games: dict=None) -> str:
    tokens = user_input.split(' ')
    command = tokens[0]
    content = tokens[1:]

    if command =='':
        return 'Quiet'
    elif command == 'hello':
        return 'Hey'
    elif command == 'equity':
        evalinput = command[6:]
        hero = []
        villain = []
        board = []
        runs = 10000
        print(content)
        for item in content:
            if item.startswith('hero:'):
                hero = [item.replace('hero:', '')[i:i+2] for i in range(0, len(item.replace('hero:', '')), 2)]
            elif item.startswith('villain:'):
                villain = [item.replace('villain:', '')[i:i+2] for i in range(0, len(item.replace('villain:', '')), 2)]
            elif item.startswith('board:'):
                board = [item.replace('board:', '')[i:i+2] for i in range(0, len(item.replace('board:', '')), 2)]
            elif item.startswith('runs:'):
                runs = min(int(item.replace('runs:', '')), 100000)
        print(f'h: {hero}, v: {villain}, b: {board} r: {runs}')
        return equity(hero, villain, board, runs, print=True)
       
    elif command == 'startgame':
        #create a game under the user profile
        games[username] = Game(username)
        game = games[username]
        return add(game, content)
        #handle game setup
    
    elif command == 'add':
        try:
            game = games[username]
        except KeyError:
            return "User has no game running, start a game with !startgame"
        return add(game, content)
    
    elif command == 'cashout':
        try:
            game = games[username]
        except KeyError:
            return "User has no game running, start a game with !startgame"
        return cashout(game, content)
    
    elif command == 'rebuy':
        try:
            game = games[username]
        except KeyError:
            return "User has no game running, start a game with !startgame"
        return rebuy(game, content)
    
    elif command == 'paid':
        try:
            game = games[username]
        except KeyError:
            return "User has no game running, start a game with !startgame"
        return paying(game, content)

    raise NotImplementedError(f"missing code for command '{command}' with prefix '{command[:7]}'")


if __name__ == '__main__':
    games = {}
    print(get_response('equity heroAsAd villain7sAc runs100', 'adenj'))
    print(get_response('equity heroAsAd villain7sAc boardAh7c7h7d2d runs100', 'adenj'))


    