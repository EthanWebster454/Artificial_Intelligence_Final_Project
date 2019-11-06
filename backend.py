import random as rand
import numpy as np


def minConflicts(board, n):

    numPieces = len(board)

    cl=[None]*numPieces

    # for ease of access, make a matrix that details the board layout
    boardMatrix = np.zeros((n,n),dtype=bool)


    # update conflicts and board layout matrix
    for ki in range(numPieces):
        _,k,l = board[ki]
        boardMatrix[k,l] = True
        cl[ki] = findConflicts(board, ki, (k,l), numPieces)


    # see if the current layout is a solution
    if all(ncf==0 for ncf in cl):
        return board, True


    # choose a random piece with conflicts
    while (True):
        ri = rand.randint(0,numPieces-1)
        if cl[ri] > 0:
            break

    # obtain the randomly chosen piece
    (pieceName,x,y) = board[ri]

    # find the conflicts for all the pieces on the board
    currConflicts = [(cl[ri],(x,y))]
    for i in range(n):
        for j in range(n):
            if not boardMatrix[i,j] and (i,j) != (x,y):
                currConflicts.append((findConflicts(board, ri, (i,j), numPieces), (i,j)))

    (minC,coords) = min(currConflicts, key=first)

    # check to see if there is a move that grants fewer or equal conflicts
    # if so, randomly break ties and update the conflict list
    if minC <= cl[ri]:
        
        shortConflictsList = [t for t in currConflicts if t[0] == minC]
        numCL = len(shortConflictsList)
        if numCL > 1:
            newC = shortConflictsList[rand.randint(0, len(shortConflictsList)-1)]
        else:
            newC = (minC,coords)

        board[ri] = (pieceName, newC[1][0], newC[1][1])

    
    return board, False




# finds conflicts for all pieces on the board excluding current piece
def findConflicts(board, exclude, c, n):

    directions=[]
    conflicts = 0
    myName = board[exclude][0]

    x, y = c

    # this part checks for pieces that can attack the current one
    # then checks to see what pieces the current one can attack
    for unit in range(n):
        if unit != exclude:
            (currName,i,j) = board[unit]

            # check for attack from other piece
            d = findDirection(x,y,i,j,currName)
            if d and d not in directions:
                directions.append(d)
                conflicts+=1

            # check if current piece can attack this one
            d = findDirection(x,y,i,j,myName)
            if d and d not in directions:
                directions.append(d)
                conflicts+=1

    return conflicts

    

# this finds the direction of attack between two pieces if one exists
def findDirection(x,y,i,j,pn):

    if pn == 'queen':
        if x == i:
            return 1
        elif y == j:
            return 2
        elif x - i == y - j:
            return 3
        elif abs(x-i) == abs(y-j):
            return 4
        else:
            return False
    elif pn == 'rook':
        if x == i:
            return 1
        elif y == j:
            return 2
        else:
            return False
    elif pn == 'bishop':
        if x - i == y - j:
            return 3
        elif abs(x-i) == abs(y-j):
            return 4
        else:
            return False
    elif pn == 'knight':
        if x-1==i and y-2==j:
            return 5
        elif x-1==i and y+2==j:
            return 6
        elif x+1==i and y-2==j:
            return 7
        elif x+1==i and y+2==j:
            return 8
        elif x-2==i and y-1==j:
            return 9
        elif x-2==i and y+1==j:
            return 10
        elif x+2==i and y-1==j:
            return 11
        elif x+2==i and y+1==j:
            return 12
            


def first(a):
    return a[0]
