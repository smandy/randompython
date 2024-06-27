
#stryingrategy = [10] * 10


class Solver:
    def __init__(self, n):
        self.n = n
        self.attempts = []
        self.lastGood = None
        self.lastBad = None

    def survives(self, x):
        assert x>=1 and x <=100, f"Bad move {x}"
        ret =  x < self.n
        #print(f"{self.n} Trying {x} -> survives = {ret}")
        self.attempts.append(x)
        
        if ret:
            self.lastGood = x
        else:
            self.lastBad = x
        #self.report()
        return ret

    def report(self):
        print(f"{self.n} lastGood ={self.lastGood} lastBad={self.lastBad} attempts=({len(self.attempts)}) : {self.attempts}")        
    
    def solve(self, s):
        strategy = s[:]
        attempts = 0
        guess = 0

        lastGood = None
        lastBad = None
        # First torch
        while True:
            guess, strategy = strategy[0], strategy[1:]
            #guess += inc
            #print(f"Guess is {guess}")
            if not self.survives(guess):
                #print(f"breaking at {guess}")
                break
        

        #print("Linear scan")
        #guess = self.lastGood + 1
        while True:
            if not self.lastGood:
                guess = 1
            else:
                guess = self.lastGood + 1

            if guess == self.lastBad:
                break
            
            s = self.survives(guess)
            if not s:
                break

def sf(initial, inc, delta):
    ret = []
    x = initial
    while x<=100:
        ret.append(x)
        x += inc
        inc = max(1, inc -  delta)
    if ret[-1] != 100:
        ret.append(100)
        print(ret)
    return ret

def findMean(strategy):
    results = []
    r = {}
    for n in range(1, 101):
        #print(f"\n\n{n}")
        s = Solver(n)
        s.solve( strategy  )
        r[n] = s.attempts
        results.append(len(s.attempts))
        if 1:
            #print(f"\n\n{n}")                        
            s.report()
            
        assert s.lastBad == n
    ret = {np.mean(results)}
    print(f"{strategy} -> {ret}")
    return( (ret, min(results), max(results)))

if 0:
    findMean(sf(10,10,0))
