
def makeEnum( name,
              values ):
    def ex(self):
        raise RuntimeError('Not Instantiable. Use me statically!')
    d = {}
    valueOf = {}
    nameOf  = {}
    for i,x in enumerate(values):
        d[x] = i
        nameOf[i] = x
        valueOf[x] = i
    d['nameOf']   = nameOf
    d['valueOf']  = valueOf
    d['__init__'] = ex
    return type(name, (object,), d)

Side = makeEnum( 'Side', ['BUY','SELL'] )
TIF  = makeEnum( 'TIF' , ['DAY','IOC' ] )
