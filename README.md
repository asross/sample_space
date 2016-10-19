# Sample Space

...is a very lightweight Python API for simulating sample spaces, events, random variables, and (conditional) distributions.

## Why?

Mostly to sanity-check statistics homework solutions, but also to wrap my head around random variables as functions mapping events to numbers and the subtleties of conditioning. It's probably not ideal for complex, high-performance simulations, but you might find its API convenient for simplifying small but tricky problems.

## Installation

```
pip install sample_space
```

## Usage

First, define a subclass of `Experiment` that responds to `rerun()`. `rerun` should perform some random experiment and store its results as instance variables. You can then define more complex events or random variables as functions of those instance variables.

Then, initialize a `SampleSpace` with an instance of your `Experiment`. You can now query the sample space for the `probability_of`, `distribution_of`, `expected_value_of`, or `variance_of` any random variable or event by passing the name of a function or attribute of your `Experiment`. You can also use a list/lambda syntax to ask similar questions about arbitrary functions of those rvs and events, or even plot histograms.

This library also exposes a few basic sampling functions (`Bern(p)`, `Bin(n,p)`, `RandomSign(p)`, and `Categ(categories, weights)`) to assist with defining experiments.

## Example

For a concrete example, check out the [iPython notebook example](./example.ipynb) (if you're reading this on Github), or read the following:

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
