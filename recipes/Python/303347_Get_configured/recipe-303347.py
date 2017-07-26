# since Python 2.2 we can directly inherit from
# the builtin type/class 'dict'

class BunchDict(dict):

    # since Python 2.3 this __new__-method could be omitted
    def __new__(cls,**kwds):
        return dict.__new__(cls, kwds)

    def __getattr__(self, attr):
        "Provide attribute access to retrieve dictionary items."
        
        # in case of error AttributeError is to be
        # raised instead of KeyError
        try:
            return self[attr]
        except KeyError:
            raise AttributeError, ("'%s' instance has no attribute '%s'" %
                                   (self.__class__.__name__, attr))

    def __setattr__(self, attr, val):
        "Provide attribute access to store dictionary items."
        self[attr] = val


class CfgBunch(BunchDict):
    "A class able to represent itself as Python source."

    def lines(self, _instancename=None, _classname=None, indentwidth=4):
        """Return a Python source representation."""
        _instancename = (_instancename or
                         self.get("_instancename",
                                  "a%s" % self.__class__.__name__))
        _classname = (_classname or
                      self.get("_classname", None) or
                      self.__class__.__name__)
        keys = self.keys()
        keys.sort()
        result = []
        result.append(("%s = %s(\n" ) % (_instancename, _classname)) 
        for k in keys:
            result.append( "%*s%s = %r,\n" % (indentwidth,' ',k, self[k]))
        result.append("%*s)" % (indentwidth,' '))
        return result

    def __str__(self):
        return "".join(self.lines())

    def __repr__(self):
        return "".join(self.lines())


if __name__=="__main__":
    
    if 1 and "example use of CfgBunch()":

        # handy initialization via keyword parameters
        cfg = CfgBunch(host="localhost", db="test",
                       user="test", passwd="test")

        # handy item access
        host = cfg.host

        # is otherwiese dictionary-like
        if cfg['host'] == cfg.user:
            "Hui?"

        # raise "KeyError: tralala"
        try:
            cfg['tralala']
        except KeyError:
            pass

        # raise "AttributeError: 'CfgBunch' instance has no attribute 'tralala'"
        try:
            cfg.tralala
        except AttributeError:
            pass

        # store new item
        cfg.one = 1

        # representation as well readable Python source
        print cfg
        #>>> print cfg
        #aCfgBunch = CfgBunch(
        #    db = 'test',
        #    host = 'localhost',
        #    one = 1,
        #    passwd = 'test',
        #    user = 'test',
        #    )        


if __name__=="__main__":

    if 1 and "how to organize your main program":

        class BigWorkerClass(object):
            """
            This class stands as an example for a big
            independent class. It receives a reference
            to the 'Main' instance providing access to
            all its attributes. Notice the readability:
            its easy to recognize that 'self.main.cfg.talk'
            refers to the same parameter as 'self.cfg.talk'
            in the 'main'-instance.
            """

            def __init__(self,main):
                self.main = main
                if self.main.cfg.talk:
                    "Yeah!"

        class Main(object):

            def __init__(self,**kwds):
                defaults = {"talk":0}
                self.cfg = CfgBunch(**defaults)
                self.cfg.update(kwds)
                self.cfg._instancename = 'Main.cfg'
                self.cfg_connection = CfgBunch(host="localhost",user="test",
                                     _instancename="Main.cfg_connection")
                # pass self.cfg around
                # even more complete: we pass 'self' directly
                self.bwc = BigWorkerClass(self) # notice the (self)!

            def work(self):
                # use parameters
                if self.cfg.talk:
                    "talk!"

                # access the same parameter, demonstrating readability
                # consistent naming counts!
                if self.bwc.main.cfg.talk:
                    "as I said"

            def explain(self):
                print "#"
                print "# configuration:"
                print "#"
                print self.cfg
                print self.cfg_connection

            def done(self):
                ""
                
        if __name__=="__main__":

            M = Main(talk=1, adhoc_param="nobody is expecting me")
            M.explain()
            M.work()
            M.done()
            
            # ### printout from M.explain()
            # #
            # # configuration:
            # #
            # Main.cfg = CfgBunch(
            #     _instancename = 'Main.cfg',
            #     adhoc_param = 'nobody is expecting me',
            #     talk = 1,
            #     )
            # Main.cfg_connection = CfgBunch(
            #     _instancename = 'Main.cfg_connection',
            #     host = 'localhost',
            #    user = 'test',
            #     )
