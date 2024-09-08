import multiprocessing

def pmap(f, xs):
    with multiprocessing.Pool() as pool:
        results = pool.map(f, xs)
    return results

def nTimes(n, f, x):
    for _ in range(n):
        x = f(x)
    return x

def repeat(n, x):
    for _ in range(n):
        yield x

def noop(x):
    return None
