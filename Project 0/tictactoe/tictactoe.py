"""
Tic Tac Toe Player
"""

import math
import random
import copy

X = "X"
O = "O"
EMPTY = None

#play=0
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
    #raise NotImplementedError
    #return 

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    pos=[]
    for i , row in enumerate(board):
        for  j , col in enumerate(row):
            if col == None:
                pos.append((i,j))
    return set(pos)

    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    """
    if board[action[0],action[1]] != EMPTY:
        if play%2 == 1:
            board[action[0],action[1]]=X
        else:
            board[action[0],action[1]]=O
        return board
    else:
        raise Exception("Invalid Move")
    """
    play=player(board)
    if play == X:
        ans=X
    else:
        ans=O
    #Nb=board.copy()
    Nb=copy.deepcopy(board)
    if Nb[action[0]][action[1]] == EMPTY:
        Nb[action[0]][action[1]] = ans
        return Nb
    else:
        raise Exception("Invalid Move")

    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #raise NotImplementedError
    [r0,r1,r2,c0,c1,c2,d0,d1] =checker(board)
    if r0 or r1 or r2 or c0 or c1 or c2 or d0 or d1:
        ans = [r0,r1,r2,c0,c1,c2,d0,d1]
        if ans.index(True) in [0,3,6]:
            return board[0][0]
        elif ans.index(True) in [1,4,7]:
            return board[1][1]
        else:
            return board[2][2]
    else:
        return (None)

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    [r0,r1,r2,c0,c1,c2,d0,d1] =checker(board)

    if r0 or r1 or r2 or c0 or c1 or c2 or d0 or d1 or counter(board,None)==0:
        return (True)
    else:
        return (False)
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    ans=winner(board)
    if ans == X:
        return (1)
    elif ans == O:
        return (-1)
    else:
        return (0)
    #raise NotImplementedError


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
    #if AI == X :
    #    goal = 1
    #else :
    #    goal = -1
    #pos=list(actions(board))
    pos=optimise(board,player(board))
    return random.choice(pos)
    ####################################Unable to choose from Empty set
    #raise NotImplementedError


def optimise(board,AI):
    if AI == X:
        NAI = O
    else:
        NAI = X
    #ans=[]
    ans = []
        
    pos=list(actions(board))
    for move in pos :
    #   move=random.choice(list(pos))
        Nb=result(board,move)
        if terminal(Nb) is False:
            ans.append(fighter(Nb,NAI))
        else:
            ans.append(utility(Nb))
    optimal=[]
    for i ,check in enumerate(ans):
        if AI == X :
            if check is max(ans):
                optimal.append(pos[i])
        else:
            if check is min(ans):
                optimal.append(pos[i])
    return optimal

def fighter(board,AI):
    if AI == X:
        NAI = O
    else:
        NAI = X
    ans =[]
    pos=list(actions(board))
    for move in pos :
        Nb=result(board,move)
        if terminal(Nb) is False:
            ans.append(fighter(Nb,NAI))
        else:
            ans.append(utility(Nb))
        if AI == X:
            if max(ans) is 1:
                return 1
        else:
            if min(ans) is -1:
                return -1

    if AI == X:
        return max(ans)
    else:
        return min(ans)