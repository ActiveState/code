import copy

class Subject:
    def __init__(self, excluded):
        # excluded is a list of attribute names
        
        # who should be notified
        self.__dict__['_observers'] = []
        
        # which attrs should not trigger a notification
        # obviously it can be done the other way round if needed
        # i.e.which attrs trigger a notification 
        self.__dict__['_excluded_attrs'] = copy.copy(excluded)

    def __setattr__(self, attrname, value):
        # set the attribute
        self.__dict__[attrname] = value
        # if the attribute triggers a notification
        if not attrname in self._excluded_attrs:
            # notify observers
            self.notify(attrname, value)

    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, attrname, value):
        for observer in self._observers:
            observer.update(self, attrname, value)

# Example usage
class Data(Subject):
    def __init__(self, excluded=[]):
        # pass up the attrs to be excluded from notification
        Subject.__init__(self, excluded)

class Observer1:
    def update(self, subject, attrname, value):
        print 'Observer1: Subject %s has updated attr %s to %s' % (subject.name, attrname, value)

class Observer2:
    def update(self, subject, attrname, value):
        print 'Observer2: Subject %s has updated attr %s to %s' % (subject.name, attrname, value)

# Example
def main():
    print "Creating data1 without notification for attrs name & surname"
    data1 = Data(excluded=['name','surname'])
    print "Creating data2 without notification for attr age"
    data2 = Data(excluded=['age'])

    obs1 = Observer1()
    data1.attach(obs1)
    data1.attach(obs1)

    obs2 = Observer2()
    data2.attach(obs2)
    data2.attach(obs2)

# now try it
# you can set any attribute directly
    print "Setting data1.name=Heather - Notification unnecessary"
    data1.name = 'Heather'
    print "Setting data1.num=333 - Notification expected"
    data1.num = 333;

    print "Setting data2.name=Molly - Notification expected"
    data2.name = 'Molly'
    print "Setting data2.age=28 - Notification unnecessary"
    data2.age = 28
    print "Setting data2.eyecolor=blue - Notification expected"
    data2.eyecolor='blue';

if __name__ == '__main__':
    main()
