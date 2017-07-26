#!/usr/bin/env python
                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                         
class EventObject:
        """Abstrac EventObject"""
        def __init__(self, eventSource):
                self._eventSource = eventSource
                                                                                                                                                                                                                                                         
        def getSource(self):
                return self._eventSource
                                                                                                                                                                                                                                                         
class HackingEvent(EventObject):
        def __init__(self, eventSource, file, machine):
                EventObject.__init__(self, eventSource)
                self._file = file
                self._machine = machine
                                                                                                                                                                                                                                                         
        def getFile(self):
                return self._file
                                                                                                                                                                                                                                                         
        def getMachine(self):
                return self._machine
                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                         
class HackingListener:
        def fileHacked(self, hackingEvent):
                raise "fileHacked - not implemented"
                                                                                                                                                                                                                                                         
class Logger(HackingListener):
        def fileHacked(self, hackingEvent):
                print "Hacking Event occured..."
                print hackingEvent.getSource().getName(), " hacked: ", hackingEvent.getFile(), " @", hackingEvent.getMachine()
                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                         
class Hacker:
        def __init__(self, name):
                self._name = name
                self._hackingListeners = []
                                                                                                                                                                                                                                                         
        def getName(self):
                return self._name
                                                                                                                                                                                                                                                         
        def addHackingListener(self, listener):
                self._hackingListeners.append( listener )
                                                                                                                                                                                                                                                         
        def removeHackingListener(self, listener):
                self._hackingListeners.remove( listener )
                                                                                                                                                                                                                                                         
        def hackFile(self, filename, machine):
                myHackingEvent = HackingEvent(self, filename, machine)
                self._fireEvent(myHackingEvent)
                                                                                                                                                                                                                                                         
        def _fireEvent(self, event):
                print "fireing event"
                for listener in self._hackingListeners:
                        listener.fileHacked(event)
                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                         
def main():
        Neo = Hacker('Neo')
        myLogger = Logger()
        Neo.addHackingListener(myLogger)
        Neo.hackFile('secureFile.txt', 'HAL9000')
                                                                                                                                                                                                                                                         
if __name__ == '__main__':
        main()
