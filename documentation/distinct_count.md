## LogDistinctCount

This class provides a space and time efficient data structure (called a sketch) to estimate the number of distinct element up to a factor `(1 ± epsilon)` with probability at least `1-delta` in a data stream. This is the implementation of the first algorithm in the paper "Counting Distinct Elements in a Data Stream" by Ziv Bar-Yossef, T. S. Jayram, Ravi Kumar, D. Sivakumar & Luca Trevisan. The data structure uses roughly `O~(1/eps^2 * log(1/delta))` memory (excluding overheads). This is currently the only implementation.


To import the class, use the following:

```python
from sketchlib.distinct_count import LogDistinctCount
```

### overview

The update time is `O(log 1/eps)`. It supports the following operations:

- insert a token to the stream.
- return the estimate for number of distinct elements the stream encounters so far up to a factor `1±eps` with probability at least `1-delta`.
- combine the sketches of two streams so that we can estimate the number of distinct elements of the combined stream.

### initialization

To initialize an instance of this class, we can specify the following parameters:

- `delta`: controls the failure probability. The default value is `0.01`.
- `epsilon`: controls the estimate's quality. The default value is `0.01`.
- `seed`: the seed for randomness. The default value is `42`.


For example,

```python
stream = LogDistinctCount(delta=0.01, epsilon=0.05, seed=42)
stream2 = LogDistinctCount()
```

### insert

Insert a new token into the stream. The token must be byte-like objects. The easiest way to achieve this is to convert a token to string.

For example,

```python
stream = LogDistinctCount(delta=0.01, epsilon=0.05, seed=42)
stream.insert("apple")
stream.insert("orange")
stream.insert("apple")
```

### estimator

Return the estimate of the number of distinct elements that have appeared in the stream so far up to a factor (1 ± epsilon) with probability at least 1-delta.

For example,

```python
stream = LogDistinctCount(delta=0.01, epsilon=0.05, seed=42)

for i in range(100, 200):
    stream.insert(str(i))

for i in range(150, 250):
    stream.insert(str(i))

print(stream.estimator())

>>> 150

```

### merge

Merge with another sketch with the same seed. The resulted sketch will provide answer to the combined stream.

For example,

```python
stream = LogDistinctCount(delta=0.01, epsilon=0.05, seed=42)
stream2 = LogDistinctCount(delta=0.01, epsilon=0.05, seed=42)

for i in range(100, 200):
    stream.insert(str(i))

for i in range(150, 250):
    stream2.insert(str(i))

stream.merge(stream2)
print(stream.estimator())

>>> 150

```

### + Operator

If A is a sketch of some stream and B is a sketch of another stream, then A + B returns the merged sketch that provides the answer to the combined stream. In other words, A = A+B is the same as A.merge(B). 

For example,

```python
stream = LogDistinctCount(delta=0.01, epsilon=0.05, seed=42)
stream2 = LogDistinctCount(delta=0.01, epsilon=0.05, seed=42)

for i in range(100, 200):
    stream.insert(str(i))

for i in range(150, 250):
    stream2.insert(str(i))

stream = stream + stream2
print(stream.estimator())

>>> 150

```

### from_existing 

Create a new sketch with similar parameters so that they can be merged later.

For example,

```python
stream = LogDistinctCount(delta=0.01, epsilon=0.05, seed=42)
stream2 = LogDistinctCount.from_existing(stream)

for i in range(100, 200):
    stream.insert(str(i))

for i in range(150, 250):
    stream2.insert(str(i))

stream.merge(stream2)
print(stream.estimator())

>>> 150

```