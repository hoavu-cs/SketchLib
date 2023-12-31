import unittest
from sketchlib.quantile_sketch import QuantileSketch

def compute_true_counts(elms):
    elms.sort()
    true_counts = {}
    for idx, elm in enumerate(elms):
        true_counts[elm] = idx + 1
    return true_counts

class TestQuantileSketch(unittest.TestCase):
    
    def test_insert_query_basic(self):
        naive_list = []
        n = 10
        epsilon = 0.001
        sketch = QuantileSketch(epsilon=epsilon, delta=0.01, n=n, seed=42)

        for i in range(1, n+1):
            sketch.insert(i)
            naive_list.append(i)
        
        true_counts = compute_true_counts(naive_list)
        queries = [0.1, 0.5, 0.9]

        for q in queries:
            result = sketch.query(q)
            if result == 1:
                assert true_counts[result] >= (q - epsilon) * len(naive_list) 
            else:
                assert true_counts[result] >= (q - epsilon) * len(naive_list) and true_counts[result-1] <= q * len(naive_list)

    def test_insert_query_advanced(self):
        naive_list = []
        n = 100
        epsilon = 0.01
        sketch = QuantileSketch(epsilon=epsilon, delta=0.01, n=n, seed=42)
        naive_list = []

        for elm in range(1, n+1):
            sketch.insert(elm, elm)
            naive_list.extend([elm]*elm)

        queries = [0.1, 0.2, 0.4, 0.5, 0.6, 0.9]
        true_counts = compute_true_counts(naive_list)

        for q in queries:
            result = sketch.query(q)
            if result == 1:
                assert true_counts[result] >= (q - epsilon) * len(naive_list) 
            else:
                assert true_counts[result] >= (q - epsilon) * len(naive_list) and true_counts[result-1] <= q * len(naive_list)

    def test_merge(self):
        naive_list1 = []
        naive_list2 = []
        n = 20000
        epsilon = 0.01
        sketch1 = QuantileSketch(epsilon=epsilon, delta=0.01, n=n, seed=42)
        sketch2 = QuantileSketch.from_existing(sketch1)
        naive_list = []

        for elm in range(1, int(n/2)):
            sketch1.insert(elm, elm)
            naive_list.extend([elm]*elm)
        
        for elm in range(int(n/4), int(3*n/4)):
            sketch2.insert(elm, elm)
            naive_list.extend([elm]*elm)

        queries = [0.1, 0.2, 0.4, 0.5, 0.6, 0.9]
        true_counts = compute_true_counts(naive_list)
        sketch1 += sketch2

        for q in queries:
            result = sketch1.query(q)
            if result == 1:
                assert true_counts[result] >= (q - epsilon) * len(naive_list) 
            else:
                assert true_counts[result] >= (q - epsilon) * len(naive_list) and true_counts[result-1] <= q * len(naive_list)

    def test_merge_2(self):
        n = 200
        epsilon = 0.1
        sketch1 = QuantileSketch(epsilon=epsilon, delta=0.01, n=n, seed=42)
        sketch2 = QuantileSketch.from_existing(sketch1)
        naive_list = []

        for elm in range(1, int(n/2)):
            sketch1.insert(elm, elm)
            naive_list.extend([elm]*elm)
        
        for elm in range(int(n/4), int(3*n/4)):
            sketch2.insert(elm, elm)
            naive_list.extend([elm]*elm)

        queries = [0.1, 0.2, 0.4, 0.5, 0.6, 0.9]
        sketch1.merge(sketch2)
        true_counts = compute_true_counts(naive_list)

        for q in queries:
            result = sketch1.query(q)
            if result == 1:
                assert true_counts[result] >= (q - epsilon) * len(naive_list) 
            else:
                assert true_counts[result] >= (q - epsilon) * len(naive_list) and true_counts[result-1] <= q * len(naive_list)

if __name__ == '__main__':
    unittest.main()
