

class memoize:
    def __init__(self, f):
        self.f = f
        self.d = {}

    def __call__(self, *args):
        t = tuple(args)
        if self.d.has_key( t ):
            print "Cache"
            ret = self.d[t]
        else:
            ret = self.f( *args )
            self.d[t] = ret
        return ret

if __name__=='__main__':
    @memoize
    def add(a,b):
        return a + b


            
