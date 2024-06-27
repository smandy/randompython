
#stryingrategy = [10] * 10


from dataclass import dataclass
import numpy as np

@dataclass
class Result:
    strategy: list[int]
    min: float
    max: float
    mean: float


class Solver:
    def __init__(self, n):
        self.n = n
        self.attempts = []
        self.lastGood = None
        self.lastBad = None

    def survives(self, x):
        assert x >= 1 and x <= 100, f"Bad move {x}"
        ret = x < self.n
        #print(f"{self.n} Trying {x} -> survives = {ret}")
        self.attempts.append(x)

        if ret:
            self.lastGood = x
        else:
            self.lastBad = x
        #self.report()
        return ret

    def report(self):
        print(f"{self.n} lastGood ={self.lastGood} lastBad={self.lastBad} "
              f"attempts=({len(self.attempts)}) : {self.attempts}")

    def solve(self, s):
        strategy = s[:]
        guess = 0

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
    while x <= 100:
        ret.append(x)
        x += inc
        inc = max(1, inc - delta)
    if ret[-1] != 100:
        ret.append(100)
        #print(ret)
    return ret

def findMean(strategy, verbose=False):
    results = []
    r = {}
    for n in range(1, 101):
        #print(f"\n\n{n}")
        s = Solver(n)
        s.solve(strategy)
        r[n] = s.attempts
        results.append(len(s.attempts))
        if verbose:
            s.report()

        assert s.lastBad == n
    #ret = (np.mean(results), min(results), max(results))
    ret = Result(strategy, min(results), max(results), np.mean(results))
    if verbose:
        print(ret)
    return ret


best = findMean(sf(15, 15, 1))

#m = findMean(bs)[0]
#import random
#bs = sf(15,15,1)



def improve(bs, inner=False):
    current = bs
    haveBest = False
    for idx in range(0, len(current.strategy) - 1):
        for perturbation in [-1, 1]:
            #print((idx, perturbation,))
            ns = bs.strategy[:]
            ns[idx] += perturbation
            r = findMean(ns)
            if r.mean < current.mean:
                haveBest = True
                current = r
    if haveBest:
        return current
    else:
        return None

def improveIterative(ns):
    current = ns
    haveBest = False
    while True:
        xs = improve(current)
        if not xs:
            break
        else:
            if xs.mean < current.mean:
                current = xs
                haveBest = True
    if haveBest:
        return current
    else:
        return None

def findGap(bs):
    currentBest = bs
    haveBest = False
    #print(f"findgap bs={bs} allBest={allBest}")
    # Try drop
    s = bs.strategy
    for idx in range(1, len(s) - 1):
        ns = findMean(s[:idx] + s[idx + 1:])
        m = improveIterative(ns)
        #print(f"ir m={m}")
        if m and m.mean < currentBest.mean:
            currentBest = m
            haveBest = True
    if haveBest:
        return currentBest
    else:
        return None


bs = findMean(sf(15, 15, 1))
bs = improveIterative(bs)

print()
print()
fg = findGap(bs)
print(f"gap is {fg}")
