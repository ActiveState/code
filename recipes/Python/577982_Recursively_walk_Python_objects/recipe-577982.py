from collections import Mapping, Set, Sequence 

# dual python 2/3 compatability, inspired by the "six" library
string_types = (str, unicode) if str is bytes else (str, bytes)
iteritems = lambda mapping: getattr(mapping, 'iteritems', mapping.items)()

def objwalk(obj, path=(), memo=None):
    if memo is None:
        memo = set()
    iterator = None
    if isinstance(obj, Mapping):
        iterator = iteritems
    elif isinstance(obj, (Sequence, Set)) and not isinstance(obj, string_types):
        iterator = enumerate
    if iterator:
        if id(obj) not in memo:
            memo.add(id(obj))
            for path_component, value in iterator(obj):
                for result in objwalk(value, path + (path_component,), memo):
                    yield result
            memo.remove(id(obj))
    else:
        yield path, obj

# optional test code from here on
import unittest

class TestObjwalk(unittest.TestCase):
    def assertObjwalk(self, object_to_walk, *expected_results):
        return self.assertEqual(tuple(sorted(expected_results)), tuple(sorted(objwalk(object_to_walk))))
    def test_empty_containers(self):
        self.assertObjwalk({})
        self.assertObjwalk([])
    def test_single_objects(self):
        for obj in (None, 42, True, "spam"):
            self.assertObjwalk(obj, ((), obj))
    def test_plain_containers(self):
        self.assertObjwalk([1, True, "spam"], ((0,), 1), ((1,), True), ((2,), "spam"))
        self.assertObjwalk({None: 'eggs', 'bacon': 'ham', 'spam': 1},
                           ((None,), 'eggs'), (('spam',), 1), (('bacon',), 'ham'))
        # sets are unordered, so we dont test the path, only that no object is missing
        self.assertEqual(set(obj for path, obj in objwalk(set((1,2,3)))), set((1,2,3)))
    def test_nested_containers(self):
        self.assertObjwalk([1, [2, [3, 4]]],
                           ((0,), 1), ((1,0), 2), ((1, 1, 0), 3), ((1, 1, 1), 4))
        self.assertObjwalk({1: {2: {3: 'spam'}}},
                           ((1,2,3), 'spam'))
    def test_repeating_containers(self):
        repeated = (1,2)
        self.assertObjwalk([repeated, repeated],
                           ((0, 0), 1), ((0, 1), 2), ((1, 0), 1), ((1, 1), 2))
    def test_recursive_containers(self):
        recursive = [1, 2]
        recursive.append(recursive)
        recursive.append(3)
        self.assertObjwalk(recursive, ((0,), 1), ((1,), 2), ((3,), 3))

if __name__ == '__main__':
    unittest.main()
