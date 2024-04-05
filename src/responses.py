from random import choice, randint
from typing import Any
from equity import *
from gamebank import *
import re



def get_response(user_input: str, username: str, games: dict[Any, Any]) -> str:
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
        for item in content:
            if item.startswith('hero:'):
                hero = [item.replace('hero:', '')[i:i+2] for i in range(0, len(item.replace('hero:', '')), 2)]
            elif item.startswith('villain:'):
                villain = [item.replace('villain:', '')[i:i+2] for i in range(0, len(item.replace('villain:', '')), 2)]
            elif item.startswith('board:'):
                board = [item.replace('board:', '')[i:i+2] for i in range(0, len(item.replace('board:', '')), 2)]
            elif item.startswith('runs:'):
                runs = min(int(item.replace('runs:', '')), 100000)
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
    games: dict[str, Game] = {}
    print(get_response('equity heroAsAd villain7sAc runs100', 'adenj', games))
    print(get_response('equity heroAsAd villain7sAc boardAh7c7h7d2d runs100', 'adenj', games))


    