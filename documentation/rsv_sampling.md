## Reservoir Sampling

This class provides an implementation of reservoir sampling in a data stream. To import the class, use the following

```python
from sketchlib.rsv_sampling import RsvSampling
```

### overview

The class uses reservoir sampling to maintain k tokens uniformly sampled at random from a data stream of unknown length. The update time for each new token is constant, and the memory use is proportional to k times the size of a token.

### initialization

To create a reservoir sampler, specify the desired sample size during initialization.

```python
sampler = RsvSampling(rsv_size = 1000)
```

### insert

Insert a token into the data stream.

```python
n = 1000
sampler = RsvSampling(rsv_size = 10)
for i in range(n):
    sampler.insert(i)
```

### reservoir

Return the tokens sampled uniformly at random from the data stream observed so far.

```python
n = 1000
sampler = RsvSampling(rsv_size = 10)
for i in range(n):
    sampler.insert(i)
for i in sampler.reservoir():
    print(i)

>>> 31
473
487
510
203
748
157
942
268
382
```

### merge

Merge two samplers with the same reservoir size say k. 
The merged sampler will k elements sampled uniformly at random from the combined stream.

```python
n = 1000
sampler = RsvSampling(rsv_size = 10)
sampler2 = RsvSampling(rsv_size = 10)
for i in range(n):
    sampler.insert(i)
for i in range(2*n):
    sampler2.insert(i)
sampler.merge(sampler2)
```

### + operator

A + B returns the combined sampler of two sampler with the same reservoir size.
In other words, A = A+B is the same as A.merge(B). 

```python
n = 1000
sampler = RsvSampling(rsv_size = 10)
sampler2 = RsvSampling(rsv_size = 10)
for i in range(n):
    sampler.insert(i)
for i in range(2*n):
    sampler2.insert(i)
sampler = sampler + sampler2
```