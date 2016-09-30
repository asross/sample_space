# Sample Space

...is a very lightweight Python API for simulating sample spaces, events, random variables, and conditional probabilities.

## Why?

Writing this helped me think about random variables as functions mapping from events in a sample space to points in R^n, and about what it means to condition. It's also useful for checking answers / visualizing statistics problems!

## Usage

You can check out the [iPython notebook example](./example.ipynb) (link may only work on Github), or see the code here:

```python
import sample_space
import matplotlib.pyplot as plt

class NCoinTosses(sample_space.Experiment):
    def __init__(self, n, p):
        self.n = n
        self.p = p

    def rerun(self):
        self.tosses = [sample_space.Bern(self.p) for _ in range(self.n)]

    def heads(self):
        return sum(self.tosses)

    def there_are_at_least_two_heads(self):
        return self.heads() >= 2

    def first_toss_heads(self):
        return self.tosses[0]

space = sample_space.SampleSpace(NCoinTosses(10, 0.5), iters=20000)

# ask for probability of any truthy method
print(space.probability_that('there_are_at_least_two_heads'))

# alias for the above, if it's more grammatical
print(space.probability_of('first_toss_heads'))

# change the number of iterations
print(space.probability_of('first_toss_heads', iters=1000))

# ask for probabilities of functions of random variables
def gt(x): return lambda y: y > x
print(space.probability_that(['heads', gt(5)]))

# ask for conditional probabilities
print(space.probability_that(['heads', gt(5)], given=['first_toss_heads']))
print(space.probability_of('first_toss_heads', given=[['heads', gt(5)]]))
print(space.probability_that(['heads', gt(5)],
    given=['first_toss_heads', 'there_are_at_least_two_heads']))

# some plots
fig = plt.figure(figsize=(14,3))

# plot distribution histograms
fig.add_subplot(121)
space.plot_distribution_of('heads') # pass kwargs

# plot conditional distribution histograms (and pass kwargs)
fig.add_subplot(122)
space.plot_distribution_of('heads', given=['first_toss_heads'], bins=10)

plt.show()
```
