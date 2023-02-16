import matchSimulation as match

import os
import random
import math

fileList = os.listdir('agents')
fileNameList = [x.split('.')[0] for x in fileList]

my_file = open("agents.txt", "r") #agentsFile as a str in .txt 
# maybe can make the filename into a cmd arg
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

    for round_n in range(n_rounds):
        print("round " + str(round_n + 1))
        random.shuffle(in_play) # reduce match-up bias

        for i in range(len(in_play)//2): # loop through each match of 2 players; last player will not play if it's odd
            # print(agentsList)
            # print(in_play)
            # print(in_play_dummy)
            print(str(in_play[i*2]) + " vs " + str(in_play[i*2 + 1])) # out of range LOOK AT THIS AGAIN
            scores = match.matchSimulation(n_games, in_play[i*2], in_play[i*2 + 1], in_play[i*2], in_play[i*2 + 1]) # A vs B vs A vs B
            A_sum = (scores[0] + scores[2])
            B_sum = (scores[1] + scores[3])

            # elimination
            if A_sum < B_sum:
                in_play_dummy.remove(in_play[i*2])
                ranking[in_play[i*2]] = n_rounds + 1 - round_n 
            else: # this includes tie... maybe find a better way to handle ties !!
                in_play_dummy.remove(in_play[i*2 + 1])
                ranking[in_play[i*2 + 1]] = n_rounds + 1 - round_n 
        
        in_play = in_play_dummy.copy() # update the list of players who are still in play after each round

    ranking[in_play[0]] = 1 # the only agent left in the game is the winner (rank=1)
    return ranking



def swiss(n_games):

    match.matchSimulation(4, agentsList[0], agentsList[1], agentsList[2], agentsList[3])



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