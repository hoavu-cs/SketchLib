from sketchlib.bloom_filter import BloomFilter
import random
import string


def random_string(length=10):
    """Generate a random string of fixed length."""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def test_bloom_filter():
    # Initialize a Bloom Filter with 1000 maximum insertions and a false positive rate of 1%
    bf = BloomFilter(n=1000, delta=0.01)
    
    # Test: Insert elements
    elements_to_insert = ['apple', 'banana', 'cherry']
    for elem in elements_to_insert:
        bf.insert(elem)

    # Test: Check for membership (should return True)
    for elem in elements_to_insert:
        assert bf.membership(elem) == True, f"Element {elem} should be in the filter"

    # Test: Check for non-membership (should return False or occasionally True due to false positives)
    non_members = ['dragonfruit', 'elderberry', 'fig']
    for elem in non_members:
        print(f"Membership of {elem}: {bf.membership(elem)}")  # Should be mostly False

    # Test: Delete an element and check for its membership (should return False)
    bf.delete('apple')
    elements_to_insert.remove('apple')
    assert bf.membership('apple') == False, "Element 'apple' should not be in the filter after deletion"

    # Test: Merge two Bloom filters
    bf2 = BloomFilter.from_existing(bf)
    elements_to_insert_2 = ['grape', 'honeydew', 'kiwi']
    for elem in elements_to_insert_2:
        bf2.insert(elem)
    bf.merge(bf2)

    # Test: Check for membership in merged filter
    for elem in elements_to_insert_2:
        assert bf.membership(elem) == True, f"Element {elem} should be in the merged filter"

    # Test: Addition of two Bloom filters
    bf3 = bf + bf2
    for elem in elements_to_insert + elements_to_insert_2:
        assert bf3.membership(elem) == True, f"Element {elem} should be in the filter after addition"

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
    assert false_positives == 0, "Inserted elements should be in the filter"

    # Test: Large number of deletions
    deleted_elements = random.sample(large_elements, int(large_n * 0.1))  # delete 10% of elements
    for elem in deleted_elements:
        bf_large.delete(elem)

    # Test: Verify non-membership for all deleted elements
    false_positives = 0
    for elem in deleted_elements:
        if bf_large.membership(elem):
            false_positives += 1

    # Allowing for a margin of error in the false positive rate
    max_allowed_false_positives = 2 * delta * large_n
    assert false_positives <= max_allowed_false_positives, f"Too many false positives: got {false_positives}, expected <= {max_allowed_false_positives}"

    print("All tests passed.")


if __name__ == '__main__':
    test_bloom_filter()
