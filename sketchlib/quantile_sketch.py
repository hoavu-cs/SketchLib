from sketchlib.count_min import CountMin
from math import log2, ceil, floor
from copy import deepcopy


class QuantileSketch:
    """ A quantile sketch based on Count-Min and dyadic intervals. """

    def __init__(self, epsilon=0.1, delta=0.01, n=10**9, seed=42):
        """
        epsilon: error bound
        delta: probability of error
        m: maximum number of elements in the stream
        n: the elements in the stream are in the range [1, n]
        """
        self._epsilon, self._delta, self._range_elements = epsilon, delta, n
        self._l1_norm, self._seed = 0, seed
        self._num_dyadic_intervals = ceil(log2(n)) + 1

        # Initialize Count-Min sketch for each dyadic interval
        cm_sketch_width = int(2 * log2(self._range_elements) / epsilon)
        self._cm_sketch = [
            CountMin(width=cm_sketch_width, delta=delta, seed=seed) 
            for _ in range(self._num_dyadic_intervals + 1)
        ]

    def _find_largest_inner_dyadic(self, a, b):
        """ Return the largest dyadic interval that is contained in [a, b]."""
        k = m = 0
        a -= 1
        b -= 1
        k_potential = floor(log2(b - a + 1))
        for i in range(k_potential, -1, -1):
            m_potential = ceil(a / (2 ** i))
            upper_limit = (m_potential + 1) * (2 ** i) - 1
            if upper_limit <= b:
                k = i
                m = m_potential
                break
        return [m * (2**k) + 1, (m + 1) * (2**k)]

    def _dyadic_decomposition(self, lower, upper):
        """ Compute the dyadic intervals decomposition of [lower, upper]. """
        if lower > upper:
            return []
        elif lower == upper:
            return [[lower, upper]]
        else:
            interval = self._find_largest_inner_dyadic(lower, upper)
            return self._dyadic_decomposition(lower, interval[0]-1) + [interval] + self._dyadic_decomposition(interval[1]+1, upper)

    def _estimate_total_count_given_intervals(self, intervals):
        """ Given a list of dyadic intervals, return the estimate of the count of elements 
        in the union of these intervals.
        """
        total_count = 0
        for a, b in intervals:
            level = int(log2(b - a + 1))
            position = ceil(a / 2 ** level)
            total_count += self._cm_sketch[level].estimate_count(str(position))
        return total_count

    def insert(self, x, count=1):
        """ Insert an element x into the sketch with a given count. """
        for i in range(self._num_dyadic_intervals + 1):
            position = ceil(x / (2 ** i))
            self._cm_sketch[i].insert(str(position), count)
        self._l1_norm += count

    def query(self, q):
        """ Query the sketch for the qth quantile. """
        threshold, lower, upper = q * self._l1_norm, 1, self._range_elements
        result = None
        while lower <= upper:
            mid = (lower + upper) // 2
            total_count = self._estimate_total_count_given_intervals(
                self._dyadic_decomposition(1, mid)
            )
            if total_count < threshold:
                lower = mid + 1
            else:
                result, upper = mid, mid - 1
        return result

    def merge(self, other):
        """ Merge self with another compatible sketch (same seed, epsilon, and delta) """
        self._l1_norm += other._l1_norm
        for i in range(self._num_dyadic_intervals + 1):
            self._cm_sketch[i].merge(other._cm_sketch[i])

    def __add__(self, other):
        """ Return a new sketch that is the merge of self and other. """
        merged_sketch = deepcopy(self)
        merged_sketch.merge(other)
        return merged_sketch

    @classmethod
    def from_existing(cls, original):
        """ Create a new instance from an existing instance. """
        return cls(
            epsilon=original._epsilon, 
            delta=original._delta, 
            n=original._range_elements, 
            seed=original._seed
        )
