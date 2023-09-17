import unittest
import numpy as np
import random
import string
from sketchlib.minhash import MinHash

class TestMinHash(unittest.TestCase):
    
    def setUp(self):
        self.minhash1 = MinHash(epsilon=0.1)
        self.minhash2 = MinHash.from_existing(self.minhash1)
        
    def test_jaccard_similarity_small(self):
        for elem in ['apple', 'banana', 'cherry']:
            self.minhash1.insert(elem)
        
        for elem in ['banana', 'cherry', 'date']:
            self.minhash2.insert(elem)
        
        estimated_jaccard = self.minhash1.estimate_jaccard_similarity(self.minhash2)
        
        actual_jaccard = len(set(['apple', 'banana', 'cherry']).intersection(set(['banana', 'cherry', 'date']))) / \
                         len(set(['apple', 'banana', 'cherry']).union(set(['banana', 'cherry', 'date'])))
        
        self.assertTrue(np.isclose(estimated_jaccard, actual_jaccard, atol=0.1))

    def test_jaccard_similarity_large(self):
        set1 = set([''.join(random.choices(string.ascii_lowercase, k=5)) for _ in range(1000)])
        set2 = set([''.join(random.choices(string.ascii_lowercase, k=5)) for _ in range(800)]) 
        
        # Insert elements from set1 and set2 into MinHash instances
        for elem in set1:
            self.minhash1.insert(elem)
        
        for elem in set2:
            self.minhash2.insert(elem)
        
        estimated_jaccard = self.minhash1.estimate_jaccard_similarity(self.minhash2)
        
        actual_jaccard = len(set1.intersection(set2)) / len(set1.union(set2))
        
        self.assertTrue(np.isclose(estimated_jaccard, actual_jaccard, atol=0.1))

if __name__ == '__main__':
    unittest.main()
