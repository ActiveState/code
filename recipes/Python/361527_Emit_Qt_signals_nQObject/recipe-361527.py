import qt
import weakref

_emitterCache = weakref.WeakKeyDictionary()

def emitter(ob):
    """Returns a QObject surrogate for *ob*, to use in Qt signaling.

    This function enables you to connect to and emit signals from (almost)
    any python object with having to subclass QObject.

      >>> class A(object):
      ...   def notify(self, *args):
      ...       QObject.emit(emitter(self), PYSIGNAL('test'), args)
      ...
      >>> ob = A()
      >>> def myhandler(*args): print 'got', args
      ...
      >>> QObject.connect(emitter(ob), PYSIGNAL('test'), myhandler)
      ... True
      >>> ob.notify('hello')
      got ('hello',)

      >>> QObject.emit(emitter(ob), PYSIGNAL('test'), (42, 'abc',))
      got (42, 'abc')
    """

    if ob not in _emitterCache:
        _emitterCache[ob] = qt.QObject()
    return _emitterCache[ob]
