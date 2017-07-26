# Simple tool for making class-like objects using nested scopes and closures in Python 3
#
# Advantages:
#  * cleaner coding style
#  * faster internal references
#  * faster external calls - no bound methods or rewriting arg tuples
#  * inlined initialization code
#  * painlessly delegate work to other objects
#
# Disadvantages:
#  * need setter methods to update attributes
#  * inheritance is not supported
#  * slower calls to special methods
#  * there is no "self"
#  * limited support for help()

import sys

class Instance:
    'Instances where methods are implemented as closures'

# The Python interpreter looks for special methods in the class dictionary
# Add support for them by dispatching them back to the instance methods
smethods =    '''__bool__ __int__ __float__ __complex__ __index__
                 __len__ __getitem__ __setitem__ __delitem__ __contains__
                 __iter__ __next__ __reversed__
                 __call__ __enter__ __exit__
                 __str__ __repr__  __bytes__ __format__
                 __eq__ __ne__ __lt__ __le__ __gt__ __ge__ __hash__
                 __add__ __mul__ __sub__ __truediv__ __floordiv__ __mod__
                 __and__ __or__ __xor__ __invert__ __lshift__ __rshift__
                 __pos__ __neg__ __abs__ __pow__ __divmod__
                 __round__ __ceil__ __floor__ __trunc__
                 __radd__ __rmul__ __rsub__ __rtruediv__ __rfloordiv__ __rmod__
                 __rand__ __ror__ __rxor__ __rlshift__ __rrshift__
                 __rpow__ __rdivmod__
                 __get__ __set__ __delete__
                 __copy__ __deepcopy__ __reduce__ __reduce_ex__
                 __getstate__ __setstate__ __getnewargs__ __getinitargs__
                 __subclasshook__ __subclasscheck__ __instancecheck__
                 __dir__ __sizeof__'''.split()
for sm in smethods:
    setattr(Instance, sm, lambda self, *args, sm=sm: self.__dict__[sm](*args))

def classify(local_dict=None):
    'Move local definitions to an instance dictionary'
    o = Instance()
    if local_dict is None:
        local_dict = sys._getframe(1).f_locals
    vars(o).update(local_dict)
    return o


############################################################################
###  Simple example  #######################################################

def Animal(name):
    'Animal-like class'
    def speak():
        print('I am', name)
    def set_name(newname):
        nonlocal name
        name = newname
    def __getitem__(key):
        return '%s is %sing' % (name, key.title())
    return classify()

d = Animal('Fido')
print(d.name)
d.speak()
d.set_name('Max')
d.speak()
print(d['fetch'])


############################################################################
###  Practical example  ####################################################

def PriorityQueue(initial_tasklist):
    'Retrieve tasks by priority.  Tasks can be removed or reprioritized.'
    from heapq import heappush, heappop

    pq = []                         # list of entries arranged in a heap
    entry_finder = {}               # mapping of tasks to entries
    REMOVED = object()              # placeholder for a removed task
    count = 0                       # unique sequence count

    def add(task, priority=0):
        'Add a new task or update the priority of an existing task'
        nonlocal count
        if task in entry_finder:
            remove(task)
        entry = [priority, count, task]
        entry_finder[task] = entry
        heappush(pq, entry)
        count += 1

    def remove(task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = entry_pop(task)
        entry[-1] = REMOVED

    def pop():
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while pq:
            priority, count, task = heappop(pq)
            if task is not REMOVED:
                del entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    def __iter__():
        'Show task in order of priority'
        pq.sort()
        for priority, count, task in pq:
            if task is not REMOVED:
                yield task

    def __repr__():
        return 'PriorityQueue()'

    def __str__():
        return 'PriorityQueue with %d pending tasks' % __len__()

    # Delegate some of the work to the entry_finder dictionary
    __contains__ = entry_finder.__contains__
    __len__ = entry_finder.__len__
    entry_pop = entry_finder.pop

    # No separate method needed for initialization
    for task, priority in initial_tasklist:
        add(task, priority)

    return classify()


if __name__ == '__main__':

    # Note: Client code is written normally.  It makes no difference
    # whether a PriorityQueue was implemented as a regular class or
    # implemented using closures.

    todo = PriorityQueue([('fish', 5), ('play', 3)])
    todo.add('code', 1)
    todo.add('sleep', 6)
    print(list(todo))
    print('Pop the topmost task:  %r' % todo.pop())
    print("Deprioritize 'play'")
    todo.add('play', 10)
    todo.remove('sleep')
    print(len(todo))
    print(list(todo))
    print(todo)
    print('fish' in todo)
    help(PriorityQueue)
    help(todo.add)
