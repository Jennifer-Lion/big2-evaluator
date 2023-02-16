import matchSimulation as match

import os
import math
import numpy as np

fileList = os.listdir('agents')
fileNameList = [x.split('.')[0] for x in fileList]

my_file = open("agents.txt", "r") #agentsFile as a str in .txt 
agentsList = my_file.read().split("\n")
my_file.close()

# ignore those that are not found in the 'agents' folder to prevent error
agentsList = [x for x in agentsList if x in fileNameList] 



def singleElim(n_games):
    ranking = {} # lowest rank = n_rounds+1; highest rank = 1

    n_agents = len(agentsList)
    n_rounds = math.ceil(math.log(n_agents, 2))

    in_play = agentsList.copy() # agents that are still in the game after each round
    in_play_dummy = agentsList.copy() # duplicate, to remove eliminated agents while in_play is being looped through

    to_bye = 2**math.ceil(math.log(n_agents, 2)) - n_agents # no. of agents to be assigned a bye in first round
    to_play = n_agents - to_bye # no. of agents to play first round

    print("Starting pair-wise single-elimination tournament on " + str(n_agents) + " agents")

    for round_n in range(n_rounds): # loop through each round of elimination
        print("\nround " + str(round_n + 1))
        np.random.shuffle(in_play) # reduce match-up bias

        for i in range(len(in_play)//2): # loop through each match of 2 players
            
            # assigning bye's in the first round
            if round_n == 0 and (i*2) >= to_play:
                for j in range(i*2, (i*2 + to_bye)):
                    print(str(in_play[j]) + " did not play - assigned 'BYE' ==> proceeds to next round \n")
                break

            print(str(in_play[i*2]) + " vs " + str(in_play[i*2 + 1]))
            scores = match.matchSimulation(n_games, in_play[i*2], in_play[i*2 + 1], in_play[i*2], in_play[i*2 + 1]) # A vs B vs A vs B
            A_sum = (scores[0] + scores[2])
            B_sum = (scores[1] + scores[3])

            # elimination
            if A_sum < B_sum:
                in_play_dummy.remove(in_play[i*2])
                ranking[in_play[i*2]] = n_rounds + 1 - round_n 
                print(str(in_play[i*2 + 1]) + " wins this match! \n")
            else:
                in_play_dummy.remove(in_play[i*2 + 1])
                ranking[in_play[i*2 + 1]] = n_rounds + 1 - round_n 
                print(str(in_play[i*2]) + " wins this match! \n")
        
        # update the list of players who are still in play after each round
        in_play = in_play_dummy.copy() 


    ranking[in_play[0]] = 1 # the only agent left in the game is the winner (rank=1)
    return ranking



def swiss(n_games):
    players = agentsList.copy()
    swissPoints = {}
    for agent in players:
        swissPoints[agent] = 0

    n_agents = len(players)
    n_rounds = math.ceil(math.log(n_agents, 2))

    np.random.shuffle(players) # reduce first round's match-up bias

    print("Starting Swiss-style tournament on " + str(n_agents) + " agents")

    for round_n in range(n_rounds): # loop through each round of elimination
        print("\nround " + str(round_n + 1))

        for i in range(len(players)//4): # loop through each match of 4 players
            print(str(players[i*4]) + " vs " + str(players[i*4 + 1]) + " vs " + str(players[i*4 + 2]) + " vs " + str(players[i*4 + 3]))
            scores = match.matchSimulation(n_games, players[i*4], players[i*4 + 1], players[i*4 + 2], players[i*4 + 3]) # A vs B vs C vs D

            # add swissPoints to the top 2 players
            low_to_high = np.argsort(scores) # index of players from losers to winners (0,1,2,3)
            swissPoints[players[i*4 + low_to_high[2]]] += 1
            swissPoints[players[i*4 + low_to_high[3]]] += 1

        # if only 1 player has no match-up, assign bye
        if len(players)%4 == 1:
            swissPoints[players[-1]] += 1
            print(players[-1] + " did not play - assigned 'BYE' ==> swissPoints + 1 \n")

        # if 2 players have no match-up, do a pairwise match
        elif len(players)%4 == 2:
            print(str(players[-2]) + " vs " + str(players[-1]))
            scores = match.matchSimulation(n_games, players[-2], players[-1], players[-2], players[-1]) # A vs B vs A vs B
            A_sum = (scores[0] + scores[2])
            B_sum = (scores[1] + scores[3])

            # add swissPoints to the winner
            if A_sum < B_sum:
                swissPoints[players[-1]] += 1
            else:
                swissPoints[players[-2]] += 1

        # if 3 players have no match-up, do a pairwise match on 2 players & assign bye on 1 player 
        elif len(players)%4 == 3:
            print(str(players[-3]) + " vs " + str(players[-2]))
            scores = match.matchSimulation(n_games, players[-3], players[-2], players[-3], players[-2]) # A vs B vs A vs B
            A_sum = (scores[0] + scores[2])
            B_sum = (scores[1] + scores[3])

            # add swissPoints to the winner
            if A_sum < B_sum:
                swissPoints[players[-2]] += 1
            else:
                swissPoints[players[-3]] += 1

            swissPoints[players[-1]] += 1
            print(players[-1] + " did not play - assigned 'BYE' ==> swissPoints + 1 \n")            

        # sort the players based on swissPoints in descending order
        tieRandom = {k: v+np.random.uniform(0,0.5) for k, v in swissPoints.items()} # dummy dictionary to break ties randomly
        players = [k for k, v in sorted(tieRandom.items(), key=lambda x:x[1], reverse=True)]
        

    ranking = {k: (n_rounds - v + 1) for k, v in swissPoints.items()}
    return ranking




if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Implement tournament for agents')
    parser.add_argument('n_games', type=int, help='number of games in a match')
    parser.add_argument('type', type=str, help='"single" or "swiss"')
    args = parser.parse_args()

    if args.type == "single":
        print(singleElim(args.n_games))
    elif args.type == "swiss":
        print(swiss(args.n_games))
