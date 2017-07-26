class Klass(object):
  
    def __getattr__(self, name):
        """
        Locate the function with the dotted
        attribute.
        """
        def traverse(parent, child):
            if instance(parent, str):
                parent = getattr(self, parent)
            return getattr(parent, child)
        return reduce(traverse, name.split('.'))
