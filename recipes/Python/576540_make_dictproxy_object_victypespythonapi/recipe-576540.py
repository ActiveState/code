__all__ = ['dictproxy', 'make_dictproxy']

from ctypes import pythonapi, py_object
from _ctypes import PyObj_FromPtr

PyDictProxy_New = pythonapi.PyDictProxy_New
PyDictProxy_New.argtypes = (py_object,)
PyDictProxy_New.rettype = py_object


def make_dictproxy(obj):
    assert isinstance(obj,dict)
    return PyObj_FromPtr(PyDictProxy_New(obj))
    
## make_dictproxy = lambda dictobj: type('',(),dictobj).__dict__

# for isinstance() check
dictproxy = type(make_dictproxy({}))


if __name__ == '__main__':

    import unittest
    
    class DictProxyTestCase(unittest.TestCase):
        
        def test_instance(self):
            d = make_dictproxy({})
            self.assertTrue(isinstance(d,dictproxy))
            self.assertFalse(isinstance(d.copy(),dictproxy))

        def test_get(self):
            d = make_dictproxy({'a': 'b', 'c': 'd'})
            self.assertEqual('b', d.get('a'))
            self.assertEqual('d', d.get('c'))
            
        def test_set(self):
            d = make_dictproxy({})
            def _test_item_assignment():
                d['a'] = 10
            self.assertRaises(TypeError, _test_item_assignment)
            
        def test_copy(self):
            d1 = make_dictproxy({'a': 'b', 'c': 'd'})
            d2 = d1.copy()
            self.assertEqual(d1, d2)
            self.assertTrue(isinstance(d2,dict))
            d2['a'] = 'z'
            self.assertNotEqual(d1, d2)
            self.assertEqual('z', d2['a'])
    
        def test_not_immutable(self):
            a = dict(val=20)
            b = make_dictproxy(a)
            a['val'] = 10
            self.assertEqual(10, b['val'])
            # This is ok, correct behavior.
            # So ... can/should not use dictproxy as immutable dict.
            # dictproxy just hide the interface.

    unittest.main()
    
