import random as rand


def minConflicts(board, n, cl):

    # quick n dirty: fix this later...
    while (True):
        ri = rand.randint(0,n-1)
        if cl[ri] > 0:
            break

    
    (pieceName,x,y) = board[ri]

    currConflicts = []

    for i in range(n):
        if i != x:
            cc = (i,y)
            currConflicts.append((findConflicts(board, ri, (i,y), n), cc))

    (minC,coords) = min(currConflicts, key=first)

    # maybe change to <= to prevent pieces from being too "rooted" in place
    if minC <= cl[ri]:

        shortConflictsList = [t for t in currConflicts if t[0] == minC]
        numCL = len(shortConflictsList)
        if numCL > 1:
            newC = shortConflictsList[rand.randint(0, len(shortConflictsList)-1)]
        else:
            newC = (minC,coords)

        board[ri] = (pieceName, newC[1][0], newC[1][1])

        cl[ri] = minC


    # update conflicts
    for ki in range(n):
        pieceN,k,l = board[ki]
        cl[ki] = findConflicts(board, ki, (k,l), n)


    if all(ncf==0 for ncf in cl):
        return board, cl, True
    
    return board, cl, False






# only finds conflicts for queen so far
def findConflicts(board, exclude, c, n):

    directions=[]
    conflicts = 0

    x, y = c

    for unit in range(n):
        if unit != exclude:
            (_,i,j) = board[unit]
            d = findDirection(x,y,i,j)
            if d and d not in directions:
                directions.append(d)
                conflicts+=1

    return conflicts

    

def findDirection(x,y,i,j):

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


def first(a):
    return a[0]