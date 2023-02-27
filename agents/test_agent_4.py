# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:57:58 2019

"""

from logic import Logic
from card import Card

logic = Logic()
card = Card()

def action(hand, field, control, turn, field_history, enemy1, enemy2, enemy3):
    
    if type(hand) != list:
        hand = hand.translate({ord('"'):None})
        hand = hand.translate({ord(']'):None})
        hand = hand.translate({ord('['):None})
        hand = hand.translate({ord("'"):None})
        hand = hand.translate({ord(' '):None})
        hand = hand.split(",")

    if type(field) != list:
        if field == "[',']":
            field = []
        else:
            field = field.translate({ord('"'):None})
            field = field.translate({ord(']'):None})
            field = field.translate({ord('['):None})
            field = field.translate({ord("'"):None})
            field = field.translate({ord(' '):None})
            field = field.split(",")

    if control == "true" or control == "True":
        control = True
    elif control == "false" or control == "False":
        control = False
    
    moveLists = logic.possibleMoves(hand, field, control, turn)
    if len(moveLists) == 0 or (len(field) != 1 and not control):
        return []
    else:
        return moveLists[0]

import sys

if __name__ == "__main__":
    st1=sys.argv[1]
    st2=sys.argv[2]
    st3=sys.argv[3]
    st4=int(sys.argv[4])
    st5=sys.argv[5]
    st6=int(sys.argv[6])
    st7=int(sys.argv[7])
    st8=int(sys.argv[8])
    print(" ".join(action(st1, st2, st3, st4, st5, st6, st7, st8)))