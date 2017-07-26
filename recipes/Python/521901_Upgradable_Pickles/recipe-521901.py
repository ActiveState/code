import pickle

class Upgradable:
    class_version = '3.0'
    def __init__(self):
        self.version = self.__class__.class_version
        self.new_attr = 42

    def pickle(self):
        return pickle.dumps(self)

    def new_method(self):
        '''
        Return the answer to life the universe and everything.
        Would normally break pickles prior to the introduction of new_attr.
        '''
        return self.new_attr
    
    @staticmethod
    def unpickle(data):
        out = pickle.loads(data)
        if not hasattr(out, 'version'):
            out.version = '0.0'
        if out.version != out.class_version:
            out.upgrade()
        return out
    
    def upgrade(self):
        version = float(self.version)
        print 'upgrade from version %s' % self.version
        if version < 1.:
            self.version = '1.0'
            print 'upgrade to version 1.0'
        if version < 2.:
            self.version = '2.0'
            print 'upgrade to version 2.0'
        if version < 3.:
            self.version = '3.0'
            self.new_attr = 42 
            print 'upgrade to version 3.0'
            
def __test__():
    ug0 = Upgradable()
    # downgrade to lower version
    del ug0.version
    del ug0.new_attr

    try:
        # breaks old pickles!
        ug0.new_method()
        raise Exception('Should have raised AttributeError!')
    except AttributeError:
        pass

    # check to see if automatic upgrade works
    ug3 = ug0.unpickle(ug0.pickle())
    assert ug3.version == '3.0'
    assert ug3.new_attr == 42
    assert ug3.new_method() == 42

__test__()
