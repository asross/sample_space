import matplotlib.pyplot as plt
import numpy as np
from .lambdas import *
from .rvs import *

def indicator(value):
    return int(bool(value))

def rv_name(g):
    if isinstance(g, list):
        val, fn = g
        return '{} {}'.format(val, fn.__name__)
    else:
        return g

def probability_that(event_occurs, iters=10000):
    return expected_value_of(lambda: indicator(event_occurs()), iters)

def expected_value_of(random_variable, iters=10000):
    return np.mean([random_variable() for _ in range(iters)])

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
        return np.array(values, dtype=np.float64)

    def joint_distribution_of(self, rvs, given=[], iters=None):
        values = []
        for _ in range(iters or self.iters):
            self.experiment.rerun()
            if all(self.experiment[g] for g in given):
                values.append([self.experiment[rv] for rv in rvs])
        return np.array(values, dtype=np.float64)

    def expected_value_of(self, rv, given=[], iters=None):
        return np.mean(self.distribution_of(rv, given, iters))
    mean = expected_value_of

    def variance_of(self, rv, given=[], iters=None):
        distribution = self.distribution_of(rv, given, iters)
        mean = np.mean(distribution)
        return np.mean((distribution - mean)**2)
    var = variance_of

    def standard_deviation_of(self, rv, given=[], iters=None):
        return np.sqrt(self.variance_of(rv, given, iters))
    std = standard_deviation_of

    def nth_moment_of(self, rv, n, given=[], iters=None, central=False, normalized=False):
        distribution = self.distribution_of(rv, given, iters)
        if central:
            mean = np.mean(distribution)
            distribution -= mean
            if normalized:
                variance = np.mean(distribution**2)
                distribution /= np.sqrt(variance)
        elif normalized:
            raise ValueError('should only pass normalized=True if central=True')
        return np.mean(distribution**n)

    def skewness_of(self, rv, given=[], iters=None):
        return self.nth_moment_of(rv, 3, given, iters, central=True, normalized=True)

    def kurtosis_of(self, rv, given=[], iters=None):
        return self.nth_moment_of(rv, 4, given, iters, central=True, normalized=True)

    def plot_distribution_of(self, rv, given=[], iters=None, **kwargs):
        distribution = self.distribution_of(rv, given, iters)
        E = np.mean(distribution)

        if 'bins' in kwargs and kwargs['bins'] == 'all':
            kwargs['bins'] = max(distribution) - min(distribution)
        if 'label' not in kwargs:
            kwargs['label'] = rv_name(rv)
        if len(given):
            plt.title('P({} = x|{})'.format(rv, ','.join([rv_name(g) for g in given])))
        else:
            plt.title('P({} = x)'.format(rv))

        plt.xlabel('x')
        plt.ylabel('p')
        norm_weights = np.ones_like(distribution)/float(len(distribution))
        hist = plt.hist(distribution, weights=norm_weights, **kwargs)
        plt.axvline(E, color='red', label='E={:.2f}'.format(E))
        return hist

    def plot_joint_distribution_of(self, rvs, given=[], iters=None, **kwargs):
        assert(len(rvs) == 2)
        distribution = self.joint_distribution_of(rvs, given, iters)
        if given:
            plt.title('P({}=x,{}=y|{}'.format(rvs[0], rvs[1], ','.join([given_name(g) for g in given])))
        else:
            plt.title('P({}=x,{}=y)'.format(rvs[0], rvs[1]))
        plt.xlabel('x')
        plt.ylabel('y')
        hist = plt.hist2d(distribution[:,0], distribution[:,1], normed=True, **kwargs)
        plt.colorbar()
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
