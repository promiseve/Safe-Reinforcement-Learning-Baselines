import unittest
import gym

import numpy as np

from agents.abs_opt_cmdp import AbsOptCMDPAgent
from util.mdp import monte_carlo_evaluation
from util.training import run_training_episodes

np.set_printoptions(precision=3, suppress=True)


def _solve(env, cost_bound, features=None, horizon=20, episodes=100):
    lp_agent = AbsOptCMDPAgent.from_discrete_env(env, features, cost_bound=cost_bound, horizon=horizon, verbose=False)
    run_training_episodes(lp_agent, env, number_of_episodes=episodes, horizon=horizon,
                          verbose=True, eval_episodes=10)
    expected_value, expected_cost, _, _ = monte_carlo_evaluation(env, lp_agent, horizon, number_of_episodes=30000,
                                                                 verbose=False)
    return expected_value, expected_cost


class TestAbsOptCMDP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = gym.make("gym_factored:chain2d-v0")

    def test_lp_agent_horizon_zero(self):
        expected_value, expected_cost = _solve(self.env, features=[0, 1], cost_bound=None, horizon=0)
        self.assertAlmostEqual(expected_value, 0, places=1)
        self.assertAlmostEqual(expected_cost, 0)

    def test_lp_agent_horizon_one(self):
        expected_value, expected_cost = _solve(self.env, features=[0, 1], cost_bound=None, horizon=1, episodes=3200)
        self.assertAlmostEqual(expected_value, 4.0, places=0)
        self.assertAlmostEqual(expected_cost, 1, places=1)

    def test_lp_agent_horizon_two(self):
        expected_value, expected_cost = _solve(self.env, features=[0, 1], cost_bound=None, horizon=2, episodes=3200)
        self.assertAlmostEqual(expected_value, 8.25, places=1)
        self.assertAlmostEqual(expected_cost, 1.75, places=1)

    def test_lp_agent_unbounded(self):
        expected_value, expected_cost = _solve(self.env, features=[0, 1], cost_bound=None, horizon=3)
        self.assertAlmostEqual(expected_value, 10, places=1)
        self.assertAlmostEqual(expected_cost, 2)

    def test_lp_agent_bounded(self):
        expected_value, expected_cost = _solve(self.env, features=[0, 1], cost_bound=0, horizon=3)
        self.assertAlmostEqual(expected_value, 1, places=1)
        self.assertAlmostEqual(expected_cost, 0, places=1)


class TestAbsOptCMDPCMDP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = gym.make("gym_factored:cmdp-v0")

    def test_lp_agent_unbounded(self):
        expected_value, expected_cost = _solve(self.env, features=[], cost_bound=None, horizon=6, episodes=30)
        self.assertAlmostEqual(expected_value, 12, places=1)
        self.assertAlmostEqual(expected_cost, 6, places=1)

    def test_lp_agent_bounded_0(self):
        expected_value, expected_cost = _solve(self.env, features=[], cost_bound=0, horizon=6, episodes=30)
        self.assertAlmostEqual(expected_value, 0, places=1)
        self.assertAlmostEqual(expected_cost, 0, places=1)

    def test_lp_agent_bounded_3(self):
        expected_value, expected_cost = _solve(self.env, features=[], cost_bound=3, horizon=6)
        self.assertAlmostEqual(expected_cost, 3, places=1)
        self.assertAlmostEqual(expected_value, 6.66, places=0)
