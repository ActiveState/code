    def range_comparison(op, checks, value, default=None):
        """
        An extensible ternary operator
        Takes an operator such as op.lt
        checks are tuples of sentinel values and results and must be supplied in
        the right order to suit the operator and prevent it matching greedily.
        ie. with lt checks must be in ascending order and descending or for gt
        """
        for sentinel, result in checks:
            if op(value, sentinel):
                return result
        return default

    class TestRangeComparison(TestCase):
    
        def make_one(self):
            from ..utils import range_comparison
            return range_comparison
    
        def test_lt(self):
            from operator import lt
            FUT = self.make_one()
            checks = [(10, "less than 10"),
                      (20, "less than 20"),
                      (100, "less than 100")]
            self.assertEqual(FUT(lt, checks, 5), "less than 10")
            self.assertEqual(FUT(lt, checks, 10), "less than 20")
            self.assertEqual(FUT(lt, checks, 50), "less than 100")
            self.assertFalse(FUT(lt, checks, 100))
