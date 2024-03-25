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
        game.add_player(name, buyin)
    return game.gamestatus()

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

def get_response(user_input: str, username: str, games: dict) -> str:
    tokens = user_input.split(' ')
    command = tokens[0]
    content = tokens[1:]

    if command =='':
        return 'Quiet'
    elif command == 'hello':
        return 'Hey'
    elif command == 'equity':
        #logic broken
        evalinput = command[6:]
        hero = []
        villian = []
        board = []
        runs = 10000
        h = 'hero:'
        v = 'villain:'
        b = 'board:'
        r = 'runs'
        #The current bug is that if you have less than 2 hole cards inputted or less than 5 board cards, the next chars 
        #are passed in. finding a better way to delimit will solve this problem.
        if h in evalinput:
            hh = evalinput[evalinput.find(h) + len(h) : evalinput.find(h) + len(h) + 4]
            hero = [hh[i].upper() + hh[i+1:i+2] for i in range(0, len(hh), 2)]
        if v in evalinput:
            vh = evalinput[evalinput.find(v) + len(v) : evalinput.find(v) + len(v) + 4]
            villian = [vh[i].upper() + vh[i+1:i+2] for i in range(0, len(vh), 2)]
        if b in evalinput:
            bi = evalinput[evalinput.find(b) + len(b) : evalinput.find(b) + len(b) + 10]
            board = [bi[i].upper() + bi[i+1:i+2] for i in range(0, len(bi), 2)]
        if r in evalinput:
            runs = evalinput[evalinput.find(r) + len(r) : evalinput.find(r) + len(r) + 2]#This wont work
        print(f'Hero hand: {hero}')
        return equity(hero, villian, board, runs, print=True)
    
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

games = {}
if __name__ == '__main__':
    print(get_response('startgame brian30 maokong50', 'adenj', games))
    print(get_response('add jonah50 josh20 harrison80', 'adenj', games))
    print(get_response('startgame brian30 maokong50', 'oliver', games))
    print(get_response('add 50 rachel naomi', 'adenj', games))
    print(get_response('add 50 jonah josh harrison', 'oliver', games))

    print(get_response('cashout brian0 maokong80 jonah26.7', 'oliver', games))

    print(get_response('startgame bob50 ed50', 'josh', games))
    print(get_response('cashout bob25', 'josh', games))
    print(get_response('rebuy bob25', 'josh', games))
    print(get_response('paid brian', 'oliver', games))

'''
!startgame 20 jonah harrison andrew

!add eric40 brian50 sean20

!rebuy andrew300

!rebuy 50 jonah harrison

!cashout sean150 eric0

!paid sean eric

!cashout jonah90 harrison150 andrew80 brian100
'''

    