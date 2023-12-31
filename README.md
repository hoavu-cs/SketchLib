
# SketchLib

This package contains various streaming algorithms that are useful for processing massive scale data. For example, for calculating heavy-hitters in a data stream, implementations of the Misra-Gries and Count-Min algorithms are available. The problems that can be solved using this package include F0 and F2 estimation as well as set-membership inquiries (Bloom Filter).  Currently, we support the following algorithms:

- Heavy Hitters (Misra-Gries, Count-Min)
- Distinct Counting
- F2 Estimation
- Quantile Sketch
- Bloom Filter
- Minhash
- Reservoir Sampling

You will need mmh3, a fast non-cryptographic hash function, to use this package. You can install it using `pip install mmh3`.

Contributor: Hoa Vu 

Past contributor: Daniel Barnas.

