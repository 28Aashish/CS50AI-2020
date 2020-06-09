"""
Tic Tac Toe Player
"""

import math
import random
import copy

X = "X"
O = "O"
EMPTY = None


def counter(board , val):
    c=0
    for i in board:
        c+= i.count(val)
    return c

def checker(board):
    
    r0 = board[0][0] == board[0][1] == board[0][2] != None
    r1 = board[1][0] == board[1][1] == board[1][2] != None
    r2 = board[2][0] == board[2][1] == board[2][2] != None

    c0 = board[0][0] == board[1][0] == board[2][0] != None
    c1 = board[0][1] == board[1][1] == board[2][1] != None
    c2 = board[0][2] == board[1][2] == board[2][2] != None

    d0 = board[0][0] == board[1][1] == board[2][2] != None
    d1 = board[2][0] == board[1][1] == board[0][2] != None
    return ([r0,r1,r2,c0,c1,c2,d0,d1])

def initial_state():
    """
    Returns starting state of the board.
    """
    #play=0
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    #raise NotImplementedError
    #Checking Number of X and O to Choose X or O chance
    P1=counter(board,X)
    P2=counter(board,O)
    if P1 == P2:
        return X
    else:
        return O
    """
    play += 1
    if play % 2 == 1:
        return 1
    else :
        return 2
    """
    
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #raise NotImplementedError
    #Checking available actions from Board
    pos=[]
    for i , row in enumerate(board):
        for  j , col in enumerate(row):
            if col == None:
                pos.append((i,j))
    return set(pos)



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #raise NotImplementedError
    #Checking Player
    play=player(board)
    if play == X:
        ans=X
    else:
        ans=O
    #Making a deep copy of Board
    Nb=copy.deepcopy(board)
    #Putting X or O on the Board
    if Nb[action[0]][action[1]] == EMPTY:
        Nb[action[0]][action[1]] = ans
        return Nb
    else:
        raise Exception("Invalid Move")



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #raise NotImplementedError
    # checker Funtion give Bools with all possible Row/Column/Diagonal for Movement
    [r0,r1,r2,c0,c1,c2,d0,d1] =checker(board)
    #If we got the Winner then We have to Retrun Symbol
    if r0 or r1 or r2 or c0 or c1 or c2 or d0 or d1:
        ans = [r0,r1,r2,c0,c1,c2,d0,d1]
        if ans.index(True) in [0,3,6]:
            return board[0][0]
        elif ans.index(True) in [1,4,7]:
            return board[1][1]
        else:
            return board[2][2]
    #Else No one is Winner
    else:
        return (None)

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #raise NotImplementedError
    
    #From Checker We will be Getting Win / Continue State of Board
    [r0,r1,r2,c0,c1,c2,d0,d1] =checker(board)
    
    #Returning if True When End or No Moves Left
    if r0 or r1 or r2 or c0 or c1 or c2 or d0 or d1 or counter(board,None)==0:
        return (True)
    else:
        return (False)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #raise NotImplementedError
    #Used By MinMax Procedural
    ans=winner(board)
    if ans == X:
        return (1)
    elif ans == O:
        return (-1)
    else:
        return (0)

#Trial Function to Implement Easy(Random) Moves on Runner 155 line change move=ttt.easy()
def easy(board):
    pos=list(actions(board))
    return random.choice(pos)

#######################################################################################
################################MIN MAX Implementation#################################
#######################################################################################
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #raise NotImplementedError
    
    #Logic for MinMax
        #if AI == X :
        #    goal = 1
        #else :
        #    goal = -1
        #pos=list(actions(board))
    pos=optimise(board,player(board))
    return random.choice(pos)

def optimise(board,AI):
    #check AI
    if AI == X:
        NAI = O
    else:
        NAI = X
    #List for inculcating Moves and Their Min-Max Value
    ans = []
    #Available Option
    pos=list(actions(board))
    #Checking Move
    for move in pos :
        Nb=result(board,move)
        #If Game Doesn't End Then Fighter Function for recurring
        if terminal(Nb) is False:
            ans.append(fighter(Nb,NAI))
        #Else Game End
        else:
            ans.append(utility(Nb))
    #Optimal Move is Checked
    optimal=[]
    for i ,check in enumerate(ans):
        #If AI is X then Try for Maximize 
        if AI == X :
            if check is max(ans):
                optimal.append(pos[i])
        #If AI is O then Try for Minmize
        else:
            if check is min(ans):
                optimal.append(pos[i])
    return optimal

#Recursive Function for Endding Check
def fighter(board,AI):
    #Checking AI
    if AI == X:
        NAI = O
    else:
        NAI = X
    #Checking Move
    ans =[]
    pos=list(actions(board))
    for move in pos :
        Nb=result(board,move)
        #If Game Not End the Fighter(Recursed) with New Board
        if terminal(Nb) is False:
            ans.append(fighter(Nb,NAI))
        #If End Then We append Ans
        else:
            ans.append(utility(Nb))
    #Giving Last MAX/MIN as per The AI wanted
    if AI == X:
        return max(ans)
    else:
        return min(ans)