def is_greater_than(y):
    f = lambda x: x > y
    f.__name__ = '> {}'.format(y)
    return f

def is_less_than(y):
    f = lambda x: x < y
    f.__name__ = '< {}'.format(y)
    return f

def is_at_least(y):
    f = lambda x: x >= y
    f.__name__ = '>= {}'.format(y)
    return f

def is_at_most(y):
    f = lambda x: x <= y
    f.__name__ = '<= {}'.format(y)
    return f

def is_between(a,b):
    f = lambda x: a <= x <= b
    f.__name__ = 'in [{},{}]'.format(a,b)
    return f

def is_approximately(y, tol=0.1):
    f = lambda x: y-tol <= x <= y+tol
    f.__name__ = '≈ {}'.format(y)
    return f

def equals(y):
    f = lambda x: x == y
    f.__name__ = '= {}'.format(y)
    return f
