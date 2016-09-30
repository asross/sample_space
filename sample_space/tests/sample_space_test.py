import unittest
from sample_space import *

class MontyHall(Experiment):
    def you_win_if_you_switch(self): return self.last_door == self.car_door
    def car_behind_door_1(self): return self.car_door == 1
    def door_2_was_opened(self): return self.open_door == 2
    def car_behind_door_3(self): return self.car_door == 3
    def rerun(self):
        self.car_door = Categ([1,2,3], [1/3., 1/3., 1/3.])
        if self.car_door == 3:
            self.open_door = Categ([1,2], [0.5, 0.5])
        else:
            self.open_door = { 1: 2, 2: 1 }[self.car_door]
        self.last_door = { 1: 2, 2: 1 }[self.open_door]

class TestSampleSpace(unittest.TestCase):
    def assertClose(self, p1, p2, tol=0.02):
        self.assertGreater(p1, p2-tol)
        self.assertLess(p1, p2+tol)

    def test_distributions(self):
        n_trials = 25000
        n_successes = Bin(n_trials, 0.5)
        p = n_successes / (1.*n_trials)
        self.assertClose(p, 0.5)

    def test_sample_space(self):
        mh = SampleSpace(MontyHall())
        self.assertClose(mh.probability_that('you_win_if_you_switch'), 2/3.)
        self.assertClose(mh.probability_that('you_win_if_you_switch',
            given=['car_behind_door_3']), 0)
        self.assertClose(mh.probability_that('door_2_was_opened',
            given=['car_behind_door_3']), 0.5)
        self.assertClose(mh.probability_that('car_behind_door_1',
            given=['you_win_if_you_switch']), 0.5)
        self.assertClose(mh.probability_that('door_2_was_opened',
            given=['you_win_if_you_switch']), 0.5)
        self.assertClose(mh.probability_that('door_2_was_opened',
            given=['car_behind_door_1']), 1)
