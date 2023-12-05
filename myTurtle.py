def outerpose(y, xs):
    "Based on clojure's 'interpose' : outerpose( a, [1,2,3] ) -> [a,1,a,2,a,3,a] )"
    for x in xs:
        yield y
        yield x
    yield y

def noop():
    pass

def drawSegment(sz, order, forward, l, r, y, d):
    if order==0:
        forward(sz)
    else:
        newSize = sz / 3.0
        drawSegmentCommandTyle = (drawSegment,
                                   (newSize,order - 1,
                                    forward, l, r, y, d) )
        directionChangeCommandTyles = [
            (l ,  (  60,) ),
            (r , ( 120,) ),
            (l ,  (  60,) )
            ]
        directionChangeCommandTyles2 = [
            (r ,  (  60,) ),
            (l  ,  ( 120,) ),
            (r ,  (  60,) )
            ]
        for (meth, args) in outerpose(drawSegmentCommandTyle,
                                      directionChangeCommandTyles):
            meth(*args)
        if 0:
            y()
            forward(-sz)
            d()
            for (meth, args) in outerpose(drawSegmentCommandTyle,
                                          directionChangeCommandTyles2):
                meth(*args)
            
def drawSnowflake( sz, order, forward, l, r, y, d):
    for i in range(3):
        drawSegment(sz, order, forward, l, r, y, d)
        r(120)
        
if __name__=='__main__':
    if 1:
        import turtle as tt
        COLORS = ['red','green','blue','purple', 'magenta']
        SIZE = 180.0
        def getPositions(ys = [200,-50],
                         xs = [-300, -100, 100]):
            for y in ys:
                for x in xs:
                    yield (x,y)
        tt.reset()
        tt.speed(0)
        for order , (color, pos)  in enumerate(zip(COLORS, getPositions() )):
            tt.penup()
            tt.setposition(*pos)
            tt.pendown()
            tt.color(color)
            drawSnowflake(SIZE, order, tt.forward, tt.left, tt.right, tt.penup, tt.pendown)
    else:
        cur = []
        def makeMove(prefix):
            def ret(x):
                cur.append( (prefix, x))
            return ret
        forward, l, r = [ makeMove(x) for x in ['F','L','R'] ]
        drawSnowflake(200.0, 5, forward, l, r, noop, noop)
