import mmh3
import math
import random
import numpy as np 
from copy import deepcopy

class MinHash:
    max_128_int = pow(2, 128) - 1

    def __init__(self, epsilon=0.1, hash_type="mmh3", seed=42):
        self.epsilon = epsilon
        self.hash_type = hash_type
        self.k = 4 * math.ceil(1 / pow(self.epsilon, 2))
        self.seed = seed
        self.seeds = np.array([self.seed * i for i in range(self.k)])
        self.minhash_signature = np.ones(self.k, dtype=float)

    def insert(self, token):
        for i in range(self.k):
            current_hash = self._hash(token, self.seeds[i])
            if current_hash < self.minhash_signature[i]:
                self.minhash_signature[i] = current_hash

    def merge(self, other_mh):
        """Merges two minhash signatures resulting in a single signature representing the union of the two original sets."""
        try:
            self.check_mergeability(other_mh)
            self.minhash_signature = np.minimum(self.minhash_signature, other_mh.minhash_signature)
        except AttributeError:
            print("Merge attempted on incompatible minhash instances.")

    def __add__(self, other_minhash):
        """Performs merge but returns result in completely new minhash."""
        merged_minhash = deepcopy(self)
        merged_minhash.merge(other_minhash)
        return merged_minhash

    def _hash(self, token, seed):
        """Compute the hash of a token."""
        if self.hash_type == "mmh3":
            return mmh3.hash(token, seed, signed=False) / MinHash.max_128_int

    @classmethod
    def from_existing(cls, original):
        """Creates a new minhash based on the parameters of an existing minhash."""
        new_minhash = cls(epsilon=original.epsilon, hash_type=original.hash_type, seed=original.seed)
        return new_minhash

    def _check_mergeability(self, other_minhash):
        """Compares other minhash signature attributes to make sure that merges or Jaccard similarity estimates make sense."""
        if other_minhash.k != self.k:
            raise AttributeError("Minhash signature sets must be of equal lengths k in order to merge.")
        else:
            if not np.array_equal(self.seeds, other_minhash.seeds):
                raise AttributeError("Minhash hash functions must have same seed values for valid result.")

    def estimate_jaccard_similarity(self, other_mh):
        """Provides an estimate for the Jaccard Similarity of two sets."""
        counter = np.sum(self.minhash_signature == other_mh.minhash_signature)
        return counter / self.k

