# Poker-Bot README

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Basic Commands](#basic-commands)
- [Installation for Development](#installation-for-development)
- [Codebase Structure](#codebase-structure)
- [Contributing](#contributing)
  - [Future Development Prospects](#future-development-prospects)
- [Contact](#contact)  

## Overview
Poker-Bot is a Discord bot designed to facilitate poker games, providing utilities like equity calculation, bank management, and interactive gameplay. It is built for poker enthusiasts and developers interested in poker-related bot development.

## Features
- Equity Calculation: Computes win, loss, and tie probabilities for given hands and board states using Monte Carlo simulation.
- Banker Helper: Manages player buy-ins, cashouts, and rebuys, maintaining the game's financials.

## Getting Started
To use the Poker-Bot in your Discord server, invite the bot to your server and ensure it has the necessary permissions to read and send messages.

### Basic Commands
- `!equity`: Calculates the equity for specified hands and board.
  - Arguments: `hero:RSRS villain:RSRS board:RSRSRSRSRS runs:INT`
    - `hero`: Hero's hand, specified as `RSRS` where `R` is the rank (2-9,T,J,Q,K,A) and `S` is the suit (s,c,h,d).
    - `villain`: Villain's hand, in the same format as the hero's hand.
    - `board`: The board cards, specified as `RSRSRSRSRS` for five cards.
    - `runs`: (Optional) Number of simulations to run for equity calculation, default is 10,000.
#### For the following commands, if the numerical vaule is the same for all players the command can be in the format   
#### ```!command VALUE PLAYER PLAYER PLAYER```
- `!startgame`: Initiates a new poker game session.
  - Arguments: `PLAYERbuyin`
    - `PLAYER`: Name of the player to add.
    - `buyin`: The amount of money the player is buying into the game with.
- `!add`: Adds players to the game with their buy-in.
  - Arguments: `PLAYERbuyin`
    - `PLAYER`: Name of the player to add.
    - `buyin`: The amount of money the player is buying into the game with.
- `!cashout`: Records players' cashouts.
  - Arguments: `PLAYERamount`
    - `PLAYER`: Name of the player to cash out.
    - `amount`: The amount of money the player is cashing out.
- `!rebuy`: Manages rebuys for players in the game.
  - Arguments: `PLAYERamount`
    - `PLAYER`: Name of the player rebuying.
    - `amount`: The rebuy amount for the player.
- `!paid`: Marks a player's debts as settled.
  - Arguments: `player`
    - `player`: Name of the player who has paid their debts.

## Installation for Development
1. Clone the repository to your local machine.
2. Ensure Python 3.8+ is installed.
3. Install required dependencies using `pip install -r requirements.txt`.
4. Create a `.env` file with your Discord bot token as `DISCORD_TOKEN`.

## Codebase Structure
- `main.py`: Entry point for the bot, handling Discord events and commands.
- `classes.py`: Contains core poker-related classes and logic, including deck handling and hand evaluation.
- `gamebank.py`: Manages game states, including players, buy-ins, and cashouts.
- `responses.py`: Processes commands and generates responses for user interactions.
- `equity_tests.py`: Contains unit tests for the equity calculation functionality.

## Contributing
I plan on optimizing the current features and adding new ones. If you'd like to contribute, please fork the repository and submit a pull request with your changes.
### Future Development Prospects
- Optimizing hand evaluation by implementing CactusKev's evaluation process
- Adding equity computation for PLO, DBBPPLO, Lowball, Red River
- User bankroll tracker using a database
- Basic hand history analyzer that takes a hand history and returns a classification (suckout, bad beat, cooler, nit fold)
- Heads-Up NLH Solver using CFRM
## Contact
For support or inquiries, please open an issue on the GitHub repository or reachout to me via email.
