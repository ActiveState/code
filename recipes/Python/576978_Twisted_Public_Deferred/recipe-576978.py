'''
@author: Alan Franzoni <public@MYSURNAME.eu>
'''
from twisted.internet.defer import Deferred

class ShouldntBecalledError(Exception):
    pass
     
class PublicDeferred(Deferred):
    """
    PublicDeferred decorator.

    Prevents calling methods which should be just be called by the "real"
    deferred object owner. If such calls occur, an error is immediately raised.
    """
    
    def __init__(self, original_d):
        self.__dict__ = original_d.__dict__ 
        
    def callback(self, result):
        raise ShouldntBecalledError, "callback() should only be called by the owner!"
    
    def errback(self, failuire):
        raise ShouldntBecalledError, "errback() should only be called by the owner!"
        
if __name__ == '__main__':
    """
    example usage:
    if you don't want somebody to mess up with your internals, do what you need
    with your deferred and wrap it into a PublicDeferred before returning it.
    """
    from twisted.internet import reactor
    from twisted.web.client import getPage
    
    def publicGetPage(*args, **kwargs):
        d = getPage(*args, **kwargs)
        return PublicDeferred(d)
    
    def printResult(result):
        print result
    
    d = publicGetPage("http://www.google.com")
    d.addCallback(printResult)
    reactor.callLater(0, d.callback, "hello, there!")
    
    reactor.run()
    
    
    
    
    
