from math import ceil, inf, pow, log
import mmh3
import numpy as np
from copy import deepcopy

class CountMin:
    """ Count-Min Sketch """

    _max_128_int = pow(2, 128) - 1

    def __init__(self, phi=0.05, epsilon=0.2, delta=0.05, seed=10):
        self._epsilon = epsilon
        self._phi = phi
        self._delta = delta
        self._epsilon_star = self._phi * self._epsilon
        self._width = ceil(1 / self._epsilon_star)
        self._depth = ceil(log(1 / self._delta))
        self._table = np.zeros((self._depth, self._width), dtype=int)
        self._hash_seeds = np.array([i * i * seed for i in range(self._depth)], dtype=int)

    @classmethod
    def from_existing(cls, original_cm):
        """ Creates a new sketch based on the parameters of an existing sketch.
            Two sketches are mergeable iff they share array size and hash
            seeds. Therefore, to create mergeable sketches, use an original to
            create new instances. """
        new_cm = deepcopy(original_cm)
        new_cm._table = np.zeros((new_cm._depth, new_cm._width), dtype=int)
        return new_cm

    def _hash(self, token, seed):
        """ Compute the hash of a token. Converts hash value to a bin number
            based on k."""
        hash_value = mmh3.hash128(token, seed, signed=False) / CountMin._max_128_int
        bin_number = int(hash_value * self._width)
        return bin_number

    def insert(self, token, count):
        for row in range(self._depth):
            col = self._hash(token, self._hash_seeds[row])
            self._table[row, col] += count

    def estimate_count(self, token):
        estimates = np.zeros(self._depth, dtype=int)
        for row in range(self._depth):
            col = self._hash(token, self._hash_seeds[row])
            estimates[row] = self._table[row, col]
        return estimates.min()

    def merge(self, other_count_min):
        self._table += other_count_min._table
