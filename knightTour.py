import numpy as np
from itertools import product, islice
import pylab as pl
import matplotlib.patches as patches

DEFAULT_BOARDSIZE = 8

knightMoves = [ (x,y) for (x,y) in product([2,1,-2,-1],[-1,2,1,-2])
                if abs(x)!=abs(y) ]
def add(x,y):
    return (x[0]+y[0], x[1]+y[1])

def isOnBoard(p, boardSize):
    x,y = p
    return x>=0 and x<boardSize and y>=0 and y<boardSize

def possibleMoves( visited ,
                   boardSize):
    candidates = [ add(visited[-1],x) for x in knightMoves ]
    return [ x for x in candidates if isOnBoard(x, boardSize) and not x in visited ]

def bestMove( xs,
              visited,
              boardSize):
    # Return the move which, when made, will leave us with the
    # least number of subsequent possible moves. Very counterintuitive!
    # Warnsdorf's rule & https://en.wikipedia.org/wiki/Knight%27s_tour
    tmp = [ (x, len(possibleMoves( visited + [x], boardSize))) for x in xs ]
    return sorted(tmp, key = lambda x: x[1] )[0][0]

def closedTour(boardSize, startingpoint = (0,0)):
    for tour in doTour(boardSize, startingpoint):
        for x in knightMoves:
            if add(x,tour[-1]) == startingpoint:
                yield tour

def doTour(boardSize ,
           startingPoint = (0,0)):
    squares = boardSize * boardSize
    # Bootstrap
    visited = [ startingPoint ]
    movesToMake = [possibleMoves(visited, boardSize)]
    # Iterate
    while movesToMake:
        if movesToMake[-1]:
            moveToMake = bestMove(movesToMake[-1], visited, boardSize)
            movesToMake[-1].remove(moveToMake)
            visited.append(moveToMake)
            if len(visited)==squares:
                yield visited[:]
            movesToMake.append( possibleMoves(visited, boardSize))
        else:
            # Backtrack
            movesToMake.pop()
            visited.pop()

def plotTour(ps, boardSize, isClosed = False):
    xs0, ys0 = zip(*ps)
    ax = pl.gca()
    major_ticks = np.arange(0, boardSize)
    ax.set_xticks(major_ticks)
    ax.set_xticks(major_ticks)
    for x in range(boardSize):
        for y in range(boardSize):
            if (x+y) % 2 == 0:
                ax.add_patch(
                patches.Rectangle(
                    (x,y), 1,1,
                    facecolor="black"))

    xs1 =  [ x + 0.5 for x in xs0]
    ys1 =  [ x + 0.5 for x in ys0]
    
    if isClosed:
        xs1.append(xs1[0])
        ys1.append(ys1[0])
        
    pl.plot( xs1, ys1, 'ro-',  linewidth = 5, markersize = 10)
    pl.plot( xs1[:1], ys1[:1], 'go',  markersize = 10)
    pl.plot( xs1[-2:-1], ys1[-2:-1], 'bo', markersize = 10)
     
if __name__=='__main__':
    pl.clf()
    X,Y = 1,1
    boardSize = 8
    for i,x in enumerate(islice(closedTour(boardSize,(0,0)),X * Y)):
        pl.subplot(X,Y,i+1)
        plotTour(x, boardSize, isClosed = True)
