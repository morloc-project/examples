import random

def choose(xs):
    return random.choice(xs)

def roll(n, d):
    return [random.randint(1, d) for _ in range(n)] 

def coin_toss():
    return bool(random.randint(0,1))
