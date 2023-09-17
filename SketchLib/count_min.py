from math import ceil, inf, pow, log
import mmh3
import numpy as np
from copy import deepcopy

class CountMin:
    max_128_int = pow(2, 128) - 1

    def __init__(self, phi=0.05, epsilon=0.2, delta=0.05, seed=10):
        self.epsilon = epsilon
        self.phi = phi
        self.delta = delta
        self.epsilon_star = self.phi * self.epsilon
        self.width = ceil(1/self.epsilon_star)
        self.depth = ceil(log(1/self.delta))
        self.table = np.zeros((self.depth, self.width), dtype=int)
        self._hash_seeds = np.array([i * i * seed for i in range(self.depth)], dtype=int)

    @classmethod
    def from_existing(cls, original_cm):
        """ Creates a new sketch based on the parameters of an existing sketch.
            Two sketches are mergeable iff they share array size and hash
            seeds. Therefore, to create mergeable sketches, use an original to
            create new instances. """
        new_cm = deepcopy(original_cm)
        new_cm.table = np.zeros((new_cm.depth, new_cm.width), dtype=int)
        return new_cm

    def _hash(self, token, seed):
        """ Compute the hash of a token. Converts hash value to a bin number
            based on k."""
        hash_value = mmh3.hash128(token, seed, signed=False) / self.max_128_int
        bin_number = int(hash_value * self.width)
        return bin_number

    def insert(self, token, count):
        for row in range(self.depth):
            col = self._hash(token, self._hash_seeds[row])
            self.table[row, col] += count

    def estimate_count(self, token):
        estimates = np.zeros(self.depth, dtype=int)
        for row in range(self.depth):
            col = self._hash(token, self._hash_seeds[row])
            estimates[row] = self.table[row, col]
        return estimates.min()

    def merge(self, other_count_min):
        self.table += other_count_min.table



