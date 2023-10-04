from math import ceil, inf, pow, log
import mmh3
import numpy as np
from copy import deepcopy

class CountMin:
    """ Implements a Count-Min Sketch for approximate frequency estimation. """

    # Class-level constant for 128-bit maximum integer
    _max_128_int = pow(2, 128) - 1

    def __init__(self, width=1, delta=0.05, seed=10):
        """ 
        Initialize a CountMin sketch.
        width: The width of the table.
        delta: Failure probability.
        seed: Seed for hash functions.
        """
        self._delta = delta
        self._width = width
        self._depth = ceil(log(1 / self._delta))
        
        # Initialize the count table
        self._table = np.zeros((self._depth, self._width), dtype=int)
        
        # Initialize hash seeds for each depth layer
        self._hash_seeds = np.arange(self._depth) * seed

    @classmethod
    def from_existing(cls, original_cm):
        """ Create a new CountMin instance based on an existing one. """
        new_cm = deepcopy(original_cm)
        
        # Reset the table to zeros
        new_cm._table = np.zeros((new_cm._depth, new_cm._width), dtype=int)
        
        return new_cm

    def _hash(self, token, seed):
        """ 
        Compute the hash of a token using the given seed. 
        Maps the hash value to a bin number.
        """
        hash_value = mmh3.hash128(token, seed, signed=False) / CountMin._max_128_int
        bin_number = int(hash_value * self._width)
        return bin_number

    def insert(self, token, count):
        """ Insert a token with its count into the sketch. """
        for row in range(self._depth):
            col = self._hash(token, self._hash_seeds[row])
            
            # Update the corresponding count in the table
            self._table[row, col] += count

    def estimate_count(self, token):
        """ 
        Estimate the frequency count of a token.
        The estimate satisfies: true count <= estimate <= true count + phi * total count
        """
        estimates = np.zeros(self._depth, dtype=int)
        
        for row in range(self._depth):
            col = self._hash(token, self._hash_seeds[row])
            estimates[row] = self._table[row, col]
            
        # Use the minimum estimate across all depth layers
        return estimates.min()

    def merge(self, other_count_min):
        """ Merge this CountMin sketch with another one. Both should have the same seeds. """
        self._table += other_count_min._table
