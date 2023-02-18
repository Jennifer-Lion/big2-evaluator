# big2-evaluator
An evaluator and ranking system for AI and human players in the card game Big Two

Big Two is a climbing game, which is more popular in Asia countries such as the Philippines and Singapore, that uses a standard deck of 52 cards. It is also known by multiple other names, like Deuces/Big Deuce, Pusoy Dos, and Dai Di. It typically involves 4 players, although there are variations that allows the game to be played by 3 players. This project will only be covering the 4-player version, but extending it to accommodate 3 players could be a valuable extension to this project. The rules that this project is based on can be found here: https://www.pagat.com/climbing/bigtwo.html

This can be adapted to rank any number of AI agents that adhere to the input and output specifications (further explained below). The ranking of multiple AI agents can be obtained automatically following these steps:

## 1.	Prepare AI agents to be evaluated
Name a unique python file for each unique AI agent and place them in the `agents` folder.
In each python file, ensure that there is a function `action(hand, field, control, turn, field_history, enemy1, enemy2, enemy3)`.
  - Parameters:
    - `hand`: A list of strings of card names in the player’s hand.
    - `field`: A list of strings of card names that were most recently played. Disregarded when `control == True`.
    - `control`: A Boolean for if a player can choose how many cards to play. `control=True` when player wins the previous trick.
    - `turn`: An integer for number of turns since the game was played. `turn == 0` denotes the start of the game.
    - `field_history`: A list of strings of all the card that have been played before.
    - `enemy1`: An integer for no. of cards left from the next player
    - `enemy2`: An integer for no. of cards left from opponent opposite of player
    - `enemy3`: An integer for no. of cards left from the previous player
  - Output: A list of strings of card(s) that is/are being played, in a 2-character format: ```NS```, where ```N``` is the number and ```S``` is the suit of the card
  e.g. ` ['8H', '9C', '10D', 'JS', 'QC'] `

## 2.	Create `agents.txt` file
This file should contain all the AI agents' names that you want to evaluate against each other, each separated with a newline. It is important for these names to be the same as the python file names that you have prepared in step number 1.

Note that human players are also supported by adding `human` as an agent. In light of that, naming an AI agent "human" should be avoided.

## 3.	Run the tournament
The tournament can be started by typing the following in the command line:
```bash
python tournament.py n_games style 
```
  - Parameters:
    - ```n_games```: number of games in a match
    - ```style```: "single" or "swiss"
  - Output: A dictionary with agent name as key, and ranking as value. An agent with rank 1 is the best player(s) from the tournament.
  
It should be noted that the ranks will not be unique - there will be duplicates denoting ties - due to the nature of the tournaments.

In the last step, the parameter ```style``` denotes the preferred tournament style – “single” for pairwise single-elimination tournament style, and “swiss” for Swiss-style tournament.
