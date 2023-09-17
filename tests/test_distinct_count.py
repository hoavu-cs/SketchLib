import unittest
import random
import string
from sketchlib.distinct_count import LogDistinctCount

class TestF0Sketch(unittest.TestCase):
    
    def random_string(self, length=10):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))

    def test_basic_functionality(self):
        f0sketch = LogDistinctCount(epsilon=0.01, delta=0.01)

        # Insert 1000 distinct elements
        distinct_elements = set()
        for i in range(100000):
            element = self.random_string()
            distinct_elements.add(element)
            f0sketch.insert(element)

        estimated_distinct = f0sketch.estimator()
        actual_distinct = len(distinct_elements)

        # Check that estimated distinct elements are within (1±ε) factor
        lower_bound = actual_distinct * (1 - 0.01)
        upper_bound = actual_distinct * (1 + 0.01)
        self.assertTrue(lower_bound <= estimated_distinct <= upper_bound)

    def test_merge_functionality(self):
        f0sketch1 = LogDistinctCount(epsilon=0.01, delta=0.01)
        f0sketch2 = LogDistinctCount.from_existing(f0sketch1)

        # Insert 500 distinct elements into f0sketch1
        distinct_elements1 = set()
        for i in range(500000):
            element = self.random_string()
            distinct_elements1.add(element)
            f0sketch1.insert(element)

        # Insert 500 distinct elements into f0sketch2
        distinct_elements2 = set()
        for i in range(500):
            element = self.random_string()
            if element not in distinct_elements1:
                distinct_elements2.add(element)
                f0sketch2.insert(element)

        # Merge f0sketch1 and f0sketch2
        f0sketch1 += f0sketch2

        # Total distinct elements after merge
        total_distinct_elements = len(distinct_elements1.union(distinct_elements2))
        
        estimated_distinct = f0sketch1.estimator()
        
        # Check that estimated distinct elements are within (1±ε) factor
        lower_bound = total_distinct_elements * (1 - 0.01)
        upper_bound = total_distinct_elements * (1 + 0.01)
        self.assertTrue(lower_bound <= estimated_distinct <= upper_bound)

    def test_merge_functionality_2(self):
        f0sketch1 = LogDistinctCount(epsilon=0.01, delta=0.01)
        f0sketch2 = LogDistinctCount.from_existing(f0sketch1)

        # Insert 1000 distinct elements
        distinct_elements = set()

        for i in range(10000):
            element = random.randint(1, 1000)
            distinct_elements.add(element)
            f0sketch1.insert(str(element))

        for i in range(10000):
            element = random.randint(500, 1500)
            distinct_elements.add(element)
            f0sketch2.insert(str(element))
        
        f0sketch2 += f0sketch1
        estimated_distinct = f0sketch2.estimator()
        actual_distinct = len(distinct_elements)

        # Check that estimated distinct elements are within (1±ε) factor
        lower_bound = actual_distinct * (1 - 0.01)
        upper_bound = actual_distinct * (1 + 0.01)
        self.assertTrue(lower_bound <= estimated_distinct <= upper_bound)

if __name__ == "__main__":
    unittest.main()
