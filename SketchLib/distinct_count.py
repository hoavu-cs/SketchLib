from abc import abstractmethod
import mmh3
import math
from bisect import bisect_left, insort
import statistics
from copy import deepcopy 
import numpy as np

class AbstractDistinctCount:
    @abstractmethod
    def insert(self, token):
        pass
    
    @abstractmethod
    def merge(self, another_sketch):
        pass
        
    @abstractmethod
    def estimator(self):
        pass

    @abstractmethod
    def from_existing(cls, original):
        pass

    def __add__(self, S):
        merged_sketch = deepcopy(self)
        merged_sketch.merge(S)
        return merged_sketch

# --------------------------------------------------------------------------

class LogDistinctCount(AbstractDistinctCount):
    """ This class solves the distinct count problem using a log sketch.
    This folows the basic idea of Fjarolet and Martin's algorithm.
    We however maintain the lowest 1/eps hash values instead of the lowest as
    suggested in Bar-Yossef et al. (2002) to have a faster update time.
    """

    _max_128_int = pow(2, 128) - 1

    def __init__(self, epsilon=0.01, delta=0.01, hash_type="mmh3", seed=42):
        self._epsilon = epsilon
        self._delta = delta
        self._hash_type = hash_type
        self._seed = seed
        self._c = 2
        self._width = self._c * int((1 / self._epsilon) ** 2)
        self._depth = self._c * int(math.log(1 / self._delta, 2))
        self._seeds = [self._seed * i for i in range(self._depth)]
        self._table = [[] for _ in range(self._depth)]
        self._naive_lst = set()

    def _binary_search(self, a, x):
        i = bisect_left(a, x)
        return i if i != len(a) and a[i] == x else -1

    def _hash(self, token, seed):
        if self._hash_type == "mmh3":
            return mmh3.hash128(token, seed, signed=False) / LogDistinctCount._max_128_int

    def _insert_into_table(self, i, hash_value):
        """ 
        Insert a hash value into the i-th row of the table while maintaining the sorted order.
        """
        j = self._binary_search(self._table[i], hash_value)
        if j == -1:
            if len(self._table[i]) < self._width:
                insort(self._table[i], hash_value)
            elif self._table[i][-1] > hash_value:
                insort(self._table[i], hash_value)
                self._table[i].pop()

    def insert(self, token):
        """ Insert a token into the sketch. """
        if len(self._naive_lst) < self._width:
            self._naive_lst.add(token)

        for i, seed in enumerate(self._seeds):
            hash_value = self._hash(token, seed)
            self._insert_into_table(i, hash_value)

    def merge(self, S):
        """ Merge S with self. """
        self._naive_lst |= S._naive_lst
        self._naive_lst = set(list(self._naive_lst)[:self._width])

        for i in range(self._depth):
            for x in S._table[i]:
                self._insert_into_table(i, x)

    def estimator(self):
        """ Estimate the number of distinct elements in the stream so far. """
        if len(self._naive_lst) < self._width:
            return len(self._naive_lst)

        est = [int(self._width / row[-1]) for row in self._table]
        return int(statistics.median(est))

    @classmethod
    def from_existing(cls, original):
        return cls(epsilon=original._epsilon, delta=original._delta,\
             hash_type=original._hash_type, seed=original._seed)