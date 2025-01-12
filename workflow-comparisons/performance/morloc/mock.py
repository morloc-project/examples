def pmock(x):
    if(len(x) <= 2):
        return x
    return x[-1] + x[0:-1] 

def pslurp(filename):
    with open(filename, "r") as fh:
        return fh.read()

def pnTimes(n, f, x):
    for _ in range(n):
        x = f(x)
    return x

def plength(x):
    return len(x)
