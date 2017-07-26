#
# version: 1  (2004-03-05)
#

class ObjectMerger:
    """
    Object 'Merger'.
    
    Returns an instance that takes methods from two given instances/objects. 
    In order, as if one have the subclass methods of the other.
    """
    def __init__(self, super, _self):
        self.___super = super
        self.___self = _self
        
    def __getattr__ ( self, name ):
        if not name.startswith('___'):
            super = self.___super
            _self = self.___self
            if hasattr(_self, name):
                return getattr(_self, name)
            elif hasattr(super, name):
                return getattr(super, name)
            
        return getattr(ObjectMerger, name)
    
    
if __name__=='__main__':
    import unittest
    
    class test1:
        def a(self): pass
        def b(self): pass
        
    class test2:
        def a(self): pass
        def c(self): pass
    
    class testObjectMerger(unittest.TestCase):
        def test_merged_instances_method_priority (self):
            """Test priority of methods"""
            c1 = test1()
            c2 = test2()
            m = ObjectMerger(c1, c2)
            self.assertEqual(m.a, c2.a)
            self.assertEqual(m.b, c1.b)
            self.assertEqual(m.c, c2.c)
            
        def test_merged_objects_with_one_noninstance (self):
            """Test mix of instance and object(string)"""
            c1 = test1()
            c2 = 'hola carlos'
            m = ObjectMerger(c1, c2)
            self.assertEqual(m.a, c1.a)
            #can't compare functions directly because:
            #   1. it seems that after first get function is copied..
            #       or something
            #   2. don't know why python fails comparing the function..
            self.assertEqual(m.__len__(), c2.__len__())
            self.assertEqual(m.b, c1.b)

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testObjectMerger))
    unittest.TextTestRunner(verbosity=2).run(suite)
