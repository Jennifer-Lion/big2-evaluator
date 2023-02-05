'''
A module to allow for human players to play in matchSimulation
'''

from logic import Logic
from card import Card

logic = Logic()
card = Card()

def action(hand, field, control, turn, field_history, enemy1, enemy2, enemy3):
    
    print("hand: " + str(hand))
    print("last played: " + str(field))
    print("in control" if control else "not in control")
    print("these cards have been played before: " + str(field_history))
    print("next player has " + str(enemy1) + " card(s) left")
    print("next next player has " + str(enemy2) + " card(s) left")
    print("previous player has " + str(enemy3) + " card(s) left")

    validMove = False
    while not validMove:
        played = []
        done = False

        while not done:

            playCard = str(input("throw card one by one in the format of NS (e.g. 2D, AH). Enter 'done' to end turn, or 'pass' to skip turn: "))
            if playCard == 'done':
                done = True
            elif playCard == 'pass':
                done = True
                played = []
            else:
                played.append(playCard)

        try:
            played = card.sortingCards(played)
            if played in logic.possibleMoves(hand, field, control, turn):
                validMove = True
            else:
                print("Invalid move, try again.")
                # validMove = True
        except:
            print("Input contains an invalid card, check formatting.")

    return played
