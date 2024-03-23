import collections
from pprint import pprint as pp
import pylab as pl
import numpy as np
import copy as cp
import pprint 

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

    @classmethod
    def parse(cls, s, initState):
        lines = s.split("\n")[1:-1]
        lines = [x.replace(' ', '') for x in lines]
        assert size( { size(x) for x in lines } ) == 1, "Dodgy board"
        #print(lines)
        zones = collections.defaultdict(list)
        coords = {}
        for i, line in enumerate(lines):
            for j, x in enumerate(line):
                x = parseInt(x)
                #print((i, j, x))
                zones[x].append((i, j))
                coords[ (i,j)] = [0, x, None]


        movesMade = []
        for i,j,val in initState:
            coords[(i,j)][0] = val
            movesMade.append( ((i,j),val))
        return Board(len(lines), len(lines[0]), coords, zones, movesMade)

    
    def __init__(self, rows, cols, coords, zones, movesMade):
        self.verbose = False
        self.running = True
        self.rows = rows
        self.cols = cols
        self.coords = coords # (row,col) -> value. 0 = empty
        self.zones = zones # List of (row,col) tuples
        for q,v in self.coords.items():
            v[2] = self.adjecentZones(q)
        self.movesMade = movesMade
        self.movesToMake = [ self.availableMoves() ]
        
    def isValid(self):
        pass
        # Sanity 

    def emptySquares(self):
        return { q : v for q,v in self.coords.items() if v[0]==0}
        
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

    def avail(self,z,moves):
        pass


    def poison(self, es):
        poisonList = collections.defaultdict(set)
        for z, moves in es.items():
            for c in self.adjacents(z):
                if self.coords[c][0]:
                    poisonList[z].add( self.coords[c][0])
        return poisonList
        

    def pruneMoves(self, am1):
        am = { q:v for q,v in am1}
        coords = am.keys()
        bad = []
        
        for quay in coords:
            moves1 = am[quay]
            adjs = self.adjacents(quay)
            for adj in adjs:
                if adj in am:
                    moves2 = am[adj]
                    contradiction = moves1.intersection(moves2)
                    for x in contradiction:
                        bad.append( (f"{quay}->{moves1} {adj}->{moves2} {contradiction}", quay, adj, contradiction))

        for s, c1, c2, contradiction in bad:
            am[c1] -= contradiction
            #am[c2] -= contradiction
        print(f"Final dict {am}")
            
    
    def availableMoves(self):
        ret =  []
        es = self.emptySquares()
        # Phase 1 - poison 
        poisonList = self.poison(es)

        self.debug(f"Poisonlist is {pprint.pformat(poisonList)}")

        for z,val in es.items():
            zone = val[1]
            adj = self.adjacents(z)
            za = self.zoneAvail(zone)

            #forbidden = { self.coords[x][0] for x in adj if self.coords[x][0] }.union({ x[1] for x in self.movesMade })
            forbidden = { self.coords[x][0] for x in adj if self.coords[x][0] }

            impossibleSquares = []
            finalMoves = za - forbidden - poisonList[z]
            if finalMoves:
                ret.append((z, finalMoves))
            else:
                impossibleSquares.append(f"Danger - impossible square {z} za={za} poison={poisonList[z]} forbidden={forbidden}")

                # Short circuit the process - if there are 'broken' squares
                # then we shouldn't consider there to be *any* valid moves.

            if impossibleSquares:
                print(f"Impossible squares -\n{pprint.pformat(impossibleSquares)}")
                return []
            self.debug(f"z={z} za={za} forbidden={forbidden} finalMoves={finalMoves}")


        # Every empty square should have an available move
        
            
        ret =  sorted(ret,key = lambda x: (len(x[1]) , len(self.coords[x[0]][2])))

        #self.pruneMoves(ret)
        return ret


    def sanityCheck(self):
        # 2 main checks - no invalid adjacents - no overpopulated zones

        for z in self.coords:
            if not self.coords[z][0]:
                continue
            for y in self.adjacents(z):
                assert self.coords[y][0] != self.coords[z][0], \
                    f"Adjacent call violation {z} {self.coords[z]} vs {y} {self.coords[y]}"

        # movesmade is consistent i.e. no dupes
        stats = collections.defaultdict(int)
        for coord, move in self.movesMade:
            stats[coord] += 1
        for a,b in stats.items():
            assert b in [0,1], f"Duplicate move {coord}"

        # Zone stats
        for zone, coords in self.zones.items():
            stats = collections.defaultdict(int)
            for coord in coords:
                v = self.coords[coord][0]
                if v != 0:
                    stats[v] += 1
            badVals = [ x for x in stats.items() if x[1] not in {0,1} ]
            assert not badVals, f"Zone violation! {badVals}"

        # Consistency between movesmade and coords

        for coord, val in self.coords.items():
            if val[0]!=0:
                moves = [ x for x in self.movesMade if x== (coord,val[0])]
                assert len(moves)==1, f"Inconsistent movesmade c={coord} v={val} mm={self.movesMade} {moves}"

    def adjecentZones(self, coord):
        zone = self.coords[coord][1]
        adj = [ x for x in self.adjacents(coord) if not self.coords[x][1] == zone ]
        zones = { self.coords[x][1] for x in adj  }
        return zones
            
    def doWork(self):
        if self.movesToMake[-1]:
            if self.movesToMake[-1][0][1]:
                #print("Make move")
                self.makeMove()
            else:
                self.movesToMake[-1] = self.movesToMake[-1][1:]
        else:
            print("Backtrack")
            self.backTrack()
            self.movesToMake.pop()
        self.sanityCheck()


    def backTrack(self, n = 1):
        #print("Backtrack!!!")
        #self.movesToMake.pop()
        for x in range(n):
            lastMove = self.movesMade.pop()
            coord, move = lastMove
            print(f"Backtrack {x} removing {coord}")
            self.coords[coord][0] = 0


    def debug(self, s):
        if self.verbose:
            print(s)
            
        
    def makeMove(self):
        #toMove = [ x for x in self.movesToMake[-1] if len( x[1] ) == 1]
        #print(f"toMove is {pprint.pformat(toMove)}")

        coord, moveSet = self.movesToMake[-1][0]

        if coord == (6,4) and self.running and False:
            print("Debug breakpoint")
            self.running = False
            self.verbose = True
            return
        
        move = moveSet.pop()
        if not moveSet:
            self.movesToMake[-1] = self.movesToMake[-1][1:]

        # Make the actual move
        self.debug(f"makeMove {coord} -> {move}")
        self.coords[coord][0] = move
        self.movesMade.append( (coord, move))

        # Not restrictive enough - need to check available moves for empty square
        am = self.availableMoves()
        amCords = {x[0] for x in am}
        es = self.emptySquares()

        badSquares = []

        self.debug(f"amCords={amCords} am={am}")
        
        for (coord2, val) in es.items():
            #self.debug(f"coord={coord} am={pprint.pformat(am)}")
            if not coord2 in amCords:
                badSquares.append(coord2)
        if badSquares:
            print(f"Bad squares (can't move) after move {coord}->{move}\n{pprint.pformat(badSquares)}")

            self.backTrack()
            return

        

        # Zone availability
        # Ensure that available moves for empty squares in a zone covers
        # Size of each zone

        amDict = { q : v for q,v in am }
        for zone, coords in self.zones.items():
            impossible = board.zoneAvail(zone)
            #print( f"Need {impossible} for zone {zone}")
            for coord in coords:
                impossible -= amDict.get(coord, set() )
                self.debug( f"zoneAvail {coord}->{move} impossible={impossible}")
            if impossible:
                print(f"zone {zone} impossible {impossible} need {board.zoneAvail(zone)}")
                self.backTrack()
                return
            
        self.movesToMake.append(self.availableMoves())
        if len(self.movesMade) == self.rows * self.cols:
            print("Yowza - solution")
    
    def plot(self):
        pl.clf()
        pl.imshow(self.grid(), extent=(0, self.cols, 0, self.rows))
        #pl.text(0.5, 0.5, 'woot', size = 25, ha = 'center', va = 'center')

        border = 0.45
        for i in range( 0, self.rows):
            for j in range(0,self.cols):
                (x,y) = self.coordFor( i,j)
                pl.text( x,y, f"( {i},{j} )\n{self.coords[ (i,j)][:2]}", size = 13, ha = 'center', va = 'center')
                if self.coords[ (i,j) ][0]:
                    pl.text( x,y, f"{self.coords[(i,j)][0]}", size = 30, ha = 'center', va = 'center')
                
        


print(__name__)
print(__name__ == '__main__')
if __name__ == '__main__' or True:
    #print("Running")
    board = Board.parse(board, initState)
    #pp(board.zones)
    #board.plot()
    #xs = sorted(board.availableMoves(), key = lambda x: len(x[1]))

    pl.clf()

    def iter():
        board.doWork()
        pl.clf()
        board.plot()

    def multIter(n):
        for i in range(n):
            iter()
            if not board.running:
                print("Breaking!")
                break
    
    while board.movesToMake and False:
        board.doWork()
        #xboard.plot()
        #time.sleep(1)
    #pp(xs)
    board.plot()

    
    #multIter(5)
    board.verbose = True
    

