import random
import numpy as np
import matplotlib.pyplot as plt

# Some helpers often useful in defining experiments
def normalized(ps):
    return [p / sum(ps) for p in ps]

def Bern(p):
    return random.random() <= p

def Bin(n, p):
    return sum(Bern(p) for _ in range(n))

def RandomSign(p):
    return 2*int(Bern(p)) - 1

def Categ(categories, weights):
    return np.random.choice(categories, p=normalized(weights))

def indicator(value):
    return int(bool(value))

def probability_that(event_occurs, iters=10000):
    return expected_value_of(lambda: indicator(event_occurs()), iters)

def expected_value_of(random_variable, iters=10000):
    return np.mean([random_variable() for _ in range(iters)])

def is_greater_than(y): return lambda x: x > y
def is_less_than(y): return lambda x: x < y
def is_at_least(y): return lambda x: x >= y
def is_at_most(y): return lambda x: x <= y
def equals(y): return lambda x: x == y

# SampleSpace is a class that wraps a "Sample" (defining an experiment),
# and by repeatedly running that experiment lets you estimate event
# probabilities, optionally conditioned on attribute/function of the sample.
class SampleSpace():
    def __init__(self, experiment, iters=10000):
        self.experiment = experiment
        self.iters = iters

    def probability_that(self, event, given=[], iters=None):
        return self.probability_of(event, given=given, iters=iters)

    def probability_of(self, event, given=[], iters=None):
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
        return np.array(values)

    def expected_value_of(self, rv, given=[], iters=None):
        return np.mean(self.distribution_of(rv, given, iters))

    def variance_of(self, rv, given=[], iters=None):
        distribution = self.distribution_of(rv, given, iters)
        expected_val = np.mean(distribution)
        return np.mean([(val - expected_val)**2 for val in distribution])

    def standard_deviation_of(self, rv, given=[], iters=None):
        return np.sqrt(self.variance_of(rv, given, iters))

    def plot_distribution_of(self, rv, given=[], iters=None, **kwargs):
        distribution = self.distribution_of(rv, given, iters)
        E = np.mean(distribution)

        if 'bins' in kwargs and kwargs['bins'] == 'all':
            kwargs['bins'] = max(distribution) - min(distribution)
        if 'label' not in kwargs:
            kwargs['label'] = rv
        if len(given):
            plt.title('P({} = x|{})'.format(rv, ','.join(given)))
        else:
            plt.title('P({} = x)'.format(rv))

        plt.xlabel('x')
        plt.ylabel('p')
        hist = plt.hist(distribution, normed=True, **kwargs)
        plt.axvline(E, color='red', label='E={:.2f}'.format(E))
        return hist

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
