class ListenableSet(set):
    '''A set that notifies listeners whenever it is updated

    Callback order and signature:

        for cb in self.listeners:  cb(self)

    '''

    def __init__(self, *args, **kwds):
        self._listeners = []
        set.__init__(self, *args, **kwds)

    def notify(self):
        'Run all the callbacks in self.listeners.'
        for cb in self._listeners:
            cb(self)

    @property
    def listeners(self):
        'Read-only access to _listeners'
        return self._listeners

    def _detect_size_change(methodname, parent):
        method = getattr(parent, methodname)
        def wrapper(self, *args, **kwds):
            original_size = len(self)
            result = method(self, *args, **kwds)
            if len(self) != original_size:
                for cb in self._listeners:
                    cb(self)
            return result
        wrapper.__name__ = methodname
        wrapper.__doc__ = method.__doc__
        return wrapper

    def _detect_any_call(methodname, parent):
        method = getattr(parent, methodname)
        def wrapper(self, *args, **kwds):
            result = method(self, *args, **kwds)
            for cb in self._listeners:
                cb(self)
            return result
        wrapper.__name__ = methodname
        wrapper.__doc__ = method.__doc__
        return wrapper

    for methodname in 'clear add pop discard remove update difference_update ' \
                      '__isub__ __iand__ __ior__ intersection_update'.split():
        locals()[methodname] = _detect_size_change(methodname, set)
    for methodname in '__ixor__ symmetric_difference_update'.split():
        locals()[methodname] = _detect_any_call(methodname, set)



# ---- Example callback to print information on size -------------------------

def notice(s):
    print 'Set at %d now has size %d\n' % (id(s), len(s))

s = ListenableSet('abcdefgh')
s.listeners.append(notice)
s.add('i')      # adding a new element changes the set and triggers a callback
s.add('a')      # adding an existing element results in no change or callback
s.listeners.remove(notice)
s.add('j')      # without a listener, works just like a regular set


# ---- Example callback to report changes in the set -------------------------

def change_report(s, prev=set()):
    added = s - prev
    if added:
        print 'Added elements: ', list(added)
    removed = prev - s
    if removed:
        print 'Removed elements: ', list(removed)
    if added or removed:
        print
    prev.clear()
    prev.update(s)

s = ListenableSet()
s.listeners.append(change_report)
s.update('abracadabra')
s ^= set('simsalabim')


# ---- Example callback to enforce a set invariant ---------------------------

def enforce_lowercase(s):
    for elem in s:
        if not elem.islower():
            raise ValueError('Set member must be lowercase: ' + repr(elem))

s = ListenableSet()
s.listeners.append(enforce_lowercase)
s.add('slartibartfast')
s.add('Bang')   # Raises an exception because the set element isn't lowercase
