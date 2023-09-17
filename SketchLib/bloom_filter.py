import mmh3
import math
import numpy as np

class BloomFilter:
    """
    Bloom Filter
    """
    def __init__(self, n=10000, delta=0.01, seed=42):
        """ n: the maximum number of insertions
            delta: false positive rate
        """
        self.n = n
        self.delta = delta
        self.seed = seed

        self.m = math.ceil(n * math.log2(1 / delta) / math.log(2))
        self.k = math.ceil(math.log(1 / delta))
        self.max_128_int = pow(2, 128) - 1
        self.B = np.zeros(self.m, dtype=int)
        self.m_minus_one = self.m - 1
        self.seeds = np.arange(self.k) * seed

    def _hash(self, token, seed):
        x = mmh3.hash128(token, seed, signed=False) / self.max_128_int
        return int(x * self.m_minus_one)

    def delete(self, x):
        """Delete x from the data structure."""
        self.B[[self._hash(x, seed) for seed in self.seeds]] -= 1

    def insert(self, x):
        """Insert x to the data structure."""
        self.B[[self._hash(x, seed) for seed in self.seeds]] += 1

    def membership(self, x):
        """Check if x is in the data structure."""
        return all(self.B[self._hash(x, seed)] != 0 for seed in self.seeds)

    def merge(self, S):
        """Combine self with Bloom filter S to obtain a new Bloom filter."""
        self.B += S.B

    def __add__(self, S):
        """Return the merged Bloom filter of self and S."""
        merged_filter = self.from_existing(self)
        merged_filter.B += self.B
        merged_filter.B += S.B
        return merged_filter

    @classmethod
    def from_existing(cls, original):
        """Create a new Bloom Filter based on an existing one."""
        return cls(n=original.n, delta=original.delta, seed=original.seed)
