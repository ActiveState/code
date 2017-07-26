class MovableListIterator:
    """This is an iterator for lists which allows one to advance
    or regress the position in the list. It also will raise an
    exception if the list is lengthened or shortened."""

    def __init__(self, myList):
        self.myList = myList
        self.originalLength = len(myList)
        self.nextIndex = 0

    def __iter__(self):
        return self

    class ListModifiedException(Exception):
        pass

    def next(self):
        if len(self.myList) != self.originalLength:
            raise MovableListIterator.ListModifiedException

        index = self.nextIndex
        if index >= self.originalLength:
            raise StopIteration
        self.nextIndex += 1
        return self.myList[index]

    def advance(self, places=1):
        self.nextIndex += places

    def regress(self, places=1):
        self.nextIndex -= places
        
        


import unittest
class TestMovableListIterator(unittest.TestCase):
    def test_create(self):
        li = list('abcde')
        i = MovableListIterator(li)
    def test_basic_loop(self):
        li = 'abcde'
        self.assertEqual( list(li), [x for x in MovableListIterator(li)] )
    def test_advance(self):
        li = 'abcdef'
        result = []
        i = MovableListIterator(li)
        result.append( i.next() )
        i.advance()
        result.append( i.next() )
        i.advance(2)
        result.append( i.next() )
        self.assertEqual( list('acf'), result )
        self.assertRaises( StopIteration, i.next )
    def test_regress(self):
        li = 'abc'
        result = []
        i = MovableListIterator(li)
        result.append( i.next() )
        i.regress()
        result.append( i.next() )
        result.append( i.next() )
        result.append( i.next() )
        i.regress(2)
        result.append( i.next() )
        result.append( i.next() )
        self.assertEqual( list('aabcbc'), result )
        self.assertRaises( StopIteration, i.next )
    def test_shrink_throws(self):
        li = [1,2,3,4]
        i = MovableListIterator(li)
        li.pop()
        self.assertRaises( MovableListIterator.ListModifiedException,
                           i.next )
    def test_grow_throws(self):
        li = [1,2,3,4]
        i = MovableListIterator(li)
        li.append(5)
        self.assertRaises( MovableListIterator.ListModifiedException,
                           i.next )
