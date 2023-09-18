## Quantile Sketch

This class provides a space and time efficient data structure to approximate quantiles.
Given a stream of tokens (with possibly duplicates) with values in the range `1, 2, 3,..., n`, 
we build a data structure (based on Count Min sketch and dyadic intervals) that allow us to estimate the quantiles of the stream.

Let m be the total number of tokens. Given `q` in the range `0,1`, we can estimate the `q`-quantile of the stream by output `i` such that

- The count of tokens `1, 2, ..., i` is at least `(q - epsilon) * n`.
- The count of tokens `1, 2,..., i-1` is less than `q * n`.

For example, if `epsilon = 0.1` if we have a stream of 10 tokens, 
`1, 1, 2, 2, 2, 3, 3, 3, 3, 3`, 
then an estimate 0.5-quantile is 2 since the count of tokens `1, 2` is `5 >= (0.5-0.1) * 10`  and the count of tokens `1` is `2 < 0.5 * 10`.

To import the class, use the following:

```python
from sketchlib.quantile_sketch import QuantileSketch
```

### overview

The sketch supports the following operations:

- insert a token with some counts into the sketch.
- query an estimate `q`-quantile of the stream.
- merge with another sketch.

### initialization

To initialize an instance of this class, we can specify the following parameters:

- `epsilon`: controls the estimate's quality. The default value is `0.01`.
- `delta`: controls the failure probability. The default value is `0.01`.
- `n`: the range of the values. The default value is `10^6`. Note that all insertions must be in the range `1,2,...,n`. You can pick a sizable upper bound since the complexity only depends on `log n`.
- `max_count`: the maximum total count of all tokens. You can pick a good upper bound since the space and time complexity only depends on `log max_count`. The default value is `10^9`.
- `seed`: the seed for randomness. The default value is `42`.

For example,

```python
stream = QuantileSketch(epsilon=0.01, delta=0.01, n=10**6, max_count=10**9, seed=1)
```

### insert

Insert a new token with a count (default=1) into the stream. The token must be an integer between `1` and `n`.

For example,

```python
stream = QuantileSketch(epsilon=0.01, delta=0.01, n=10**6, max_count=10**9, seed=1)
for i in range(1, 1000):
    stream.insert(x=i)

stream.insert(x=1, count=5)
```
In the first loop, we add tokens `1, 2, ..., 999` to the stream. Then we add 5 more of token 1 to the stream. The stream now consists of `1, 2, 3, ..., 999, 1, 1, 1, 1, 1`. Note that the current count is `999+5=1004` which should be below the `max_count` we specified.

### query

To query for an approximate q-quantile, use `.query(q)`. This will return an integer `i` between `1` and `n` that satisfies:
- The count of tokens `1,2,...,i` is at least `(q -epsilon) * n`.
- The count of tokens `1,2,...,i-1` is less than `q * n`.

```python
m = 1000
epsilon = 0.1
sketch = QuantileSketch(epsilon=epsilon, delta=0.01, max_count=m, n=m, seed=42)

for i in range(1, m):
    sketch.insert(i)
    naive_list.append(i)
    
true_counts = compute_true_counts(naive_list)
queries = [0.1, 0.5, 0.9]

for q in queries:
    result = sketch.query(q)
    print(result)

>>> 98
500
898

```

### from_existing 

Create a new sketch based on the parameters (e.g., seed, max_count, n) of an existing minhash so that they can be merged later.

For example,

```python
m = 1000000
n = 200
epsilon = 0.01
sketch1 = QuantileSketch(epsilon=epsilon, delta=0.01, max_count=m, n=m, seed=42)
sketch2 = QuantileSketch.from_existing(sketch1)

```

### merge

Merge with another sketch with the same parameters.

For example,

```python
m = 1000000
n = 200
epsilon = 0.1
sketch1 = QuantileSketch(epsilon=epsilon, delta=0.01, max_count=m, n=n, seed=42)
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
sketch1.merge(sketch2)

for q in queries:
    result = sketch1.query(q)
    print(result, true_counts[result]/len(naive_list))

>>> q: 0.1, result: 52, true quantile: 0.102751677852349
q: 0.2, result: 65, true quantile: 0.20570469798657717
q: 0.4, result: 85, true quantile: 0.4083892617449664
q: 0.5, result: 93, true quantile: 0.504496644295302
q: 0.6, result: 102, true quantile: 0.6025503355704698
q: 0.9, result: 139, true quantile: 0.9030201342281879

```

### + operator

`sketch1 + sketch2` return the merged sketch of `sketch1` and `sketch2`. 
 In other words, A = A + B is the same as A.merge(B).


