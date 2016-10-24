# Sample Space

...is a very lightweight Python API for simulating sample spaces, events, random variables, and (conditional) distributions.

## Example

Check out the [iPython notebook](./example.ipynb) or read the following:

```python
from sample_space import *

class NCoinTosses(Experiment):
    def __init__(self, n, p):
        self.n = n
        self.p = p

    def rerun(self):
        self.tosses = [Bern(self.p) for _ in range(self.n)]

    def heads(self):
        return sum(self.tosses)

    def there_are_at_least_two_heads(self):
        return self.heads() >= 2

    def first_toss_heads(self):
        return self.tosses[0]

space = SampleSpace(NCoinTosses(10, 0.5), iters=20000)

# ask for probability of any truthy method
print('        P(#H>=2):', space.probability_that('there_are_at_least_two_heads'))

# alias for the above, if it's more grammatical
print('           P(H1):', space.probability_of('first_toss_heads'))

# change the number of iterations
print(' P(H1), 1K iters:', space.probability_of('first_toss_heads', iters=1000))

# ask for probabilities of functions of random variables
print('         P(#H>5):', space.probability_that(['heads', is_greater_than(5)]))

# ask for conditional probabilities
print('      P(#H>5|H1):', space.probability_that(['heads', is_greater_than(5)], given=['first_toss_heads']))
print('      P(H1|#H>5):', space.probability_of('first_toss_heads', given=[['heads', is_greater_than(5)]]))
print(' P(#H>5|H1,H>=2):', space.probability_that(['heads', is_greater_than(5)],
    given=['first_toss_heads', 'there_are_at_least_two_heads']))

# ask for expectations, variances, and moments, conditionally or absolutely
print('           E(#H):', space.expected_value_of('heads'))
print('        E(#H|H1):', space.expected_value_of('heads', given=['first_toss_heads']))
print('         Var(#H):', space.variance_of('heads'))
print('      Var(#H|H1):', space.variance_of('heads', given=['first_toss_heads']))
print('1st moment of #H:', space.nth_moment_of('heads', 1))
print('2nd moment of #H:', space.nth_moment_of('heads', 2))
print('3rd moment of #H:', space.nth_moment_of('heads', 3))
print('4th moment of #H:', space.nth_moment_of('heads', 4))
print('  Skewness of #H:', space.nth_moment_of('heads', 3, central=True, normalized=True), '(using nth_moment_of w/ central=True, normalized=True)')
print('  Skewness of #H:', space.skewness_of('heads'), '(using skewness_of)')
print('  Kurtosis of #H:', space.kurtosis_of('heads'))

# some plots
fig = plt.figure(figsize=(14,3))

# plot distribution histograms
fig.add_subplot(121)
space.plot_distribution_of('heads') # pass kwargs
plt.legend()

# plot conditional distribution histograms
fig.add_subplot(122)
space.plot_distribution_of('heads', given=['first_toss_heads'], bins=10) # can pass kwargs
plt.legend()
plt.show()
```

Which should output (plus some plots):

```
        P(#H>=2): 0.98975
           P(H1): 0.502
 P(H1), 1K iters: 0.48
         P(#H>5): 0.37665
      P(#H>5|H1): 0.5076294006183305
      P(H1|#H>5): 0.6580109757729888
 P(#H>5|H1,H>=2): 0.49361831442463533
           E(#H): 4.9983
        E(#H|H1): 5.48924623116
         Var(#H): 2.4486457975
      Var(#H|H1): 2.31806506582
1st moment of #H: 4.99245
2nd moment of #H: 27.5097
3rd moment of #H: 163.13055
4th moment of #H: 1015.54155
  Skewness of #H: -0.00454435802967 (using nth_moment_of w/ central=True, normalized=True)
  Skewness of #H: 0.00414054522343 (using skewness_of)
  Kurtosis of #H: 2.78225928171
```

## Why?

Mostly to avoid bugs / reduce boilerplate in statistical simulations for sanity-checking homework solutions. But also to get a better understanding of probability theory.

[Sample spaces](https://en.wikipedia.org/wiki/Sample_space) are a core concept in probability theory. They encapsulate the idea of repeatedly running an experiment with random results. Almost every important statistical quantity -- the probability of an event, or any moment of a random variable -- is always defined relative to a sample space. So if you're trying to program meaningful simulations, you might as well organize your code by explicitly defining one.

## Installation / Usage

First run

```
pip install sample_space
```

and `import` the library. Then define a subclass of `Experiment` that responds to `rerun(self)`. `rerun` should perform a random experiment and store one or more basic results as instance variables. If you want to define more complex events or random variables, you can express them as instance methods.

Then, initialize a `SampleSpace` with an instance of your `Experiment`. You can query your sample space for the `probability_that`/`probability_of` an event, or you can query it for the `distribution_of`, `expected_value_of`, `variance_of`, `skewness_of`, `kurtosis_of`, or `nth_moment_of` of random variable (which can also just be an event, in which case it will be interpreted as an indicator). Finally, for any of these methods, you can pass a `given` keyword argument with a list of events, which will make any results you obtain conditional on all of those events occurring. Behind the scenes, `SampleSpace` will just `rerun` your experiment 10000 times and average your random variable or count how often an event occurs (conditionally). You can pass an `iters` keyword argument to any method or to `SampleSpace.__init__` to increase the number of iterations.

To reference events or random variable, pass the string name of an instance variable or instance method of your experiment, or pass an array with a variable/method name and a lambda function. For example:

```python
space = SampleSpace(CoinTossExperiment(10))
space.probability_that('first_toss_is_heads')
space.probability_that(['n_heads', lambda h: h > 5])
space.expected_value_of('n_heads')
space.expected_value_of('n_heads', given=['first_toss_is_heads'])
space.probability_that('first_toss_is_heads, given=[['n_heads', lambda h: h > 3], 'last_toss_is_heads'])
```

Additionally, `sample_space` defines a few helpful lambda-returning methods (`is_greater_than(x)`, `is_less_than(x)`, `is_at_least(x)`, `is_at_most(x)`, `equals(x)`) for convenience. Of course, you could also define instance methods on your `Experiment` to accomplish the same goal.

The library also exposes a few basic sampling functions (`Bern(p)`, `Bin(n,p)`, `RandomSign(p)`, and `Categ(categories, weights)`) to assist with defining experiments.

## Lite Version

If you'd prefer not to define a full `Experiment` class, you can also just define a random event / random variable function that returns either a boolean or a number, and call `probability_that`/`expected_value_of`:

```python
import sample_space as ss

def weighted_coin_flip_is_heads(p=0.4):
  return ss.Bern(p)

def n_weighted_heads(n=100, p=0.4):
  return sum(weighted_coin_flip_is_heads(p) for _ in range(n))

print(ss.probability_that(weighted_coin_flip_is_heads))
print(ss.probability_that(lambda: weighted_coin_flip_is_heads(0.5))
print(ss.expected_value_of(n_weighted_heads))
print(ss.expected_value_of(lambda: n_weighted_heads(200, 0.3)))
```

## License

[MIT](http://opensource.org/licenses/MIT)
