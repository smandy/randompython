x = 1.5

while True:
    newX = x/2.0 + 1 / x
    print(f"new={newX:4f} old={x:4f} diff={newX-x}")
    if newX == x:
        break
    x = newX
