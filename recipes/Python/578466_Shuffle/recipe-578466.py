import random
import unittest

def shuffle(cards):
    max = len(cards)-1
    while max != 0:
        r = random.randint(0, max)
        cards[r], cards[max] = cards[max], cards[r]
        max = max - 1
    return cards

class TestCase(unittest.TestCase):
    def setUp(self):
        self.actual = range(1, 53)

    def test_elements(self):
        expected = shuffle(self.actual)
        self.assertEqual(set(self.actual), set(expected))

if __name__ == "__main__":
    unittest.main()
