import mmh3
import statistics
import math
import numpy as np
from copy import deepcopy

class F2Estimate():
    """ 
    This is the tug-of-war sketch for estimating the second frequency moment of a stream 
    proposed by Alon et al. 2000.
    """
    
    # Class-level constant for 128-bit maximum integer
    _max_128_int = pow(2, 128) - 1
    
    def __init__(self, epsilon=0.01, delta=0.01, seed=42):
        """ 
        Initialize an F2Estimate instance.
        epsilon: relative error,
        delta: failure probability,
        seed: seed for hash function.
        """
        
        self._epsilon = epsilon
        self._delta = delta
        self._seed = seed
        self._c = 3  # Constant multiplier to increase table width and depth

        # Calculate the table dimensions
        self._width = self._c * int(1 / (self._epsilon * self._epsilon))
        self._depth = self._c * int(math.log(1 / self._delta, 2))

        # Initialize hash table and seeds
        self._table = np.zeros((self._depth, self._width), dtype=int)
        self._seeds = np.array([[self._seed * i * j for j in range(self._width)] for i in range(self._depth)])

    def _hash(self, token, seed):
        """ Compute the {-1,+1} hash of a token based on the seed. """
        x = mmh3.hash128(token, seed, signed=False) / F2Estimate._max_128_int
        return -1 if x <= 0.5 else 1

    def insert(self, x, y):
        """ Insert token x into the stream with weight y. """
        for i in range(self._depth):
            for j in range(self._width):
                self._table[i, j] += self._hash(x, self._seeds[i, j]) * y

    def merge(self, S):
        """ Merge this F2Estimate instance with another one, S. """
        self._table += S._table

    def __add__(self, S):
        """ Return the merged sketch of self and S using Python's addition operator. """
        merged_sketch = deepcopy(self)
        merged_sketch.merge(S)
        return merged_sketch

    def estimator(self):
        """ Return the F2 estimator of the current stream. """
        avg = [statistics.mean(self._table[i]**2) for i in range(self._depth)]
        return statistics.median(avg)

    @classmethod
    def from_existing(cls, original):
        """ Create a new F2Estimate instance based on the parameters of an existing one. """
        return F2Estimate(epsilon=original._epsilon, delta=original._delta, seed=original._seed)
