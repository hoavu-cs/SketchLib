import unittest
from sketchlib.bloom_filter import BloomFilter
import random
import string

def random_string(length=10):
    """Generate a random string of fixed length."""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

class TestBloomFilter(unittest.TestCase):

    def test_bloom_filter_operations(self):
        # Initialize a Bloom Filter
        bf = BloomFilter(n=1000, delta=0.01)
        
        # Test: Insert elements
        elements_to_insert = ['apple', 'banana', 'cherry']
        for elem in elements_to_insert:
            bf.insert(elem)

        # Test: Check for membership
        for elem in elements_to_insert:
            self.assertTrue(bf.membership(elem), f"Element {elem} should be in the filter")

        # Test: Check for non-membership
        non_members = ['dragonfruit', 'elderberry', 'fig']
        for elem in non_members:
            self.assertFalse(bf.membership(elem), f"Element {elem} should mostly not be in the filter")

        # Test: Delete an element and check for its membership
        bf.delete('apple')
        elements_to_insert.remove('apple')
        self.assertFalse(bf.membership('apple'), "Element 'apple' should not be in the filter after deletion")

    def test_bloom_filter_operations_merge(self):

        # Initialize a Bloom Filter
        bf = BloomFilter(n=1000, delta=0.01)
        
        # Test: Insert elements
        elements_to_insert = ['apple', 'banana', 'cherry']
        for elem in elements_to_insert:
            bf.insert(elem)

        # Test: Merge two Bloom filters
        bf2 = BloomFilter.from_existing(bf)
        elements_to_insert_2 = ['grape', 'honeydew', 'kiwi']
        for elem in elements_to_insert_2:
            bf2.insert(elem)
        bf.merge(bf2)


        merged_elements = set(elements_to_insert + elements_to_insert_2)
        # Test: Addition of two Bloom filters
        bf3 = bf + bf2
        for elem in merged_elements:
            self.assertTrue(bf3.membership(elem), f"Element {elem} should be in the filter after addition")

        bf.merge(bf2)
        # Test: Check for membership in merged filter
        for elem in merged_elements:
            self.assertTrue(bf.membership(elem), f"Element {elem} should be in the merged filter")

    def test_bloom_filter_operations_large(self):

        # Test: Large number of insertions
        large_n = 100000
        delta = 0.01
        bf_large = BloomFilter(n=large_n, delta=delta)
        large_elements = [random_string() for _ in range(large_n)]
        for elem in large_elements:
            bf_large.insert(elem)

        # Test: Verify membership for all inserted elements
        false_positives = 0
        for elem in large_elements:
            if not bf_large.membership(elem):
                false_positives += 1
        self.assertEqual(false_positives, 0, "Inserted elements should be in the filter")

        # Allowing for a margin of error in the false positive rate
        max_allowed_false_positives = 2 * delta * large_n
        self.assertLessEqual(false_positives, max_allowed_false_positives, f"Too many false positives: got {false_positives}, expected <= {max_allowed_false_positives}")

        # Test: Large number of deletions
        deleted_elements = random.sample(large_elements, int(large_n * 0.1))  # delete 10% of elements
        for elem in deleted_elements:
            bf_large.delete(elem)

        # Test: Verify non-membership for all deleted elements
        false_positives = 0
        for elem in deleted_elements:
            if bf_large.membership(elem):
                false_positives += 1


if __name__ == '__main__':
    unittest.main()
