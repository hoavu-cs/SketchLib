import random
from copy import deepcopy

class RsvSampling:
    """ 
    Implements a reservoir sampling algorithm to sample a fixed-size subset
    of a stream of items whose size is unknown a priori.
    """

    def __init__(self, rsv_size):
        """ 
        Initialize the reservoir sampler.
        
        rsv_size: Size of the reservoir for storing sampled items.
        """
        self._rsv = []            # Reservoir list to store sampled items
        self._rsv_size = rsv_size # Fixed size of the reservoir
        self._stream_length = 0   # Counter to keep track of the number of items seen

    def insert(self, token):
        """ 
        Insert a token into the stream and update the reservoir accordingly.
        
        token: Item to be inserted into the stream.
        """
        self._stream_length += 1  # Increment the counter for the stream length

        # If reservoir is not yet full, simply append
        if len(self._rsv) < self._rsv_size:
            self._rsv.append(token)
        else:
            # Otherwise, possibly replace an existing item in the reservoir
            j = random.randint(1, self._stream_length)
            if j <= self._rsv_size:
                self._rsv[j - 1] = token

    def reservoir(self):
        """ 
        Return the current set of items in the reservoir.
        """
        return self._rsv

    def merge(self, S):
        """ 
        Merge this reservoir with another one of the same size.
        
        S: Another RsvSampling object to merge with.
        """
        # Combine both reservoirs and resample to maintain the original size
        self._rsv = random.sample(self._rsv + S._rsv, self._rsv_size)

    def __add__(self, S):
        """ 
        Return a new RsvSampling object that is the result of merging self and S.
        
        S: Another RsvSampling object to merge with.
        """
        # Create a deep copy and merge with the other reservoir
        new_sampler = deepcopy(self)
        new_sampler.merge(S)
        return new_sampler

    @classmethod
    def from_existing(cls, original):
        """ 
        Create a new RsvSampling object with the same reservoir size as the original.
        
        original: An existing RsvSampling object to base the new one on.
        """
        return cls(rsv_size=original._rsv_size)
