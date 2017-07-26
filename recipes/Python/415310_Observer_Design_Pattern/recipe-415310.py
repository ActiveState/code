from weakref import ref

class Event(object):
    def __init__(self, name, stuff=None):
        self.name = name
        self.stuff = stuff

    def __str__(self):
        return '%s(%s)'%(self.name,self.stuff)

class Observer(object):
    listeners={}
    weakListeners={}
    
    def register(self, eventName, callback, isWeak=False):
        if not isWeak: listenDict = Observer.listeners
        else: listenDict = Observer.weakListeners
        callbacks = listenDict.get(eventName)
        if not callbacks:
            callbacks = []
            listenDict[eventName] = callbacks
        if not isWeak and callback not in callbacks:
            callbacks.append(callback)
        elif isWeak:
            for cb in callbacks:
                refobj = cb()
                if refobj and refobj==callback:
                    return
            callbacks.append(ref(callback))

    def unregister(self, eventName, callback, isWeak=False):
        if not isWeak: listenDict = Observer.listeners
        else: listenDict = Observer.weakListeners
        callbacks = listenDict.get(eventName)
        if callbacks:
            if not isWeak:
                try: callbacks.remove(callback)
                except: pass
            else:
                cblist = []; cblist.extend(callbacks)
                for cb in cblist:
                    refobj = cb()
                    if refobj and refobj==callback:
                        callbacks.remove(cb)
                    elif not refobj:
                        callbacks.remove(cb)

    def fireEvent(self, event):
        if not event: return
        callbacks = []
        callbacks.extend(Observer.listeners.get(event.name,[]))
        for cb in Observer.weakListeners.get(event.name,[]): callbacks.append(cb())
        for cb in callbacks:
            if cb: cb(event)

    def fireEventName(self, name, stuff=None):
        self.fireEvent(Event(name,stuff))

observer = Observer()
