# Sample Space

...is a very lightweight Python API for simulating sample spaces, events, random variables, and conditional probabilities.

## Why?

Mostly to help sanity-check my statistics homework solutions, but writing this helped me think about random variables as functions mapping from events in a sample space to points in R^n, and about what it means to condition. It's probably not ideal for complex, high-performance simulations, but you might find its API convenient for sanity-checking simple problems!

## Installation

```
pip install sample_space
```

## Usage

First, define a subclass of `sample_space.Experiment` that responds to `rerun()`. Re-run should perform some random experiment and set instance variables to its results. You can also define functions of those results (such as composing them to form more complex events, or computing values of random variables).

Then, initialize a `sample_space.SampleSpace` with an instance of an `Experiment`. You can now query the sample space for the probabilities of your experiment's events, using the names of experiment variables, methods, or even arbitrary functions of them you pass along in an array. You can make this query conditional, too.

Finally, you can also use `SampleSpace` to generate a sample of the distribution of a random variable of the experiment, and plot a histogram.

This library also exposes a few basic functions (`Bern(p)`, `Bin(n,p)`, `RandomSign(p)`, and `Categ(categories, weights)`) to assist with defining experiments.

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
print(space.probability_that('there_are_at_least_two_heads'))

# alias for the above, if it's more grammatical
print(space.probability_of('first_toss_heads'))

# change the number of iterations
print(space.probability_of('first_toss_heads', iters=1000))

# ask for probabilities of functions of random variables
print(space.probability_that(['heads', is_greater_than(5)]))

# ask for conditional probabilities
print(space.probability_that(['heads', is_greater_than(5)], given=['first_toss_heads']))
print(space.probability_of('first_toss_heads', given=[['heads', is_greater_than(5)]]))
print(space.probability_that(['heads', is_greater_than(5)],
    given=['first_toss_heads', 'there_are_at_least_two_heads']))

# ask for expectations and variances, conditionally or absolutely
print(space.expected_value_of('heads'))
print(space.expected_value_of('heads', given=['first_toss_heads']))
print(space.variance_of('heads'))
print(space.variance_of('heads', given=['first_toss_heads']))

# some plots
fig = plt.figure(figsize=(14,3))

# plot distribution histograms
fig.add_subplot(121)
space.plot_distribution_of('heads') # pass kwargs

# plot conditional distribution histograms
fig.add_subplot(122)
space.plot_distribution_of('heads', given=['first_toss_heads'], bins=10) # can pass kwargs

plt.show()
```

## Lite Version

You can also just define a random event / random variable function that returns either a boolean or a number, and call `probability_that` and `expected_value_of` without defining a full `SampleSpace`:

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
