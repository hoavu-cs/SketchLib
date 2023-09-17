## F2Estimate

This class provides a space and time efficient data structure to estimate (called a sketch) the second moment of a data stream up to a factor `(1 ± epsilon)` with probability at least `1-delta`. 

This is an implementation of the Tug-of-War sketch algorithm in the paper "The Space Complexity of Approximating the Frequency Moments" by Noga Alon, Yossi Matias, Mario Szegedy.

To import the class, use the following:

```python
from sketchlib.f2_estimate import F2Estimate
```

### Overview

The second frequency moment is often referred to as the surprise number, since it measures how uneven the distribution of elements in the stream is. For example, the frequency moment of the following stream 

("apple", 2), ("orange", 1), ("apple", 3), ("mango", 4), ("orange", 1)

is `(2+3)^2 + (1+1)^2 + 4^2 = 45`.

The data structure uses roughly `O~(1/eps^2 * log(1/delta))` memory (excluding overheads). 
The update time is `O(1/eps^2 log (1/delta))`. It supports the following operations:

- insert a weighted token into the stream.
- return the estimate of the second frequency moment of the stream up to a factor `1±eps` with probability at least `1-delta`.
- combine the sketches of two streams so that we can estimate the second frequency moment of the combined stream.



### Initialization

To initialize an instance of this class, we can specify the following parameters:

- `delta`: controls the failure probability. The default value is `0.01`.
- `epsilon`: controls the estimate's quality. The default value is `0.01`.
- `seed`: the seed for randomness. The default value is `42`.

For example,

```python
stream = F2Estimate(delta=0.01, epsilon=0.05, seed=42)
stream2 = F2Estimate()
```

### insert

Insert a new token and the weight into the stream. 
The token must be byte-like objects. The easiest way to achieve this is to convert a token to string.

For example,

```python
stream = F2Estimate(delta=0.01, epsilon=0.05, seed=42)
stream.insert("apple", 2)
stream.insert("orange", 2)
stream.insert("apple", 4)
```

At this point, the count of "apple" is 6 and the count of "orange" is 2. Therefore the second frequency moment at this point is `6^2 + 2^2 = 40`.

### estimator

Return the estimate of the number of distinct elements that have appeared in the stream so far up to a factor (1 ± epsilon) with probability at least 1-delta.

For example,

```python
stream = F2Estimate(delta=0.01, epsilon=0.05, seed=42)
stream.insert("apple", 2)
stream.insert("orange", 2)
stream.insert("apple", 4)

print(stream.estimator())

>>> 39.899749373433586

```

### merge

Merge with another sketch with the same seed. The resulted sketch will provide answer to the combine streams.

For example,

```python
stream = F2Estimate(delta=0.01, epsilon=0.05, seed=42)
stream2 = F2Estimate(delta=0.01, epsilon=0.05, seed=42)

stream.insert("apple", 2)
stream.insert("orange", 2)
stream.insert("apple", 4)

stream2.insert("apple", 3)
stream2.insert("orange", 1)
stream2.insert("apple", 2)
stream2.insert("pineapple", 5)

stream.merge(stream2)

print(stream.estimator())

>>> 155.9206349206349

```
### + operator

If A is a sketch of some stream and B is a sketch of another stream, then A + B returns the merged sketch that provides the answer to the combined stream. In other words, A = A+B is the same as A.merge(B). 

For example,

```python
stream = F2Estimate(delta=0.01, epsilon=0.05, seed=42)
stream2 = F2Estimate(delta=0.01, epsilon=0.05, seed=42)

stream.insert("apple", 2)
stream.insert("orange", 2)
stream.insert("apple", 4)

stream2.insert("apple", 3)
stream2.insert("orange", 1)
stream2.insert("apple", 2)
stream2.insert("pineapple", 5)

stream = stream + stream2

print(stream.estimator())

>>> 155.9206349206349

```

### from_existing 

Create a new sketch with similar parameters so that they can be merged later.

For example,
```python
stream = F2Estimate(delta=0.01, epsilon=0.05, seed=42)
stream2 = F2Estimate.from_existing(stream)

stream.insert("apple", 2)
stream.insert("orange", 2)
stream.insert("apple", 4)

stream2.insert("apple", 3)
stream2.insert("orange", 1)
stream2.insert("apple", 2)
stream2.insert("pineapple", 5)

stream.merge(stream2)

print(stream.estimator())

>>> 155.9206349206349

```