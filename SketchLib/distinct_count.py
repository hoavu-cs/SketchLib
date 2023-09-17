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

    def __init__(self, epsilon=0.01, delta=0.01, hash_type="mmh3", seed=42):
        self.epsilon = epsilon
        self.delta = delta
        self.hash_type = hash_type
        self.seed = seed
        self.max_128_int = pow(2, 128) - 1
        self.c = 2
        self.width = self.c * int((1 / self.epsilon) ** 2)
        self.depth = self.c * int(math.log(1 / self.delta, 2))
        self.seeds = [self.seed * i for i in range(self.depth)]
        self.table = [[] for _ in range(self.depth)]
        self.naive_lst = set()

    def _binary_search(self, a, x):
        i = bisect_left(a, x)
        return i if i != len(a) and a[i] == x else -1

    def _hash(self, token, seed):
        if self.hash_type == "mmh3":
            return mmh3.hash128(token, seed, signed=False) / self.max_128_int

    def _insert_into_table(self, i, hash_value):
        j = self._binary_search(self.table[i], hash_value)
        if j == -1:
            if len(self.table[i]) < self.width:
                insort(self.table[i], hash_value)
            elif self.table[i][-1] > hash_value:
                insort(self.table[i], hash_value)
                self.table[i].pop()

    def insert(self, token):
        if len(self.naive_lst) < self.width:
            self.naive_lst.add(token)

        for i, seed in enumerate(self.seeds):
            hash_value = self._hash(token, seed)
            self._insert_into_table(i, hash_value)

    def merge(self, S):
        self.naive_lst |= S.naive_lst
        self.naive_lst = set(list(self.naive_lst)[:self.width])

        for i in range(self.depth):
            for x in S.table[i]:
                self._insert_into_table(i, x)

    def estimator(self):
        if len(self.naive_lst) < self.width:
            return len(self.naive_lst)

        est = [int(self.width / row[-1]) for row in self.table]
        return int(statistics.median(est))

    @classmethod
    def from_existing(cls, original):
        return cls(epsilon=original.epsilon, delta=original.delta,\
             hash_type=original.hash_type, seed=original.seed)