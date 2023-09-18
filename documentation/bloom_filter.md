## BloomFilter

This class provides an implementation of Bloom Filter, a space and time-efficient approach to represent a set that supports insertions, deletions, and membership queries. 

The Bloom Filter was first introduced in the paper "Space/Time Trade-offs in Hash Coding with Allowable Errors" by Burton H. Bloom.

To import the class, use the following:

```python
from sketchlib.bloom_filter import BloomFilter
```
### overview

The data structure allows three operations: 

- insert an element into the set
- delete an element from the set
- check if an element is in the set

If there are at most `n` elements in the set and `delta` is the false positive rate (i.e., the probability that an element is not in the set but is falsely reported as being in the set by the data structure), then the data structure uses roughly `O~(n * log(1/delta))` bits of memory (excluding overheads). 

The update time is `O(1/eps^2 log (1/delta))`.

If each element is an image of size `200kb`, then if we need to store `m = 10^6` images, then the total space is `2 * 10^8 Kb = 200Gb`. So if we allow `1%` false positive rate, then the space that Bloom Filter uses is `10^6  * ln(log(1/0.01))/ln(2)` bits which is approximate `0.2754 Mb`. This is a big saving.

Each operation takes roughly `O(log(1/delta))` time.

### initialization

To initialize an instance of this class, we can specify the following parameters:

- `delta`: controls the false positive rate. The default value is `0.01`.
- `n`: the maximum number of elements to be inserted into the filter.
- `seed`: the seed for randomness. The default value is `42`.

```python
delta = 0.1
n = 1000
B = BloomFilter(n = n, delta = delta, seed = 50)
```

### insert

To insert an element into the set, the element must be a byte-like object. The simplest approach is to convert an object to a string. 
For example,

```python
delta = 0.0001
n = 100
B = BloomFilter(n = n, delta = delta)

for i in range(n):
    B.insert(str(i))
```

### membership

Check if an element is in the set, use the membership query function. However, there is a probability `delta` of false positives, meaning the function may incorrectly return `True` for an element that is not in the set. 

For example,

```python
delta = 0.0001
n = 10000
false_positives = 0
B = BloomFilter(n = n, delta = delta)

for i in range(n):
    B.insert(str(i))

for j in range(2*n):
    if j >= n and B.membership(str(j)) == True:
        false_positives += 1
        
print(false_positives)

>>> 1
```

### merge

To merge with another Bloom filter with the same seed, use the merge function. The resulting filter will provide the answer to the union of two sets. 

For example,

```python
delta = 0.05
n = 1000
B = BloomFilter(n = 2*n, delta = delta, seed=42)
C = BloomFilter(n = 2*n, delta = delta, seed=42)
false_positives = 0

for i in range(n):
    B.insert(str(i))

for i in range(int(n/2), int((3/2)*n)):
    C.insert(str(i))

B.merge(C)

for j in range(2*n):
    if j >= (3/2)*n and B.membership(str(j)) == True:
        false_positives += 1

print(false_positives)

>>> 12
```

### delete

To delete an element from the set, use the delete function. However, note that the overall correctness is only guaranteed if the element exists in the set. For example,


```python
delta = 0.05
n = 1000
B = BloomFilter(n = 2*n, delta = delta)
C = BloomFilter(n = 2*n, delta = delta)
false_positives = 0

for i in range(n):
    B.insert(str(i))

for i in range(int(n/2), int((3/2)*n)):
    C.insert(str(i))

B.merge(C)

for j in range(2*n):
    if j >= (3/2)*n and B.membership(str(j)) == True:
        false_positives += 1

print(false_positives)

>>> 12
```

### + operator

Merge two Bloom filters A and B with the same seeds.  The resulting filter will provide the answer to the union of two sets. 
In other words, A = A + B is the same as A.merge(B).

```python
delta = 0.05
n = 1000
B = BloomFilter(n = 2*n, delta = delta)
C = BloomFilter(n = 2*n, delta = delta)
false_positives = 0

for i in range(n):
    B.insert(str(i))

for i in range(int(n/2), int((3/2)*n)):
    C.insert(str(i))

B = B + C

for j in range(2*n):
    if j >= (3/2)*n and B.membership(str(j)) == True:
        false_positives += 1

print(false_positives)

>>> 12
```

### from_existing 

Create a new Bloom Filter with similar parameters (which is the seeds to hash functions in this case) so that they can be merged later.

```python
delta = 0.05
n = 1000
B = BloomFilter(n = 2*n, delta = delta)
C = BloomFilter.from_existing(B)
false_positives = 0

for i in range(n):
    B.insert(str(i))

for i in range(int(n/2), int((3/2)*n)):
    C.insert(str(i))

B.merge(C)

for j in range(2*n):
    if j >= (3/2)*n and B.membership(str(j)) == True:
        false_positives += 1

print(false_positives)

>>> 12
```

# get_filter

Return the bit filter array of the Bloom Filter. 

```python
from sketchlib.bloom_filter import BloomFilter

# Initialize a Bloom Filter with 1000 maximum insertions and a false positive rate of 1%
bf = BloomFilter(n=10, delta=0.1)

# Test: Insert elements
elements_to_insert = ['apple', 'banana', 'cherry']
for elem in elements_to_insert:
    bf.insert(elem)

print(bf.get_filter())

>> [1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 1 0 0 0 0 0 0 0 1 0 0
 0 0 0 1 0 0 0 1 1 0 0]

```