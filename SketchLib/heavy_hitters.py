from sketchlib.count_min import CountMin
from heapq import heappush, heappop, heapify
from math import ceil
from abc import abstractmethod
from copy import deepcopy


class AbstractHeavyHitters:
    @abstractmethod
    def insert(self, token, count):
        pass

    @abstractmethod
    def get_heavy_hitters(self):
        pass

    @abstractmethod
    def merge(self, other_finder):
        pass

    @abstractmethod
    def from_existing(self, original):
        pass

    def __add__(self, other):
        merged_sketch = deepcopy(self)
        merged_sketch.merge(other)
        return merged_sketch

# --------------------------------------------------------------------------

class CountMinCashRegister(AbstractHeavyHitters):
    """ This class solves the heavy hitters problem using a count-min data
        structure. It works only for the cash register model of a stream where
        each token count must be greater than 0 (c > 0). """
        
    def __init__(self, phi=0.05, epsilon=0.2, delta=0.01, seed=42):
        self._init_params(phi, epsilon, delta, seed)
        self._l1_norm = 0
        self._min_heap = []

    def _init_params(self, phi, epsilon, delta, seed):
        """ Initialize parameters and create a CountMin object. """
        self._phi = phi
        self._epsilon = epsilon
        self._delta = delta
        self._seed = seed
        self._count_min = CountMin(phi=phi, epsilon=epsilon, delta=delta, seed=seed)

    def insert(self, token, count):
        """ Insert a token into the count-min sketch and update the heap of heavy hitters. """
        self.update_l1_norm(count)
        self.update_heap(token, count)

    def update_l1_norm(self, count):
        """ Update the l1_norm based on the incoming count. """
        self._l1_norm += count

    def update_heap(self, token, count):
        """ Update the min heap based on the newly inserted token. """
        cutoff = self._phi * self._l1_norm
        self._count_min.insert(str(token), count)
        point_query = self._count_min.estimate_count(token)
        if point_query >= cutoff:
            heappush(self._min_heap, (point_query, token))
        
        self.remove_below_cutoff(cutoff)

    def remove_below_cutoff(self, cutoff):
        """ Remove tokens from the heap that are below the cutoff. """
        while self._min_heap and self._min_heap[0][0] < cutoff:
            heappop(self._min_heap)

    def get_heavy_hitters(self):
        """ Retrieve all heavy hitters from the min heap. """
        return {item: self._count_min.estimate_count(item) for _, item in self._min_heap}

    def merge(self, other):
        """ Merges another heavy-hitter instance into this one. Both instances being
            merged need to share all parameters and hash seeds; otherwise, the merge will fail. """
        self._count_min.merge(other._count_min)
        self._l1_norm += other._l1_norm
        self._min_heap.extend(other._min_heap)
        heapify(self._min_heap)

        cutoff = self._phi * self._l1_norm
        self.remove_below_cutoff(cutoff)

    @classmethod
    def from_existing(cls, original):
        """ Creates a new sketch based on the parameters of an existing sketch.
            Two sketches are mergeable iff they share array size and hash
            seeds. Therefore, to create mergeable sketches, use an original to
            create new instances. """
        new_instance = cls()
        new_instance._init_params(original._phi, original._epsilon, original._delta, original._seed)
        new_instance._count_min = CountMin.from_existing(original._count_min)
        new_instance._l1_norm = 0
        new_instance._min_heap = []
        return new_instance

# --------------------------------------------------------------------------

class MisraGries(AbstractHeavyHitters):
    """ Implements the Misra-Gries algorithm for finding frequent items (heavy hitters). """

    def __init__(self, phi=0.05, epsilon=0.2):
        self._init_params(phi, epsilon)
        self._counters = {}
        self._m = 0

    def _init_params(self, phi, epsilon):
        """ Initialize parameters and compute the number of buckets. """
        self._phi = phi
        self._epsilon = epsilon
        self._k = ceil(1 / (self._phi * self._epsilon))

    def insert(self, token, count=1):
        """ Insert a token into the counters. """
        for _ in range(count):
            self._m += 1
            self._update_counters(token)
        
    def _update_counters(self, token):
        """ Update the counters based on the newly inserted token. """
        if token in self._counters:
            self._counters[token] += 1
        else:
            if len(self._counters) < self._k - 1:
                self._counters[token] = 1
            else:
                self._decrement_counters()

    def _decrement_counters(self):
        """ Decrement all counters and remove those that reach zero. """
        for key in list(self._counters.keys()):
            self._counters[key] -= 1
            if self._counters[key] == 0:
                del self._counters[key]

    def get_heavy_hitters(self):
        """ Retrieve all heavy hitters based on the set threshold. """
        threshold = (1 - self._epsilon) * self._phi * self._m
        return {k: v for k, v in self._counters.items() if v > threshold}

    def merge(self, other):
        """ Merge another Misra-Gries instance into this one. """
        self._m += other._m
        for key, value in other._counters.items():
            self._counters[key] = self._counters.get(key, 0) + value
        self._prune_counters()

    def _prune_counters(self):
        """ Remove excess counters and decrement remaining ones if necessary. """
        if len(self._counters) > self._k:
            min_value = sorted(self._counters.values())[self._k]
            keys_to_delete = []
            for key in self._counters.keys():
                self._counters[key] -= min_value
                if self._counters[key] <= 0:
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                del self._counters[key]

    @classmethod
    def from_phi_and_eps(cls, phi=0.0025, epsilon=0.2):
        new_instance = cls()
        new_instance._init_params(phi=phi, epsilon=epsilon)
        return new_instance

        