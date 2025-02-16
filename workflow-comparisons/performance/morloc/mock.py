import copy

def pmock(x):
    if(len(x) <= 2):
        return x
    y = copy.copy(x)
    temp = y[0]
    y[0] = y[-1]
    y[-1] = temp
    return y

def pslurp(filename):
    with open(filename, "rb") as fh:
        data = bytearray(fh.read())
    return data

def pnTimes(n, f, x):
    if(n == 0):
        return x
    for _ in range(n):
        x = f(x)
    return x
