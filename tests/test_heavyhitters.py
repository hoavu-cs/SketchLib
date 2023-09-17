import unittest
from collections import Counter
import random
from sketchlib.heavy_hitters import CountMinCashRegister, MisraGries

class TestHeavyHitters(unittest.TestCase):

    def test_count_min_cash_register(self):
        cash_register = CountMinCashRegister(phi=0.3, epsilon=0.1)
        
        # Tokens that should be heavy hitters
        heavy_tokens = ['apple'] * 60000
        heavy_tokens += ['orange'] * 60000
        # Tokens that should not be heavy hitters
        light_tokens = ['banana'] * 20000
        light_tokens += ['mango'] * 20000
        light_tokens += ['banana'] * 20000
        light_tokens += ['kiwi'] * 20000

        # Mix and insert tokens
        tokens = heavy_tokens + light_tokens
        random.shuffle(tokens)
        for token in tokens:
            cash_register.insert(token, 1)
        
        heavy_hitters = cash_register.get_heavy_hitters()
        
        self.assertIn('apple', heavy_hitters)
        self.assertNotIn('banana', heavy_hitters)

    def test_misra_gries(self):
        misra = MisraGries(phi=0.3, epsilon=0.01)
        
        # Tokens that should be heavy hitters
        heavy_tokens = ['apple'] * 60000
        heavy_tokens += ['orange'] * 60000
        # Tokens that should not be heavy hitters
        light_tokens = ['banana'] * 20000
        light_tokens += ['mango'] * 20000
        light_tokens += ['banana'] * 20000
        light_tokens += ['kiwi'] * 20000

        # Mix and insert tokens
        tokens = heavy_tokens + light_tokens
        random.shuffle(tokens)
        for token in tokens:
            misra.insert(token)
        
        heavy_hitters = misra.get_heavy_hitters()

        self.assertIn('apple', heavy_hitters)
        self.assertNotIn('banana', heavy_hitters)

    def test_count_min_cash_register_merge(self):
        cash_register1 = CountMinCashRegister(phi=0.3, epsilon=0.1)
        cash_register2 = CountMinCashRegister(phi=0.3, epsilon=0.1)

        cash_register1.insert('apple', 40000)
        cash_register1.insert('banana', 10000)

        cash_register2.insert('apple', 20000)
        cash_register2.insert('orange', 50000)

        merged_register = cash_register1 + cash_register2
        heavy_hitters = merged_register.get_heavy_hitters()

        self.assertIn('apple', heavy_hitters)
        self.assertIn('orange', heavy_hitters)
        self.assertNotIn('banana', heavy_hitters)

    def test_misra_gries_merge(self):
        misra1 = MisraGries(phi=0.3, epsilon=0.01)
        misra2 = MisraGries(phi=0.3, epsilon=0.01)

        for _ in range(40000):
            misra1.insert('apple')
        for _ in range(10000):
            misra1.insert('banana')

        for _ in range(20000):
            misra2.insert('apple')
        for _ in range(50000):
            misra2.insert('orange')

        misra1.merge(misra2)
        heavy_hitters = misra1.get_heavy_hitters()

        self.assertIn('apple', heavy_hitters)
        self.assertIn('orange', heavy_hitters)
        self.assertNotIn('banana', heavy_hitters)


if __name__ == "__main__":
    unittest.main()
