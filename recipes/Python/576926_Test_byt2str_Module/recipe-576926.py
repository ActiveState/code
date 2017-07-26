import byt2str
import unittest
from test import support

class ConvertTest(unittest.TestCase):

    def test_min(self):
        # Check that the "convert" min range is correct.
        self.assertEqual(byt2str.convert(1), '1 Byte')
        with self.assertRaises(AssertionError):
            byt2str.convert(0)

    def test_max(self):
        # Test the max range for "convert" for errors.
        prefix = ('geop', 'bronto', 'yotta', 'zetta', 'exa',
                  'peta', 'tera', 'giga', 'mega', 'kilo', '')
        suffix = map(lambda s: '1023 ' + (s + 'bytes').capitalize(), prefix)
        self.assertEqual(byt2str.convert((1 << 110) - 1), ', '.join(suffix))
        with self.assertRaises(AssertionError):
            byt2str.convert(1 << 110)

    def test_ternary(self):
        # Ensure that three separate components validate.
        string = byt2str.convert((1 << 40) + (1 << 20) * 123 + 456)
        self.assertEqual(string, '1 Terabyte, 123 Megabytes, 456 Bytes')

    def test_binary(self):
        # Observe if two non-contiguous numbers render well.
        string = byt2str.convert(789 * (1 << 30) + (1 << 10))
        self.assertEqual(string, '789 Gigabytes, 1 Kilobyte')

class PartitionTest(unittest.TestCase):

    def setUp(self):
        # Create test cases for child classes.
        self.numbers = (1, 2, 4, 6, 8, 10, 16,
                        32, 36, 64, 100, 128,
                        216, 256, 512, 1000)

    def test_base(self):
        # Execute a series of tests for children.
        for number, result in zip(self.numbers, self.results):
            answer = list(byt2str.partition_number(number, self.pn_base))
            self.assertListEqual(answer, result)

class BaseTwoTest(PartitionTest):

    def setUp(self):
        # Create variables to test against in base two.
        super().setUp()
        self.pn_base = 2
        self.results = ([1],
                        [0, 1],
                        [0, 0, 1],
                        [0, 1, 1],
                        [0, 0, 0, 1],
                        [0, 1, 0, 1],
                        [0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 1],
                        [0, 0, 1, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 1, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 1, 1, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 1, 0, 1, 1, 1, 1, 1])

class BaseSixTest(PartitionTest):

    def setUp(self):
        # Setup parameters for the base six test.
        super().setUp()
        self.pn_base = 6
        self.results = ([1],
                        [2],
                        [4],
                        [0, 1],
                        [2, 1],
                        [4, 1],
                        [4, 2],
                        [2, 5],
                        [0, 0, 1],
                        [4, 4, 1],
                        [4, 4, 2],
                        [2, 3, 3],
                        [0, 0, 0, 1],
                        [4, 0, 1, 1],
                        [2, 1, 2, 2],
                        [4, 4, 3, 4])

class BaseTenTest(PartitionTest):

    def setUp(self):
        # Create some data needed for testing base ten.
        super().setUp()
        self.pn_base = 10
        self.results = ([1],
                        [2],
                        [4],
                        [6],
                        [8],
                        [0, 1],
                        [6, 1],
                        [2, 3],
                        [6, 3],
                        [4, 6],
                        [0, 0, 1],
                        [8, 2, 1],
                        [6, 1, 2],
                        [6, 5, 2],
                        [2, 1, 5],
                        [0, 0, 0, 1])

class BytesTest(unittest.TestCase):

    def test_ascending(self):
        # See if bytes are computed correctly while ascending.
        example = ('0 Bytes',
                   '1 Kilobyte', '2 Megabytes', '3 Gigabytes',
                   '4 Terabytes', '5 Petabytes', '6 Exabytes',
                   '7 Zettabytes', '8 Yottabytes', '9 Brontobytes',
                   '10 Geopbytes')
        results = tuple(byt2str.format_bytes(range(0, 11, 1)))
        self.assertTupleEqual(results, example)

    def test_descending(self):
        # Check that strings for descending numbers are valid.
        example = ('10 Bytes',
                   '9 Kilobytes', '8 Megabytes', '7 Gigabytes',
                   '6 Terabytes', '5 Petabytes', '4 Exabytes',
                   '3 Zettabytes', '2 Yottabytes', '1 Brontobyte',
                   '0 Geopbytes')
        results = tuple(byt2str.format_bytes(range(10, -1, -1)))
        self.assertTupleEqual(results, example)

class SuffixTest(unittest.TestCase):

    def test_prefix(self):
        # Ensure that each prefix is selected correctly.
        example = ['Byte', 'Kilobyte', 'Megabyte', 'Gigabyte',
                   'Terabyte', 'Petabyte', 'Exabyte', 'Zettabyte',
                   'Yottabyte', 'Brontobyte', 'Geopbyte']
        results = [byt2str.format_suffix(power, 1) for power in range(11)]
        self.assertListEqual(results, example)

    def test_plural(self):
        # Test a range of numbers for the number of the word.
        example = ['Bytes', 'Bytes', 'Byte', 'Bytes', 'Bytes']
        results = [byt2str.format_suffix(0, number) for number in range(-1, 4)]
        self.assertListEqual(results, example)

def test_main():
    support.run_unittest(ConvertTest, BytesTest, SuffixTest,
                         BaseTwoTest, BaseSixTest, BaseTenTest)

if __name__ == '__main__':
    test_main()
