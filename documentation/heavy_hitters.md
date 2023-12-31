## Heavy Hitters  
  
This class provides a space and time efficient data structure to find the most frequent elements of a data stream. 
All elements that occur at least `phi * m` times are returned (where `m` is the length of the stream), while elements that occur less than`(phi - epsilon) * m` times are ignored. 
  
Currently, there are two classes CountMinCashRegister and MisraGries that implement the heavy hitters algorithm. 

CountMinCashRegister is an implementation of the heavy hitters algorithm using the Count-Min sketch data structure by Graham Cormode and S. Muthukrishnan in the cash register model. 
Count-Min sketch might return some incorrect heavy hitters with probability `delta`. Count-Min sketch can work with non-integer counts. 

MisraGries is an implementation of the heavy hitters algorithm using the Misra-Gries sketch data structure by J. Misra and David Gries.
Misra-Gries sketch is deterministic and will always return the correct heavy hitters. However, it can only work with integer counts.
If you work with non-integer counts or large integer counts, it is also recommended to use CountMinCashRegister instead as Misra-Gries.


To import the class, use the following:  
  
```python  
from sketchlib.heavy_hitters import CountMinCashRegister 
```  

or 

```python
from sketchlib.heavy_hitters import MisraGries
```


### Overview  
  
These support the following operations:  
  
- insert a token and count (default is 1) as encountered in the data stream. 
- return all heavy hitter elements and their approximate counts. 
- combine the sketches of two streams so that we can find all the heavy hitters in the combined stream.  
  
### Initialization  
  
To initialize an instance of this class, we can specify the following parameters:  

  -`phi`: defines the cutoff for what constitutes a heavy hitter. The default value is `0.05`.
 - `epsilon`: controls margin of error within which false positives are permitted. 
 - `delta`: controls the failure probability. The default value is `0.01` (for CountMinCashRegister only). 
 - `seed`: the seed for randomness. The default value is `42`.

  
```python  
cash_register = CountMinCashRegister(phi=0.3, epsilon=0.1)
```  
  
### insert  
  
Insert a new token into the sketch. The token must be byte-like objects. The easiest way to achieve this is to convert a token to string.  By default, items are inserted with a count of 1. However, this can be easily overridden in cases where each token has an associated count (such as a sales quantity).

For example,  
  
  
```python  
cash_register = CountMinCashRegister(phi=0.01, epsilon=0.2, delta=0.01)  
cash_register.insert("apple")  
cash_register.insert("orange", 10)  
cash_register.insert("apple", 5)  
```

For MisraGries, the count must be a positive integer.


### get_heavy_hitters
Returns a dictionary of all the heavy-hitters that have appeared in the stream so far along with an estimated count for each.
Recall that all elements that occur at least `phi * m` times are returned (where `m` is the length of the stream), while elements that occur less than`(phi - epsilon) * m` times are ignored. 

For CountMinCashRegister, the estimate is within a factor of `(1 + epsilon)` with probability `1 - delta` of the true count.
For MisraGries, the estimate is within a factor of `(1 - epsilon)` of the true count.

  
For example,  
```python
stream = CountMinCashRegister(phi=0.01, epsilon=0.2)  
  
stream.insert("heavy-hitter", 10000)  
stream.insert("lightweight", 1)
  
print(stream.get_heavy_hitters())  

>>> {'heavy-hitter': 10000}

```  
  
### merge  
  
Merge with another sketch with the same initialization parameters. The resulted sketch will provide answer to the combined stream.  
  
For example,  
  
```python  
stream = CountMinCashRegister(delta=0.01, epsilon=0.05, seed=42)  
stream2 = CountMinCashRegister(delta=0.01, epsilon=0.05, seed=42)  

stream.insert("heavy-hitter", 10000)  
stream.insert("lightweight", 1)

stream2.insert("other heavy-hitter", 8000)  
stream2.insert("lightweight", 1)
  
stream.merge(stream2)  
print(stream.get_heavy_hitters())  
  
>>> {'heavy-hitter': 10000, 'other heavy-hitter': 8000} 
  
```  
  
### + operator  
  
If A is a sketch of some stream and B is a sketch of another stream, then A + B returns the merged sketch that provides the answer to the combined stream. 
In other words, A = A+B is the same as A.merge(B).   
  
For example,  
  
```python  
stream = CountMinCashRegister(delta=0.01, epsilon=0.05, seed=42)  
stream2 = CountMinCashRegister(delta=0.01, epsilon=0.05, seed=42)  

stream.insert("heavy-hitter", 10000)  
stream.insert("lightweight", 1)

stream2.insert("other heavy-hitter", 8000)  
stream2.insert("lightweight", 1)
  
stream = stream + stream2  
print(stream.get_heavy_hitters())  
  
>>> {'heavy-hitter': 10000, 'other heavy-hitter': 8000} 
  
```  
  
### from_existing   
Create a new sketch with similar parameters so that they can be merged later.  
  
For example,  

```python
stream = CountMinCashRegister(delta=0.01, epsilon=0.05, seed=42)  
stream2 = CountMinCashRegister.from_existing(stream)

stream.insert("heavy-hitter", 10000)  
stream.insert("lightweight", 1)

stream2.insert("other heavy-hitter", 8000)  
stream2.insert("lightweight", 1)
  
stream = stream + stream2  
print(stream.get_heavy_hitters())  
  
>>> {'heavy-hitter': 10000, 'other heavy-hitter': 8000} 

```