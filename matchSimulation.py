from logic import Logic
from card import Card

import importlib

def matchSimulation(n_games, agent1, agent2, agent3, agent4):
    # Initialization of AI
    player1 = importlib.import_module('agents.'+agent1)
    player2 = importlib.import_module('agents.'+agent2)
    player3 = importlib.import_module('agents.'+agent3)
    player4 = importlib.import_module('agents.'+agent4)

    # Initialization of table
    logic = Logic()
    card = Card()

    # Initialization of simulation settings
    scoresTotal = [0, 0, 0, 0]
    winsTotal = [0, 0, 0, 0]
    disqualifiedTournament = [False, False, False, False]
    disqualifiedCounter = [0, 0, 0, 0]

    for sess in range(n_games):
        
        # Shuffle and deal cards
        shuffled = card.shuffleDeck()
        player1Hand = card.sortingCards(shuffled[ 0:13])
        player2Hand = card.sortingCards(shuffled[13:26])
        player3Hand = card.sortingCards(shuffled[26:39])
        player4Hand = card.sortingCards(shuffled[39:52])

        # Initialize variables before every game starts
        myTurn = shuffled.index('3D') // 13
        gameOver = False
        control = True
        passes = 0 # number of passes before this guy's turn
        field = [] # last card(s) played
        field_history = [] # cards that have been played
        turn = 0
        scoresRound = [0, 0, 0, 0]
        disqualified = disqualifiedTournament
        


        # Game starts
        while not gameOver:
            # Choosing player
            if myTurn == 0:
                handInPlay = player1Hand
                player = player1
            elif myTurn == 1:
                handInPlay = player2Hand
                player = player2
            elif myTurn == 2:
                handInPlay = player3Hand
                player = player3
            else:
                handInPlay = player4Hand
                player = player4

            # Take note of number of cards left
            cardsLeft = [len(player1Hand), len(player2Hand), len(player3Hand), len(player4Hand)]

            # Combination played
            played = player.action(handInPlay, field, control, turn, field_history, cardsLeft[(myTurn+1) % 4], cardsLeft[(myTurn+2) % 4], cardsLeft[(myTurn+3) % 4])

            # Valid combinations of cards
            valid_moves = logic.possibleMoves(handInPlay, field, control, turn)

            try:
                played = card.sortingCards(played)

                if played in valid_moves: # valid move
                    if played == []:
                        passes += 1
                    else:
                        field = played
                        field_history += field
                        field_history = card.sortingCards(field_history)
                        passes = 0

                    # Update hand after throwing cards
                    if myTurn == 0:
                        player1Hand = [card for card in handInPlay if card not in played]
                        if player1Hand == []:
                            gameOver = True
                    elif myTurn == 1:
                        player2Hand = [card for card in handInPlay if card not in played]
                        if player2Hand == []:
                            gameOver = True
                    elif myTurn == 2:
                        player3Hand = [card for card in handInPlay if card not in played]
                        if player3Hand == []:
                            gameOver = True
                    else:
                        player4Hand = [card for card in handInPlay if card not in played]
                        if player4Hand == []:
                            gameOver = True

                else: # invalid move
                    disqualified[myTurn] = True
                    print(str([agent1, agent2, agent3, agent4][myTurn]) + " disqualified.")
                    if control: # if disqualified player was supposed to lead the trick
                        passes = 3 # pass the control to the next player

            except: # disqualify player if wrong format for 3 games
                disqualifiedCounter[myTurn] += 1 # add 1 strike for every game that the agent throws an incompatible format
                if disqualifiedCounter[myTurn] >= 3:
                    disqualified[myTurn] = True
                    disqualifiedTournament[myTurn] = True
                    print(str([agent1, agent2, agent3, agent4][myTurn]) + " has been disqualified from this match for throwing cards of the format.")
                    if control: # if disqualified player was supposed to lead the trick
                        passes = 3 # pass the control to the next player


            if gameOver:
                break

                        
            # if next player has only 1 card left
            if cardsLeft[(myTurn+1) % 4] == 1: 
                if played == [] and valid_moves != [[]]: # pass
                    lastCardDanger = True
                elif len(played) == 1: # singles
                    # if player deliberately chooses singles when there are other possible combinations
                    if control and len(valid_moves[-1]) > 1: 
                        lastCardDanger = True
                    # if player does not play his highest card
                    elif card.getCardValues(played)[0] != max(card.getCardValues(handInPlay)):
                        lastCardDanger = True
                    else:
                        lastCardDanger = False
                else:
                    lastCardDanger = False
            else:
                lastCardDanger = False


            # Deciding the next player
            turn += 1
            myTurn = (myTurn+1) % 4

            while disqualified[myTurn]: # skip 
                turn += 1
                myTurn = (myTurn+1) % 4
                passes += 1

            if passes == 3:
                control = True
                passes = 0
            else:
                control = False



        # Game ends & scoring
        scoresRound = [-len(player1Hand), -len(player2Hand), -len(player3Hand), -len(player4Hand)]
        for i in range(4): # adjust penalties
            if scoresRound[i] == -13: # 13 cards remaining; never play any of his cards
                scoresRound[i] = -39
            elif scoresRound[i] < -9: # 10-12 cards remaining
                scoresRound[i] *= 2
        
        tempScoreSum = sum(scoresRound)
        if lastCardDanger: # prev player did not take precautions    
            scoresRound = [0,0,0,0]
            scoresRound[(myTurn-1) % 4] = tempScoreSum # prev player
        
        scoresRound[myTurn] = -tempScoreSum
        winsTotal[myTurn] += 1

        for i in range(4):
            scoresTotal[i] += scoresRound[i]
        


    return scoresTotal



if __name__ == '__main__':
    import time
    import argparse

    parser = argparse.ArgumentParser(description='Match Simulation for 4 players')
    parser.add_argument('n_games', type=int, help='number of games in a match')
    parser.add_argument('agent_1', type=str, help='agent 1')
    parser.add_argument('agent_2', type=str, help='agent 2')
    parser.add_argument('agent_3', type=str, help='agent 3')
    parser.add_argument('agent_4', type=str, help='agent 4')
    args = parser.parse_args()

    start = time.time()

    print(matchSimulation(args.n_games, args.agent_1, args.agent_2, args.agent_3, args.agent_4))

    end = time.time()
    print("time taken: " + str(end-start))
