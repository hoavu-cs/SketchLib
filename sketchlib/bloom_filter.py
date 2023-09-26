import mmh3
import math
import numpy as np

class BloomFilter:
    """ Implements a Bloom Filter for approximate set membership queries. """

    # Class-level constant for 128-bit maximum integer
    _max_128_int = pow(2, 128) - 1

    def __init__(self, n=10000, delta=0.01, seed=42):
        """ 
        Initialize a Bloom Filter.
        n: Maximum number of elements to be inserted.
        delta: Desired false positive rate.
        seed: Seed for hash functions.
        """
        self._n = n
        self._delta = delta
        self._seed = seed

        # Calculate size of the bit array (m) and the number of hash functions (k)
        self._m = math.ceil(n * math.log2(1 / delta) / math.log(2))
        self._k = math.ceil(math.log(1 / delta))
        
        # Initialize bit array
        self._B = np.zeros(self._m, dtype=int)
        self._m_minus_one = self._m - 1
        
        # Initialize seeds for hash functions
        self._seeds = np.arange(self._k) * seed

    def _hash(self, token, seed):
        """ 
        Compute the hash of a token using the given seed.
        Maps the hash value to an index in the bit array.
        """
        x = mmh3.hash128(token, seed, signed=False) / BloomFilter._max_128_int
        return int(x * self._m_minus_one)

    def delete(self, x):
        """ Delete an element from the Bloom filter. """
        self._B[[self._hash(x, seed) for seed in self._seeds]] -= 1

    def insert(self, x):
        """ Insert an element into the Bloom filter. """
        self._B[[self._hash(x, seed) for seed in self._seeds]] += 1

    def membership(self, x):
        """ 
        Check if an element is likely to be in the set.
        Note: There can be false positives.
        """
        return all(self._B[self._hash(x, seed)] != 0 for seed in self._seeds)

    def merge(self, S):
        """ Merge this Bloom filter with another one. """
        self._B += S._B

    def __add__(self, S):
        """ Return a new Bloom filter that is a merge of self and S. """
        merged_filter = self.from_existing(self)
        merged_filter._B += self._B
        merged_filter._B += S._B
        return merged_filter

    def get_filter(self):
        """ Return the current state of the filter. """
        return self._B

    @classmethod
    def from_existing(cls, original):
        """ Create a new Bloom filter based on the parameters of an existing one. """
        return cls(n=original._n, delta=original._delta, seed=original._seed)
