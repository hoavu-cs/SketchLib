import mmh3
import statistics
import math
import numpy as np
from copy import deepcopy

class F2Estimate():
    
    def __init__(self, epsilon=0.01, delta=0.01, hash_type="mmh3", seed=42):
        """ estimate the second frequency moment of a stream using the tug-of-war sketch.
        epsilon: relative error,
        delta: failure probability.
        """
        self._epsilon = epsilon
        self._delta = delta
        self._hash_type = hash_type
        self._seed = seed
        self._max_128_int = pow(2, 128) - 1
        self._c = 3  # Constant multiplier

        self._width = self._c * int(1 / (self._epsilon * self._epsilon))
        self._depth = self._c * int(math.log(1 / self._delta, 2))

        self._table = np.zeros((self._depth, self._width), dtype=int)
        self._seeds = np.array([[self._seed * i * j for j in range(self._width)] for i in range(self._depth)])

    def _hash(self, token, seed):
        """ Compute the {-1,+1} hash of a token.
        """
        if self._hash_type == "mmh3":
            x = mmh3.hash128(token, seed, signed=False) / self._max_128_int
            return -1 if x <= 0.5 else 1
        else:
            return 0

    def insert(self, x, y):
        """ Insert token x into the stream with weight y.
        """
        for i in range(self._depth):
            for j in range(self._width):
                self._table[i, j] += self._hash(x, self._seeds[i, j]) * y

    def merge(self, S):
        """ Merge with another F2 sketch S.
        Require that S has the same seed, eps, & delta.
        """
        self._table += S._table

    def __add__(self, S):
        """ Return the merged sketch of self and S
        """
        merged_sketch = deepcopy(self)
        merged_sketch.merge(S)
        return merged_sketch

    def estimator(self):
        """ Return the F2 estimator of the current stream.
        """
        avg = [statistics.mean(self._table[i]**2) for i in range(self._depth)]
        return statistics.median(avg)

    @classmethod
    def from_existing(cls, original):
        """ Creates a new sketch based on the parameters of an existing sketch.
        Two sketches are mergeable iff they share array size and hash seeds.
        Therefore, to create mergeable sketches, use an original to create new instances.
        """
        return F2Estimate(epsilon=original._epsilon, delta=original._delta, hash_type=original._hash_type, seed=original._seed)
