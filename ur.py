# Dice stats for royal game of ur


from collections import defaultdict

r = defaultdict(int)

for a in range(0,2):
    for b in range(0,2):
        for c in range(0,2):
            for d in range(0,2):
                r[a + b + c + d] += 1

xs = [ r[x] for x in range(0,5)]

for num, freq in enumerate(xs):
    print(f"{num} : {freq}")

"""
    
2s
    
xx--
x-x-
x--x
-xx-
-x-x
--xx

ones ( threes is just the inverse of this)

x---
-x--
--x-
---x

fours and zeros - trivial I guess


"""
