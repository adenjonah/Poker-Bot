from random import choice, randint
from classes import *

def get_response(user_input: str) -> str:
    usermessage = user_input

    if usermessage =='':
        return 'Quiet'
    elif usermessage == 'hello':
        return 'Hey'
    elif usermessage[:6] == 'equity':
        evalinput = usermessage[6:]
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
    raise NotImplementedError(f"missing code for command '{usermessage}' with prefix '{usermessage[:7]}'")