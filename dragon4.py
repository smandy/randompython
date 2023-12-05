from functools import partial
from itertools import cycle, product

def drawLSystem(prev,
                rules,
                renderFactory,
                sz,
                scaleFact,
                order,
                f,
                l,
                r):
    if order==0:
        d = renderFactory(f, l, r, sz)
        for x in prev:
            d[x]()
    else:
        nextGen = ''
        for x in prev:
            nextGen += rules[x]
        drawLSystem( nextGen,
                     rules,
                     renderFactory ,
                     sz * scaleFact,
                     scaleFact,
                     order - 1,
                     f,
                     l,
                     r)
    
if __name__=='__main__':
    rules = {
        'A' : '+B-A-B+',
        'B' : '-A+B+A-',
        '+' : '+',
        '-' : '-'
    }
    def renderFactory(f, l, r, sz):
        return {
            'A' : partial( f, sz),
            'B' : partial( f, sz),
            '+' : partial( l, 60),
            '-' : partial( r, 60)
        }
    seed = 'A'
    import turtle as tt
    COLORS = ['red','green','blue','purple', 'magenta']
    SIZE = 150
    SCALEFACT = 1.0/2
    tt.reset()
    tt.speed(0)
    for order , (color, pos)  in enumerate(zip(cycle(COLORS),
                                               product([-300, -100, 100],
                                                       [160,-40, -240],
                                               ) )):
        tt.penup()
        tt.setposition(*pos)
        tt.pendown()
        tt.color(color)
        drawLSystem(seed, rules, renderFactory, SIZE, SCALEFACT, order, tt.forward, tt.left, tt.right)
        

        
