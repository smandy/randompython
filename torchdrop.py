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


def validStrategy(xs):
    for a, b in zip(xs[:-1], xs[1:]):
        if a >= b:
            return False
    if xs[-1] != 100:
        return False
    return True

def improve(bs):
    current = bs
    haveBest = False
    for idx in range(0, len(current.strategy) - 1):
        for perturbation in [-3, -2, -1, 1, 2, 3]:
            ns = bs.strategy[:]
            ns[idx] += perturbation
            if not validStrategy(ns):
                continue
            #print((idx, perturbation, ns))
            r = findMean(ns)
            if r.mean <= current.mean:
                haveBest = True
                current = r
    if haveBest:
        return current
    else:
        return None

def improve2(bs):
    current = bs
    haveBest = False
    for idx in range(0, len(current.strategy) - 2):
        for sign in [-3, -2, -1, 1, 2, -3]:
            ns = bs.strategy[:]
            #ns[idx] += perturbation
            ns[idx] += sign
            ns[idx + 1] -= sign

            if not validStrategy(ns):
                continue
            #print((idx, perturbation, ns))
            r = findMean(ns)
            if r.mean <= current.mean:
                haveBest = True
                current = r
    if haveBest:
        return current
    else:
        return None


def improveIterative(ns, improvers=[improve]):
    current = ns
    history = set([tuple(current.strategy)])
    haveBest = False
    while True:
        # print(f"Iter {current} ({len(history)} {history}")
        xs = [improver(current) for improver in improvers]
        xs = [x for x in xs if x and not tuple(x.strategy) in history]
        if not xs:
            break
        for x in xs:
            ts = tuple(x.strategy)
            if ts in history:
                continue
            else:
                if x.mean < current.mean or \
                   (x.mean <= current.mean and ts not in history):
                    history.add(ts)
                    #print(f"History {history}")
                    current = x
                haveBest = True
    if haveBest:
        return current
    else:
        return None

def findGap(bs):
    currentBest = bs
    haveBest = False
    # Try drop
    s = bs.strategy
    for idx in range(1, len(s) - 1):
        ns = findMean(s[:idx] + s[idx + 1:])
        m = improveIterative(ns, improvers=[improve, improve2])
        #print(f"ir m={m}")
        #print(f"findgap ns={ns} m={m}  currentBest={currentBest}")
        if m and m.mean <= currentBest.mean:
            currentBest = m
            haveBest = True
    if haveBest:
        return currentBest
    else:
        return None


def gaps(xs):
    return [xs[0]] + [x[1] - x[0] for x in zip(xs[:-1], xs[1:])]

def fromGaps(xs):
    ret = []
    count = 0
    for x in xs:
        count += x
        ret.append(count)
    return ret


naive = findMean([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
initial = findMean(sf(15, 15, 1))


#current = initial

bs2 = improveIterative(initial, improvers=[improve, improve2])
print(naive)
print(initial)
print(bs2)
#bs = improveIterative(initial)
#bs2 = improveIterative(bs, improver=improve2)
#bs3 = improveIterative(initial, improver=improve2)
#bs3 = improveIterative(bs2)

#print()
#print()
#fg = findGap(bs2)
#print(f"gap is {fg}")
