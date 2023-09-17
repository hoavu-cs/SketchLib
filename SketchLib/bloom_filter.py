import mmh3
import math
import numpy as np

class BloomFilter:
    """ Bloom Filter """

    _max_128_int = pow(2, 128) - 1

    def __init__(self, n=10000, delta=0.01, seed=42):
        """ n: the maximum number of insertions
            delta: false positive rate
        """
        self._n = n
        self._delta = delta
        self._seed = seed
        self._m = math.ceil(n * math.log2(1 / delta) / math.log(2))
        self._k = math.ceil(math.log(1 / delta))
        self._B = np.zeros(self._m, dtype=int)
        self._m_minus_one = self._m - 1
        self._seeds = np.arange(self._k) * seed

    def _hash(self, token, seed):
        x = mmh3.hash128(token, seed, signed=False) / BloomFilter._max_128_int
        return int(x * self._m_minus_one)

    def delete(self, x):
        """ Delete x from the data structure."""
        self._B[[self._hash(x, seed) for seed in self._seeds]] -= 1

    def insert(self, x):
        """ Insert x to the data structure."""
        self._B[[self._hash(x, seed) for seed in self._seeds]] += 1

    def membership(self, x):
        """ Check if x is in the data structure."""
        return all(self._B[self._hash(x, seed)] != 0 for seed in self._seeds)

    def merge(self, S):
        """ Combine self with Bloom filter S to obtain a new Bloom filter."""
        self._B += S._B

    def __add__(self, S):
        """ Return the merged Bloom filter of self and S."""
        merged_filter = self.from_existing(self)
        merged_filter._B += self._B
        merged_filter._B += S._B
        return merged_filter

    def get_filter(self):
        """ Return the filter."""
        return self._B

    @classmethod
    def from_existing(cls, original):
        "" "Create a new Bloom Filter based on an existing one. """
        return cls(n=original._n, delta=original._delta, seed=original._seed)
