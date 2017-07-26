class itemproperty(object):

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        if doc is None and fget is not None and hasattr(fget, "__doc__"):
            doc = fget.__doc__
        self._get = fget
        self._set = fset
        self._del = fdel
        self.__doc__ = doc

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return bounditemproperty(self, instance)

    def __set__(self, instance, value):
        raise AttributeError("can't set attribute")

    def __delete__(self, instance):
        raise AttributeError("can't delete attribute")

    def getter(self, fget):
        return itemproperty(fget, self._set, self._del, self.__doc__)

    def setter(self, fset):
        return itemproperty(self._get, fset, self._del, self.__doc__)

    def deleter(self, fdel):
        return itemproperty(self._get, self._set, fdel, self.__doc__)


class bounditemproperty(object):

    def __init__(self, item_property, instance):
        self.__item_property = item_property
        self.__instance = instance

    def __getitem__(self, key):
        fget = self.__item_property._get
        if fget is None:
            raise AttributeError("unreadable attribute item")
        return fget(self.__instance, key)

    def __setitem__(self, key, value):
        fset = self.__item_property._set
        if fset is None:
            raise AttributeError("can't set attribute item")
        fset(self.__instance, key, value)

    def __delitem__(self, key):
        fdel = self.__item_property._del
        if fdel is None:
            raise AttributeError("can't delete attribute item")
        fdel(self.__instance, key)


if __name__ == "__main__":

    class Element(object):

        def __init__(self, tag, value=None):
            self.tag = tag
            self.value = value
            self.children = {}

        @itemproperty
        def xpath(self, path):
            """Get or set the value at a relative path."""
            path = path.split('/')
            element = self
            for tag in path:
                if tag in element.children:
                    element = element.children[tag]
                else:
                    raise KeyError('path does not exist')
            return element.value

        @xpath.setter
        def xpath(self, path, value):
            path = path.split('/')
            element = self
            for tag in path:
                element = element.children.setdefault(tag, Element(tag))
            element.value = value

        @xpath.deleter
        def xpath(self, path):
            path = path.split('/')
            element = self
            for tag in path[:-1]:
                if tag in element.children:
                    element = element.children[tag]
                else:
                    raise KeyError('path does not exist')
            tag = path[-1]
            if tag in element.children:
                del element.children[tag]
            else:
                raise KeyError('path does not exist')

    tree = Element('root')
    tree.xpath['unladen/swallow'] = 'african'
    assert tree.xpath['unladen/swallow'] == 'african'
    assert tree.children['unladen'].xpath['swallow'] == 'african'
    assert tree.children['unladen'].children['swallow'].value == 'african'

    tree.xpath['unladen/swallow'] = 'european'
    assert tree.xpath['unladen/swallow'] == 'european'
    assert len(tree.children) == 1
    assert len(tree.children['unladen'].children) == 1

    tree.xpath['unladen/swallow/airspeed'] = 42
    assert tree.xpath['unladen/swallow'] == 'european'
    assert tree.xpath['unladen/swallow/airspeed'] == 42

    del tree.xpath['unladen/swallow']
    assert 'swallow' not in tree.children['unladen'].children
    try:
        tree.xpath['unladen/swallow/airspeed']
    except KeyError:
        pass
    else:
        assert False
