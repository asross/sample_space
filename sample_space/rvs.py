import random
import numpy as np

def Unif(a, b):
    return a + random.random()*(b-a)

def Bern(p):
    return random.random() <= p

def Bin(n, p):
    return sum(Bern(p) for _ in range(n))

def RandomSign(p):
    return 2*int(Bern(p)) - 1

def normalized(ps):
    return [p / sum(ps) for p in ps]

def Categ(categories, weights):
    return np.random.choice(categories, p=normalized(weights))
