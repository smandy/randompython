import collections
from pprint import pprint as pp
import pylab as pl
import numpy as np
import copy as cp

board = """
1 1 3 3
1 2 2 3
1 2 4 4
"""

initState = []



board = """
1 1 8 8 9 a a a
1 1 8 9 9 9 a a
1 2 8 6 9 b c c
2 2 8 6 b b b c
3 2 2 6 6 b d c
3 4 4 7 7 d d c
3 4 4 4 5 d d e
3 3 5 5 5 5 e e
"""

initState = [
    (1,0,4),
    (7,0,4),
    (0,2,1),
    (1,2,2),
    (7,2,3),
    (0,4,5),
    (0,6,5),
    (7,6,1),
    (3,7,3)
    
    ]


def parseInt(s):
    return int( f"0x{s}", base = 16 ) 


print("Woot")

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.coords = {} # (row,col) -> value. 0 = empty
        self.zones = collections.defaultdict(list) # List of (row,col) tuples

    def isValid(self):
        pass
        # Sanity check

    def emptySquares(self):
        return [q for q,v in self.coords.items() if v[0]==0]
        
    def zoneOccupied(self, zone):
        zoneNums = set( range( 1, len(self.zones[zone]) + 1))
        occupied = { self.coords[x][0] for x in self.zones[zone] if self.coords[x][0] }
        #print(zoneNums)
        #print(occupied)
        return occupied

    def zoneAvail(self, zone):
        nums = set( range(1, len(self.zones[zone]) + 1) )
        #print(f"nums is {nums}")
        occupied = self.zoneOccupied(zone)
        avail = nums - occupied
        #print(f"avail is {avail}")
        return avail
        
    def grid(self):
        ret = np.zeros( (self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                ret[i][j] = self.coords[ (i,j) ][1]
        return ret

    def isOnBoard( self, i_j ):
        (i,j) = (i_j)
        return i>=0 and i <self.rows and j>=0 and j<self.cols

    def adjacents( self, i_j):
        (i,j) = (i_j)
        candidates = [ (i + ioffset, j + joffset) for
                       ioffset in [-1,0, 1] for
                       joffset in [-1,0, 1] ]
        candidates = [ x for x in candidates if self.isOnBoard(x) and not x == i_j]
        return candidates

    def coordFor(self, i,j, border = 0.45):
        return (j + border, self.rows - border - i )

    def availableMoves(self):
        ret =  []
        es = self.emptySquares()
        for z in es:
            zone = self.coords[z][1]
            adj = self.adjacents(z)
            za = self.zoneAvail(zone)
            #print(z, adj, za)

            forbidden = { self.coords[x][0] for x in adj if self.coords[x][0] }
            ret.append((z, za - forbidden))
            #print(z, za, forbidden, za - forbidden)
        return ret
        
    
    def plot(self):
        pl.clf()
        pl.imshow(self.grid(), extent=(0, self.cols, 0, self.rows))
        #pl.text(0.5, 0.5, 'woot', size = 25, ha = 'center', va = 'center')

        border = 0.45
        for i in range( 0, self.rows):
            for j in range(0,self.cols):
                (x,y) = self.coordFor( i,j)
                pl.text( x,y, f"( {i},{j} )\n{self.coords[ (i,j)]}", size = 13, ha = 'center', va = 'center')
                if self.coords[ (i,j) ][0]:
                    pl.text( x,y, f"{self.coords[(i,j)][0]}", size = 30, ha = 'center', va = 'center')
                
        

def parseBoard(s, initState):
    lines = s.split("\n")[1:-1]
    lines = [x.replace(' ', '') for x in lines]

    assert size( { size(x) for x in lines } ) == 1, "Dodgy board"
    print(lines)

    ret = Board(len(lines), len(lines[0]))
    
    zones = collections.defaultdict(list)
    for i, line in enumerate(lines):
        for j, x in enumerate(line):
            x = parseInt(x)
            print((i, j, x))
            ret.zones[x].append((i, j))
            ret.coords[ (i,j)] = [0, x]
    for i,j,val in initState:
        ret.coords[(i,j)][0] = val
    return ret

print(__name__)
print(__name__ == '__main__')
if __name__ == '__main__' or True:
    print("Running")
    board = parseBoard(board, initState)
    pp(board.zones)
    board.plot()

    xs = sorted(board.availableMoves(), key = lambda x: len(x[1]))
    pp(xs)
