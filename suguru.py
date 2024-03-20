board = """
1 1 3 3
1 2 2 3
1 2 4 4
"""

import collections
from pprint import pprint as pp

def parseBoard(s):
    lines = s.split("\n")[1:-1]
    lines = [ x.replace(' ', '') for x in lines ]
    print(lines)


    grid = []
    zones = collections.defaultdict( list)
    for i,line in enumerate(lines):
        grid.append([])
        for j,x  in enumerate(line):
            x = int(x)
            print( (i,j,x))
            zones[x].append( (i,j))
            grid[-1].append(x)
    return zones, grid
        


if __name__=='__main__':
    groups, grid = parseBoard(board)
    pp(groups)
    pp(grid)
    pl.clf()
    pl.imshow( np.array(y), extent = ( 0, len(grid[0]), 0, len(grid)))
