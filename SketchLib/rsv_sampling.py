import random
from copy import deepcopy

class RsvSampling:
    """ Sample a random element in a data stream without knowing the stream length. """
    
    def __init__(self, rsv_size):
        """ Initialize with a reservoir size k to return k random tokens from the stream. """
        self._rsv = []
        self._rsv_size = rsv_size
        self._stream_length = 0

    def insert(self, token):
        """ Insert a token into the stream. """
        self._stream_length += 1
        if len(self._rsv) < self._rsv_size:
            self._rsv.append(token)
        else:
            j = random.randint(1, self._stream_length)
            if j <= self._rsv_size:
                self._rsv[j - 1] = token

    def reservoir(self):
        """ Return the list of sampled tokens. """
        return self._rsv
    
    def merge(self, S):
        """ Merge two samplers with the same size. """
        self._rsv = random.sample(self._rsv + S._rsv, self._rsv_size)
    
    def __add__(self, S):
        """ Return the merged sampler of self and S. """
        new_sampler = deepcopy(self)
        new_sampler.merge(S)
        return new_sampler
    
    @classmethod
    def from_existing(cls, original):
        """ Create another reservoir sampler with the same size. """
        return cls(rsv_size=original._rsv_size)
