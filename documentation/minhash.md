## Minhash

This class provides a space and time efficient data structure (called a minhash) to represent large sets in a much more compact form. It is able to provide an estimate of the Jaccard similarity of two sets within a factor `(1 ± epsilon)` much more quickly than performing an exact calculation.


To import the class, use the following:

```python
from sketchlib.minhash import MinHash
```

### Overview

The update time is `O(1/eps^2)`. It supports the following operations:

- insert a token into the minhash.
- return an estimate of the Jaccard similarity between two sets to within a factor `1±eps`.
- combine the minhashes of two sets so that we can treat the union of two sets as a single set.

### Initialization

To initialize an instance of this class, we can specify the following parameters:

- `epsilon`: controls the estimate's quality. The default value is `0.01`.

For example,

```python
stream = MinHash(epsilon=0.05)
stream2 = MinHash()
```

### insert

Insert a new token into the stream. The token must be byte-like objects. The easiest way to achieve this is to convert a token to string.

For example,

```python
stream = MinHash(epsilon=0.01)
stream.insert("apple")
stream.insert("orange")
stream.insert("apple")
```

### estimate_jaccard_similarity

Return an estimate of the Jaccard similarity between the current set and another set up to a factor (1 ± epsilon). 

NOTE: both sets must have the same epsilon and seed values. See from_existing for how to achieve this.

For example,

```python
stream = MinHash(epsilon=0.01)
stream2 = MinHash.from_existing(stream)

for i in range(100, 200):
    stream.insert(str(i))

for i in range(150, 250):
    stream.insert(str(i))

print(stream.estimate_jaccard_similarity(stream2))

>>> 0.33

```

### merge

Merge with another minhash with the same epsilon and internal seeds. The resulting minhash will provide a representation of the union of the two sets.

For example,

```python
stream = MinHash(epsilon=0.01)
stream2 = MinHash.from_existing(stream)
stream3 = MinHash.from_existing(stream)

for i in range(100, 200):
    stream.insert(str(i))

for i in range(150, 250):
    stream2.insert(str(i))

for i in range(200, 300):
    stream3.insert(str(i))

stream.merge(stream2)
print(stream.estimate_jaccard_similarity(stream3))

>>> .167

```

### + Operator

If A is a minhash of some stream and B is a minhash of another stream, then A + B returns the merged minhash representing the combined stream. In other words, A = A+B is the same as A.merge(B). 

For example,

```python
stream = MinHash(epsilon=0.01)
stream2 = MinHash.from_existing(stream)
stream3 = MinHash.from_existing(stream)

for i in range(100, 200):
    stream.insert(str(i))

for i in range(150, 250):
    stream2.insert(str(i))
    
for i in range(200, 300):
    stream3.insert(str(i))

stream1 = stream + stream2
print(stream1.estimate_jaccard_similarity(stream3))

>>> .167

```

### from_existing 

Create a new minhash based on the parameters of an existing minhash so that they can be merged later.

For example,

```python
stream = MinHash(epsilon=0.05)
stream2 = MinHash.from_existing(stream)

for i in range(100, 200):
    stream.insert(str(i))

for i in range(150, 250):
    stream2.insert(str(i))

stream.merge(stream2)

```