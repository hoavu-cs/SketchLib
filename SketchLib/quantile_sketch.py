from sketchlib.count_min import CountMin
from math import log2, ceil, floor

class QuantileSketch:
    """
    A quantile sketch based on Count-Min.
    """

    def __init__(self, epsilon=0.1, delta=0.01, m=10**9, n=10**9, seed=42):
        """
        epsilon: error bound
        delta: probability of error
        m: maximum number of elements in the stream
        n: the elements in the stream are in the range [1, n]
        """
        self.epsilon = epsilon
        self.delta = delta
        self.max_count = m
        self.range_elements = n
        self.l1_norm = 0
        self.num_dyadic_intervals = ceil(log2(n))

        # Initialize Count-Min sketch for each dyadic interval
        cm_sketch_width = ceil(4*log2(self.max_count)/self.epsilon)   
        self.cm_sketch = [
            CountMin(width=cm_sketch_width, delta=self.delta, seed=seed)
            for _ in range(self.num_dyadic_intervals + 1)
        ]

    def _decompose_into_dyadic_intervals(self, lower, upper):
        """
        Compute the dyadic intervals decomposition of [lower, upper].
        """
        if lower < 1:
            raise ValueError("Lower bound must be at least 1.")
        
        if lower == upper:
            return [(lower, upper)]
        
        if lower > upper:
            return []

        split_point = lower + 2 ** floor(log2(upper - lower)) - 1
        intervals = [(lower, split_point)]
        intervals += self._decompose_into_dyadic_intervals(split_point + 1, upper)
        return intervals

    def _positions_in_intervals(self, x):
        """
        Return the position of the dyadic intervals that x belongs to in each level.
        For example, if n = 20, then we have the following dyadic intervals:
        level 2^0: [1, 1], [2, 2], ..., [19, 19], [20, 20]
        level 2^1: [1, 2], [3, 4], ..., [19, 20]
        level 2^2: [1, 4], [5, 8], ..., [17, 20]
        ...
        For each level, return the position of x in the dyadic interval.
        For example, if x = 5, then return [5, 3, 2, 1, 1] because x is in the dyadic intervals
        [5, 5], [5, 6], [5, 8], [1, 16], [1, 32].
        """
        positions = []
        for i in range(self.num_dyadic_intervals + 1):
            length = 2 ** i
            position = ceil(x / length)
            positions.append(position)
        return positions

    def _estimate_total_count_given_intervals(self, intervals):
        """
        Given a list of dyadic intervals, return the estimate of the count of elements 
        in the union of these intervals.
        """
        total_count = 0
        for a, b in intervals:
            level = int(log2(b - a + 1))
            total_count += self.cm_sketch[level].estimate_count(str(a))
        return total_count

    def insert(self, x, count=1):
        """
        Insert an element x into the sketch with a given count.
        """
        positions = self._positions_in_intervals(x)
        for i, pos in enumerate(positions):
            self.cm_sketch[i].insert(str(pos), count)
        self.l1_norm += count        

    def query(self, q):
        """
        Query the sketch for the qth quantile. Return the smallest i such that 
        count(i) >= q * l1_norm and count(i - 1) < (q + epsilon) * l1_norm.
        """
        threshold = q * self.max_count
        lower, upper = 1, self.max_count

        while lower < upper:
            mid = (lower + upper) // 2
            intervals = self._decompose_into_dyadic_intervals(1, mid)
            total_count = self._estimate_total_count_given_intervals(intervals)

            print(total_count)

            if total_count > q * self.l1_norm:
                upper = mid
            elif total_count < q * self.l1_norm:
                lower = mid + 1
            else:
                return mid

        intervals = self._decompose_into_dyadic_intervals(1, lower)
        total_count = self._estimate_total_count_given_intervals(intervals)

        print(lower, total_count, self.l1_norm)

        if total_count > q * self.l1_norm:
            return lower
        else:
            return lower + 1

    def merge(self, other_sketch):
        """ 
        Merge self with another compatible sketch (same seed, epsilon, and delta)
        """ 
        self.l1_norm += other_sketch.l1_norm
        for i in range(self.num_dyadic_intervals + 1):
            self.cm_sketch[i].merge(other_sketch.cm_sketch[i])

    def __add__(self, other):
        """ 
        Return a new sketch that is the merge of self and other.
        """ 
        merged_sketch = deepcopy(self)
        merged_sketch.merge(other)
        return merged_sketch

    @classmethod
    def from_existing(cls, original):
        new_instance = cls(epsilon=original.epsilon, delta=original.delta, m=original.max_count,\
            n=original.range_elements, seed=original.seed)
        return new_instance


        

