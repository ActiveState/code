# concrecte_class_finder.py
# An object-oriented alternative to complex if-then-else or switches
# Tested under Python 2.7 and 2.6.6 only
#
# Copyright (C) 2011 by Lucio Santi <lukius at gmail dot com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__author__ = 'Lucio Santi <lukius at gmail dot com>'
__version__ = '1.0'
__all__ = ['ConcreteClassFinder',
           'SubclassNotFoundException',
           'ClassNotFoundException',
           'MultipleSubclassesFoundException',
           'MultipleClassesFoundException']

###############################################################################
class ConcreteClassFinder(object):
    """An object that searches for a suitable class for handling a single
    object or a collection of them. This search can be performed over the leaf 
    subclasses of a base class as well as over an iterable object containing
    classes (e.g., a list).
    Each of the classes inspected should provide a user-defined class method
    that indicates whether the respective class can correctly handle the
    desired object/s. By default, this method name is 'can_handle'/
    'can_handle_objects'.
    Actions can be specified for exceptional cases where no classes or multiple
    classes are found. 
    """
  
    @classmethod
    def __default_testing_method(cls):
        return 'can_handle'
	
    @classmethod
    def __default_testing_method_with_args(cls):
        return 'can_handle_objects'
	
    @classmethod
    def __class_handles(cls, klass, method_name, args):
        method = getattr(klass, method_name)
        try:
            return method(args)
        except Exception:
            return False

    @classmethod
    def find_subclass(cls, base_class, object, if_none = None, if_many = None, method = None):
        if( method is None ):
            method = cls.__default_testing_method()          
        return cls.__pre_find_subclass(base_class, method, object, if_none, if_many)
	
    @classmethod
    def find_subclass_with_args(cls, base_class, args, if_none = None, if_many = None, method = None):
        if( method is None ):
            method = cls.__default_testing_method_with_args()          
        return cls.__pre_find_subclass(base_class, method, args, if_none, if_many)
        
    @classmethod
    def __pre_find_subclass(cls, base_class, method, args, if_none = None, if_many = None):
        def default_action_if_none():
            raise SubclassNotFoundException(base_class, method, args)
        def default_action_if_many(candidates):
            raise MultipleSubclassesFoundException(base_class, method, args, candidates)
          
        if( if_none is None ):
            if_none = default_action_if_none
        if( if_many is None ):
            if_many = default_action_if_many
        
        candidates = [klass for klass in LeafSubclassRetriever(base_class).value() if hasattr(klass, method)]
        return cls.__find_class(candidates, method, args, if_none, if_many)

    @classmethod
    def find_class(cls, classes, object, if_none = None, if_many = None, method = None):
        if( method is None ):
            method = cls.__default_testing_method()          
        return cls.__pre_find_class(classes, method, object, if_none, if_many)
        
    @classmethod
    def find_class_with_args(cls, classes, args, if_none = None, if_many = None, method = None):
        if( method is None ):
            method = cls.__default_testing_method_with_args()          
        return cls.__pre_find_class(classes, method, args, if_none, if_many)        

    @classmethod
    def __pre_find_class(cls, classes, method, args, if_none = None, if_many = None):
        def default_action_if_none():
            raise ClassNotFoundException(classes, method, args)
        def default_action_if_many(candidates):
            raise MultipleClassesFoundException(classes, method, args, candidates)
          
        if( if_none is None ):
            if_none = default_action_if_none
        if( if_many is None ):
            if_many = default_action_if_many
            
        return cls.__find_class(classes, method, args, if_none, if_many)
        
    @classmethod
    def __find_class(cls, classes, method, args, action_if_none, action_if_many):
        suitable_classes = filter(lambda klass: cls.__class_handles(klass, method, args), classes)
        
        if( len(suitable_classes) < 1 ): return action_if_none()
        if( len(suitable_classes) > 1 ): return action_if_many(suitable_classes)  
        return suitable_classes[0]
###############################################################################        
        

###############################################################################
class LeafSubclassRetriever(object):
  def __init__(self, base_class):
        self.base_class = base_class
        
  def value(self):
        direct_subclasses = self.base_class.__subclasses__()
        leaf_subclasses = list()
        for klass in direct_subclasses:
          if( len(klass.__subclasses__()) > 0 ):
                leaf_subclasses += LeafSubclassRetriever(klass).value()
          else:
                leaf_subclasses.append(klass)
                
        return leaf_subclasses
###############################################################################        

###############################################################################
class ClassFindingException(Exception):
    def __init__(self, method, args, candidates = None):
        self.method = method
        self.arguments = args
        self.candidates = candidates
        
    def __str__(self):
        raise NotImplementedError('subclass responsibility')
	
class SubclassNotFoundException(ClassFindingException):
    def __init__(self, base_class, method, args):
        super(SubclassNotFoundException, self).__init__(method, args)
        self.base_class = base_class
	
    def __str__(self):
        return 'base class %s has no subclass satisfying %s(%s)' \
               % (self.base_class.__name__, str(self.method), str(self.arguments))
        
class ClassNotFoundException(ClassFindingException):
    def __init__(self, classes, method, args):
        super(ClassNotFoundException, self).__init__(method, args)
        self.classes = classes
        
    def __str__(self):
        return '%s does not contain any class satisfying %s(%s)' \
               % (str(self.classes), str(self.method), str(self.arguments))        
	
class MultipleSubclassesFoundException(ClassFindingException):
    def __init__(self, base_class, method, args, candidates):
        super(MultipleSubclassesFoundException, self).__init__(method, args, candidates)
        self.base_class = base_class
        
    def __str__(self):
        return 'base class %s has multiple subclasses satisfying %s(%s): %s' \
                % (self.base_class.__name__, str(self.method), str(self.arguments), str(self.candidates))

class MultipleClassesFoundException(ClassFindingException):
    def __init__(self, classes, method, args, candidates):
        super(MultipleSubclassesFoundException, self).__init__(method, args, candidates)
        self.classes = classes
        
    def __str__(self):
        return '%s contains multiple classes satisfying %s(%s): %s' \
               % (str(self.classes), str(self.method), str(self.arguments), str(self.candidates))
###############################################################################
