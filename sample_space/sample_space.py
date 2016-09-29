import numpy
import random
import matplotlib.pyplot

# Some helpers often useful in defining experiments
def normalized(ps):
    return [p / sum(ps) for p in ps]

def Bern(p):
    return random.random() <= p

def Bin(n, p):
    return sum(Bern(p) for _ in range(n))

def RandomSign(p):
    return 2*int(Bern(p)) - 1

def Categ(cats, ps):
    return numpy.random.choice(cats, p=normalized(ps))

# SampleSpace is a class that wraps a "Sample" (defining an experiment),
# and by repeatedly running that experiment lets you estimate event
# probabilities, optionally conditioned on attribute/function of the sample.
class SampleSpace():
    def __init__(self, experiment, iters=10000):
        self.experiment = experiment
        self.iters = iters

    def probability_that(self, event, given=[], iters=None):
        n_given = 0
        n_event = 0
        for _ in range(iters or self.iters):
            self.experiment.rerun()
            if all(self.experiment[g] for g in given):
                n_given += 1
                n_event += int(self.experiment[event])
        return n_event / n_given

    def distribution_of(self, rv, given=[], iters=None):
        values = []
        for _ in range(iters or self.iters):
            self.experiment.rerun()
            if all(self.experiment[g] for g in given):
                values.append(self.experiment[rv])
        return values

    def plot_distribution_of(self, rv, given=[], iters=None, bins=None):
        distribution = self.distribution_of(rv, given, iters)
        if len(given):
            matplotlib.pyplot.title('P({} = x|{})'.format(rv, ','.join(given)))
        else:
            matplotlib.pyplot.title('P({} = x)'.format(rv))
        matplotlib.pyplot.xlabel('x')
        matplotlib.pyplot.ylabel('p')
        matplotlib.pyplot.hist(distribution, normed=True, bins=bins)

# a bit of hackery to let you condition on sample attributes,
# instance methods, or external functions of either one.
class Experiment():
    def __getitem__(self, s):
        if isinstance(s, list):
            return s[1](self[s[0]])
        else:
            val = getattr(self, s)
            return val() if callable(val) else val

    def rerun(self):
        raise NotImplementedError("must define Experiment#rerun")
