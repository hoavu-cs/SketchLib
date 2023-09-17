import unittest
import random
import string
from sketchlib.f2_estimate import F2Estimate

class TestF2Estimate(unittest.TestCase):

    def random_string(self, length=10):
        """Generate a random string of a given length."""
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))

    def test_basic_functionality(self):
        epsilon = 0.05
        f2 = F2Estimate(epsilon=epsilon, delta=0.01)

        # Number of iterations and the second frequency moment
        N = 1000
        freq_moment = 0

        # Weight dictionary to hold the weights (counts) of each element
        weight_dict = {}

        # Insert N distinct elements with random weights
        for _ in range(N):
            element = self.random_string()
            weight = random.randint(1, 10)
            
            weight_dict[element] = weight
            f2.insert(element, weight)

            freq_moment += weight ** 2

        # Get the estimated second frequency moment
        estimated_moment = f2.estimator()

        # Check whether the estimate is within (1±ε) factor of the actual value
        lower_bound = freq_moment * (1 - epsilon)
        upper_bound = freq_moment * (1 + epsilon)

        self.assertTrue(lower_bound <= estimated_moment <= upper_bound)

    def test_merge_functionality(self):
        epsilon = 0.05
        f2_1 = F2Estimate(epsilon=epsilon, delta=0.01)
        f2_2 = F2Estimate.from_existing(f2_1)

        # Frequency moment for each sketch
        freq_moment_1 = 0
        freq_moment_2 = 0

        # Insert elements into f2_1
        for _ in range(500):
            element = self.random_string()
            weight = random.randint(1, 10)
            f2_1.insert(element, weight)
            freq_moment_1 += weight ** 2

        # Insert elements into f2_2
        for _ in range(500):
            element = self.random_string()
            weight = random.randint(1, 10)
            f2_2.insert(element, weight)
            freq_moment_2 += weight ** 2

        # Merge the sketches
        f2_1.merge(f2_2)

        # Total frequency moment
        total_moment = freq_moment_1 + freq_moment_2

        # Estimate after merging
        estimated_moment = f2_1.estimator()

        # Check the estimate
        lower_bound = total_moment * (1 - epsilon)
        upper_bound = total_moment * (1 + epsilon)

        self.assertTrue(lower_bound <= estimated_moment <= upper_bound)

    def test_skewed_distribution(self):
        epsilon = 0.05
        f2 = F2Estimate(epsilon=epsilon, delta=0.01)

        # Skewed weights for three distinct elements
        skewed_weights = {'item1': 700, 'item2': 200, 'item3': 100}

        # Frequency moment calculation
        freq_moment = 0
        for item, weight in skewed_weights.items():
            f2.insert(item, weight)
            freq_moment += weight ** 2

        # Estimation
        estimated_moment = f2.estimator()

        # Check the estimate
        lower_bound = freq_moment * (1 - epsilon)
        upper_bound = freq_moment * (1 + epsilon)
        #print(estimated_moment, lower_bound, upper_bound)
        self.assertTrue(lower_bound <= estimated_moment <= upper_bound)

if __name__ == '__main__':
    unittest.main()
