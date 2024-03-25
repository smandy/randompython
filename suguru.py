import collections
from pprint import pprint as pp
import pylab as pl
import numpy as np
import copy as cp
import pprint
import functools

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
        assert len( { len(x) for x in lines } ) == 1, "Dodgy board"
        #print(lines)
        zones = collections.defaultdict(list)
        coords = {}
        for i, line in enumerate(lines):
            for j, x in enumerate(line):
                x = parseInt(x)
                #print((i, j, x))
                zones[x].append((i, j))
                # current, zone, zones, zoneSet, 'can be'
                coords[ (i,j)] = [0, x, None, None, None]


                
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
            v[3] = set(range(len(self.zones[v[1]] )))

        self.movesMade = movesMade

        avail = self.availableMoves()
        newMoves = self.pruneMoves(avail)
        debug = [ x for x in newMoves if x[0] == (7,0) ]
        print(f"DEBUG: new 70's\n{debug}")
        
        #print(f"avail={len(avail)} pruned={len(pruned)}")
        #self.pruneMoves(self.availableMoves())

        #moveCoords = {x[0] for x in self.movesToMake}
        #newMoves = [ x for x in newMoves if not x[0] in moveCoords]
        self.movesToMake = newMoves

    def flatten(self, m2m):
        ret = []
        for (coord, moveSet) in m2m:
            for move in moveSet:
                ret.append( (coord, move) )
        return ret
        
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
        

    def pruneMoves(self, am):
        verboten = set(self.movesMade)
        verbotenCoords = { x[0] for x in self.movesMade }
        filtered = []
        for x in am:
            (coord, move ) = x
            if not x in verboten and not x[0] in verbotenCoords:
                filtered.append(x)
                for adj in self.adjacents(coord):
                    verboten.add( (adj, move))

                verboten.add( (coord,move))
                verbotenCoords.add( coord)
        print(f"Filtered {filtered}")
        return filtered

    def availableMoves(self):
        ret =  []
        rd = {}
        es = self.emptySquares()
        # Phase 1 - poison 
        #poisonList = self.poison(es)
        #self.debug(f"Poisonlist is {pprint.pformat(poisonList)}")

        for z,val in es.items():
            zone = val[1]
            adj = self.adjacents(z)
            za = self.zoneAvail(zone)

            #forbidden = { self.coords[x][0] for x in adj if self.coords[x][0] }.union({ x[1] for x in self.movesMade })
            forbidden = { self.coords[x][0] for x in adj if self.coords[x][0] }

            impossibleSquares = []
            finalMoves = za - forbidden
            #self.debug(f"finalMoves={finalMoves}")
            if finalMoves:
                ret.append((z, finalMoves))
                rd[z] = finalMoves
            else:
                impossibleSquares.append(f"Danger - impossible square {z} za={za}")

                # Short circuit the process - if there are 'broken' squares
                # then we shouldn't consider there to be *any* valid moves.

            if impossibleSquares:
                print(f"Impossible squares -\n{pprint.pformat(impossibleSquares)}")
                return []
            #self.debug(f"z={z} za={za} forbidden={forbidden} finalMoves={finalMoves}")


        # Every empty square should have an available move
        
            
        ret =  sorted(ret,key = lambda x: (len(x[1]) , - len(self.coords[x[0]][2])))

        ret2 = self.flatten(ret)

        debug = [ x for x in ret2 if x[0] == (7,0) ]
        print(f"DEBUG: incremental new 70's\n{debug}")
        
        return ret2


    def sanityCheck(self):


        # Debug - find (7,0)
        debug = [ x for x in self.movesToMake if x[0] == (0,7)]
        if debug:
            print(f"DEBUG: 70's\n{pprint.pformat(debug)}")
        
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
            assert b in [0,1], f"Duplicate move {a} {b}"

        # Zone stats
        for zone, coords in self.zones.items():
            stats = collections.defaultdict(int)
            for coord in coords:
                v = self.coords[coord][0]
                if v != 0:
                    stats[v] += 1
            badVals = [ x for x in stats.items() if x[1] not in {0,1} ]
            assert not badVals, f"Zone violation for zone={zone} stat={badVals}"

        # Consistency between movesmade and coords

        for coord, val in self.coords.items():
            if val[0]!=0:
                moves = [ x for x in self.movesMade if x== (coord,val[0])]
                assert len(moves)==1, f"Inconsistent movesmade c={coord} v={val} mm={self.movesMade} {moves}"

        # Hygeine
        #assert self.movesToMake[-1], f"Bad moves to make {self.movesToMake}"

    def adjecentZones(self, coord):
        zone = self.coords[coord][1]
        adj = [ x for x in self.adjacents(coord) if not self.coords[x][1] == zone ]
        zones = { self.coords[x][1] for x in adj  }
        return zones
            
    def doWork(self):
        if not self.movesToMake:
            print("doWork: No moves to make!")
            self.running = False
            self.verbose = True
            return

        if self.movesToMake:
            self.debug("dowork: Make move")
            self.makeMove()
        else:
            self.debug("doWork: Backtracking")
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
        (coord, move) = self.movesToMake.pop()

        if coord == (6,4) and self.running and False:
            print("Debug breakpoint")
            self.running = False
            self.verbose = True
            return
        
        # Make the actual move
        self.debug(f"makeMove {coord} -> {move}")

        existing = self.coords[coord][0]
        assert existing in [0,move], f"Try to set populated square {coord}->{move} vs existing={existing}"
        if existing == 0:
            self.coords[coord][0] = move
            self.movesMade.append( (coord, move))

        # Not restrictive enough - need to check available moves for empty square
        am = self.availableMoves()
        amCords = {x[0] for x in am}
        es = self.emptySquares()

        # Zone availability
        # Ensure that available moves for empty squares in a zone covers
        # Size of each zone

        if 0:
            amDict = { q : v for q,v in am }
            for zone, coords in self.zones.items():
                impossible = board.zoneAvail(zone)
                #print( f"Need {impossible} for zone {zone}")
                for coord in coords:
                    if coord in amDict:
                        impossible.discard(amDict[coord])
                    self.debug( f"zone={zone} zoneAvail {coord}->{move} impossible={impossible}")
                if impossible:
                    print(f"zone {zone} impossible {impossible} need {board.zoneAvail(zone)}")
                    self.backTrack()
                    return


        #flatMoves = functools.reduce( lambda a,b: a+b, self.movesToMake)
        newMoves = self.pruneMoves(self.availableMoves())
        moveCoords = {x[0] for x in newMoves}
        populated = [ coord for coord,value in self.coords.items() if value[0] ]
        self.movesToMake += [ x for x in newMoves if not x[0] in moveCoords and not x[0] in populated]


        self.populateAllowedValues()
        
        if len(self.movesMade) == self.rows * self.cols:
            print("Yowza - solution")

    def populateAllowedValues(self):
        for q,myVal in self.coords.items():
            myVal[4] = cp.copy(myVal[3])

            # Exclude adjacents
            for adj in self.adjacents(q):
                otherVal = self.coords[adj]
                if otherVal[0] != 0:
                    myVal[4].discard(otherVal[0])

            # Exclude zone occupants
            myVal[4] -= self.zoneOccupied(myVal[1])
                    
    
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

    count = 0
    def iter():
        global count
        board.doWork()
        pl.clf()
        board.plot()
        count += 1

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

    multIter(30)
    #board.verbose = True
    

