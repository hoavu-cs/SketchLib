import mmh3
import math
import random
import numpy as np
from copy import deepcopy


class MinHash:
    """ MinHash Sketch """

    max_128_int = pow(2, 128) - 1

    def __init__(self, epsilon=0.1, seed=42):
        """
        epsilon: approximation error for Jaccard similarity,
        seed: seed for hash function.
        """
        self._epsilon = epsilon
        self._k = 4 * math.ceil(1 / pow(self._epsilon, 2))
        self._seed = seed
        self._seeds = np.arange(self._k) * self._seed
        self._minhash_signature = np.ones(self._k, dtype=float)

    def insert(self, token):
        """ Inserts a token into the set. """
        for i in range(self._k):
            current_hash = self._hash(token, self._seeds[i])
            if current_hash < self._minhash_signature[i]:
                self._minhash_signature[i] = current_hash

    def merge(self, other_mh):
        """ Merges two minhash signatures resulting in a single signature 
        representing the union of the two original sets. """
        try:
            self._check_mergeability(other_mh)
            self._minhash_signature = np.minimum(self._minhash_signature, other_mh._minhash_signature)
        except AttributeError:
            print("Merge attempted on incompatible minhash instances.")

    def __add__(self, other_minhash):
        """ Performs merge but returns result in completely new minhash. """
        merged_minhash = deepcopy(self)
        merged_minhash.merge(other_minhash)
        return merged_minhash

    def _hash(self, token, seed):
        """ Compute the hash of a token. """
        return mmh3.hash(token, seed, signed=False) / MinHash.max_128_int

    @classmethod
    def from_existing(cls, original):
        """ Creates a new minhash based on the parameters of an existing minhash. """
        new_minhash = cls(epsilon=original._epsilon, seed=original._seed)
        return new_minhash

    def _check_mergeability(self, other_minhash):
        """ Compares other minhash signature attributes to make sure that merges or Jaccard similarity estimates make sense. """
        if other_minhash._k != self._k:
            raise AttributeError("Minhash signature sets must be of equal lengths k in order to merge.")
        else:
            if not np.array_equal(self._seeds, other_minhash._seeds):
                raise AttributeError("Minhash hash functions must have same seed values for valid result.")

    def estimate_jaccard_similarity(self, other_mh):
        """ Provides an estimate for the Jaccard Similarity of two sets. """
        counter = np.sum(self._minhash_signature == other_mh._minhash_signature)
        return counter / self._k

    def get_signature(self):
        """ Returns the minhash signature. """
        return self._minhash_signature
