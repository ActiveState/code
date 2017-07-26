"""
Purpose of this module:
    
Provide a basic undo mechanism.

The undo mechanism is build on top of the observer pattern. The basic
undoer records all parameters needed to undo the change of attributes.

Precondition for usage as an undo mechanism:
    
    1. All attributes important for the undo / redo mechanism must be
       implemented as attributes of new style classes, or be lists or
       dictionaries as mentioned below.
    
    2. Those attributes must be used in a consistent style:

        a) The values of an attribute should only be a"scalar", a list or a
           dictionary [they should have a "type"]. [the same attribute should
           not contain a dictionary at one point in time, and a integer later].
           
    3. The undoer has to be informed of those attributes, it has to be
       activated, and it has to be informed when one undoable
       operation is complete.
       
    4. For lists and dictionaries, the module offers a drop-in
       replacements to intercept changes. You might have to change the
       creation of your lists and dictionaries to use these
       replacement lists and dictionaries.
        
You can mix the mechanism provided here with a higher level interface.

For scalars, we put "scalar_observer" into the attribute slot to intercept
accesses to the attribute. The  values themselves live in a different, "private"
attribute. These private attributes are accessed directly for the
undo / redo steps.

It is important to note that undoing / redoing should not trigger the
undo mechanism. The methods implemented in this module should observe
this restriction.

For dictionaries and lists, we derive the base types. The undo / redo
mechanism uses the methods of the original type.

If you assign a list or a dictionary to a observed attribute
(observe_list_attribute_in_class or observer_dict_attribute_in_class),
the list or mapping is automatically converted to a monitored list or
mapping. This conversion is not done recursively, however.
"""

from scalar_observer import scalar_observer, list_observer_in_instance, dict_observer_in_instance
from list_dict_observer import list_observer, dict_observer

__all__ =('scalar_observer', 'list_observer', 'dict_observer', 'observer', 'basic_undomechanism')

class passthrough(object):
    """
    Instances of this class are used to disable monitoring for scalar attributes.
    The values are just passed through.
    """
    
    def __init__ (self,private_attributename):
        self.private_attributename = private_attributename 
    
    def __set__ (self, instance, value):
        setattr(instance, self.private_attributename, value)
    
    def __get__ (self, instance, owner):
        return getattr(instance, self.private_attributename)

class observer(object):
    """
    Observe changes to (new style) classes.

    To use:

    a) Call observe_scalar(klass, external_attributename)
       for each scalar attribute you want to observer.

       The normal Python comparison operation (=) is used to check if
       a new value is stored in an instance attribute.
                                      
    b) Call observe_list(klass, external_attributename) for each
       list attribute you want to observe.
                                      
    c) Call observe_dict(klass, external_attributename) for each
       dict attribute you want to observe.
        
    2. Call enable / disable to enable / disable observation.

This is an abstract class.

Limitations:

    Assumes that instance attributes are used consistently with
    certain types.
    
    """
    def __init__ (self):
        self.observed_scalar_attributes =[]
        self.observed_list_attributes =[]
        self.observed_dict_attributes =[]
        self.removed_functions =[]
        
        self.observer = self 
        # See enable_category.
        
        # Overwriting this one attribute allows
        # Clients of this module to implemente tracing of all
        # calls to this module.
        
        self.is_enabled = False 
        # Is set to True if enabled is called. Set to False if
        # disable is called.
        
    def monitor_scalar (self, klass, external_attributename):
        """
        Put in a hook so that we can observe modications to instances of klass
        with respect to the attribute "attributename".
    
        It is assumed that the attribute only contains scalar objects. A scalar
        object is an object which is unstructured, and not shared.
        
        If the value of an attribute is an instance (or None), then this is considered
        a scalar: the structure is exposed within the instance, not at the attribute level.
        """
    
        self.observed_scalar_attributes.append((klass, external_attributename))
    
    def monitor_list_attribute_in_class (self, klass, external_attributename):
        self.observed_list_attributes.append((klass, external_attributename))
    
    def observe_dict_attribute_in_class (self, klass, external_attributename):
        self.observed_dict_attributes.append((klass, external_attributename))
    # 
    # Delayed activation of the observer mechanism is probably useful.
    # 
    # Switching on / off is potentially useful.
    def enable (self):
        """
        Enable monitoring.
        Return True if monitoring was already enabled, false otherwise.
        """
        result = self.is_enabled 
        for l, klass in((self.observed_scalar_attributes, scalar_observer),
            (self.observed_list_attributes, list_observer_in_instance),
            (self.observed_dict_attributes, dict_observer_in_instance)):
            self.enable_category(l, klass)
                     
        self.enable_put_in_removed_functions()
        self.is_enabled = True 
        return result 
    
    def enable_put_in_removed_functions (self):
        """
        Reinstate the functions which were removed from list_observer and dict_observer.
        """
        for klass, attribute, function in self.removed_functions:
            setattr(klass, attribute, function)
    
    def enable_category (self, l, monitor_class):
        for klass, external_attributename in l:
            setattr(klass, external_attributename,
               monitor_class(external_attributename, self.observer))
    
    def disable_category (self, l, monitor_class):
        for klass, external_attributename in l:
            setattr(klass, external_attributename, passthrough(internal_attributename))
          
    def disable (self):
        """
        Disable monitoring (temporarily).
        """
        was_enabled = self.is_enabled
        if was_enabled:
            for l, klass in(
                (self.observed_scalar_attributes, scalar_observer),
                (self.observed_list_attributes, list_observer_in_instance),
                (self.observed_dict_attributes, dict_observer_in_instance)):
                    
                self.disable_category(l, klass)
              
            self.remove_overrides_in_list_and_dict_monitor()
            self.is_enabled = False 
        return was_enabled
          
    def remove_overrides_in_list_and_dict_monitor (self):
        """
        Deletes all function definitions in list_observer and dict_observer.
        The net effect of this is that instances of these classes should
        behave like regular lists and dictionaries.
        """      
        import inspect 
        for klass in(list_observer, dict_observer):
            for attribute in dir(klass):
                try:
                    entity = getattr(klass, attribute)
                except AttributeError:
                    pass 
                else:
                    if inspect.isfunction(entity):
                        delattr(klass, attribute)
                        self.removed_functions.append(klass, attribute, entity)

class basic_undomechanism(observer):
    """
    This class provides the basic operations for undoable operations.
    
    Records a list of changes which it will undone or redone one by
    one.
    
    The granularity of the undo / redo operations is determined by
    calls to the 'mark' procedure. Only immediately after the 'mark'
    call can undo be called.  Redo can only be called after calling
    undo.
          
    'rollback' is a special case of undo: it is not redoable, and mark
    should *not* have been called.
    
    The envisioned usage of this facility is in error recovery: if a
    command does not go through, you can call this command to undo all
    your changes (and leave the application in a consistent state).
          
    Use the observe_scalar, observe_list_attribute_in_class and
    observe_dict_attribute_in_class methods to make assignment to
    instance variables undoable.
    
    Usage pattern:
        m = basic_undomechanism()
        class c(object):
            def x(self):
                self.y = 122
        m.observe_scalar(c, "y")
        m.enable()
        
        All assignements to y in instances of c will now be monitored, and information
        will be stored away to make the changes undoable.
    
    Call 'enable' to activate the undo mechanism, 'disable' to
    temporarily stop the undo mechanism from collecting information
    about changes.
          
    The individual changes are bundled into "_commands". The
    boundaries of these _commands are marked by a call to the
    procedure "mark".
    
    The procedure 'reset' can be called externally to erase all undo
    information.
          
    Individual lists and dictionaries can also be monitored for change
    with the list_observer and dict_observer classes.
    
    If you do not nest lists / dictionaries in lists / dictionaries,
    then you might be able to use the automatic conversion offered by
    the 'list_observer_in_instance' and 'dict_observer_in_instance'
    class.
    
    You can also mix "high level undo" with "low level undo". Usage
    pattern:
        
        was_enabled = m.disable()
        def undo_function(*args):
            # undo something
            if was_enabled:
                m.enable()
            return (redo_function, redo_arguments)
        # compute the undo arguments.
        m.add_undo_step(undo_function, undo_arguments)        
          
    Possible optimizations later: special handling for string attributes.
    """
    def __init__ (self):
        observer.__init__(self)
        self.reset()
    
    def reset (self):
        self._steps =[]
        self._commands =[None, None]
        self._index = 0
    
    # handling scalars
    def scalar_set (self, instance, private_attributename, external_attributename):
        self._steps.append((self.scalar_set_undo, (instance, private_attributename)))
    
    def scalar_set_undo (self, instance, private_attributename):
        """Undo the changes done by the assignment of an instance"""
        newvalue = getattr(instance, private_attributename)
        delattr(instance, private_attributename)
        return self.scalar_set_redo,(instance, private_attributename, newvalue)
    
    def scalar_set_redo (self, instance, private_attributename, newvalue):
        setattr(instance, private_attributename, newvalue)
        return self.scalar_set_undo,(instance, private_attributename)
    
    def scalar_modify (self, instance, private_attributename, external_attributename, oldvalue):
        self._steps.append((self.scalar_modify_undo, (instance, private_attributename, oldvalue)))
    
    def scalar_modify_undo (self, instance, private_attributename, oldvalue):
        new_value = getattr(instance, private_attributename)
        setattr(instance, private_attributename, oldvalue)
        return self.scalar_modify_undo, (instance, private_attributename, new_value)
    
    # handling lists
    def list_assignment_replace (self, instance, attributename, oldvalue):
        self._steps.append((self.list_assignment_replace_undo, (instance, attributename, oldvalue)))
    
    def list_assignment_replace_undo (self, instance, attributename, oldvalue):
        newvalue = getattr(instance, attributename)
        setattr(instance, attributename, oldvalue)
        return self.list_assignment_replace_redo, (instance, attributename, newvalue)
    
    def list_assignment_replace_redo (self, instance, attributename, newvalue):
        oldvalue = getattr(instance, attributename)
        setattr(instance, attributename, newvalue)
        return self.list_assignment_replace_undo, (instance, attributename, oldvalue)
    
    def list_assignment_new (self, instance, attributename):
        self._steps.append((self.list_assignment_new_undo, (instance, attributename)))
    
    def list_assignment_new_undo (self, instance, attributename):
        newvalue = getattr(instance, attributename)
        delattr(instance, attributename)
        return self.list_assignment_new_redo, (instance, attributename, newvalue)
    
    def list_assignment_new_redo (self, instance, attributename, newvalue):
        setattr(instance, attributename, newvalue)
        return self.list_assignment_new_undo, (instance, attributename)
    
    def list_create (self, array, key):
        self._steps.append((self.list_create_undo, (array, key)))
    
    def list_create_undo (self, array, key):
        value = list.__getitem__(array, key)
        list.__delitem__(array, key)
        return self.list_create_redo, (array, key, value)
    
    def list_create_redo (self, array, key, value):
        list.__setitem__(array, key, value)
        return self.list_create_undo, (array, key)
    
    def list_set (self, array, key, oldvalue):
        self._steps.append((self.list_set_undo, (array, key, oldvalue)))
    
    def list_set_undo (self, array, key, value):
        oldvalue = list.__getitem__(array, key)
        list.__setitem__(array, key, value)
        return self.list_set_undo, (array, key, oldvalue)
    
    def list_setslice (self, list_observer, i, j, newvalue, oldvalue):
        self._steps.append((self.undo_list_setslice, (list_observer, i, j, newvalue, oldvalue)))
        
    def undo_list_setslice (self, list_observer, i, j, newvalue, oldvalue):
        list.__setslice__(list_observer, i, i+len(newvalue), oldvalue)
        return(self.redo_list_setslice, (list_observer, i, j, newvalue, oldvalue))
        
    def redo_list_setslice (self, list_observer, i, j, newvalue, oldvalue):
        list.__setslice__(list_observer, i, j, newvalue)
        return(self.undo_list_setslice, (list_observer, i, j, newvalue, oldvalue))
    
    def list_delslice (self, list_observer, i, oldvalue):
        self.list_setslice(list_observer, i, i+len(oldvalue), [], oldvalue)
    
    def list_del (self, list_observer, key, oldvalue):
        self._steps.append((self.list_del_undo, (list_observer, key, oldvalue)))
        
    def list_del_undo (self, list_observer, key, oldvalue):
        if type(key)==type(1):
            list.__setitem__(list_observer, slice(key, key), [oldvalue])
        else:
            list.__setitem__(list_observer, key, oldvalue)
        return self.list_del_redo, (list_observer, key, oldvalue)
    
    def list_del_redo (self, list_observer, key, oldvalue):
        oldvalue = list.__getitem__(list_observer, key)
        list.__delitem__(list_observer, key)
        return self.list_del_undo, (list_observer, key, oldvalue)
    
    def list_extend (self, list_observer, newvalue):
        old_insert_index = len(list_observer) - len(newvalue)
        self.list_setslice(list_observer, old_insert_index, old_insert_index, newvalue, [])
    
    def list_insert (self, observer, i, x):
        self.list_setslice(observer, i, i, [x], [])
    
    def list_append (self, array):
        self._steps.append((self.list_append_undo, (array, )))
    
    def list_append_undo (self, array):
        oldvalue = list.pop(array)
        return self.list_append_redo, (array, oldvalue)
    
    def list_append_redo (self, array, oldvalue):
        list.append(array, oldvalue)
        return self.list_append_undo, (array, )
    
    def list_pop (self, array, oldvalue):
        self._steps.append((self.list_append_redo, (array, oldvalue)))
    
    def list_remove (self, list_object, index, element):
        self.list_del(list_object, index, element)
    
    def list_reverse (self, list_observer):
        self._steps.append((self.list_reverse_undo, (list_observer, )))
        
    def list_reverse_undo (self, list_observer):
        list.reverse(list_observer)
        return(self.list_reverse_undo, (list_observer, ))
    
    def list_sort (self, list_observer, oldvalue):
        self._steps.append((self.list_sort_undo, (list_observer, oldvalue)))
        
    def list_sort_undo (self, list_observer, oldlist):
        newlist = list_observer[:]
        list.__setslice__(list_observer, 0, 2147483647, oldlist)
        return(self.list_sort_undo, (list_observer, newlist))
    
    # handling dictionaries
    # Dictionary monitors are are really handled like list observers.
    # For now,  just use the same methods.
    dict_assignment_new = list_assignment_new 
    dict_assignment_new_undo = list_assignment_new_undo 
    dict_assignment_new_redo = list_assignment_new_redo 
    
    dict_assignment_replace = list_assignment_replace 
    dict_assignment_replace_undo = list_assignment_replace_undo 
    dict_assignment_replace_redo = list_assignment_replace_redo 
    
    def dict_create (self, dictionary, key):
        self._steps.append((self.dict_create_undo, (dictionary, key)))
    
    def dict_create_undo (self, dictionary, key):
        value = dict.__getitem__(dictionary, key)
        dict.__delitem__(dictionary, key)
        return self.dict_create_redo, (dictionary, key, value)
        
    def dict_create_redo (self, dictionary, key, value):
        dict.__setitem__(dictionary, key, value)
        return self.dict_create_undo, (dictionary, key, )
    
    def dict_set (self, dictionary, key, oldvalue):
        self._steps.append((self.dict_set_undo, (dictionary, key, oldvalue)))
    
    def dict_set_undo (self, dictionary, key, value):
        oldvalue = dict.__getitem__(dictionary, key)
        dict.__setitem__(dictionary, key, value)
        return self.dict_set_undo, (dictionary, key, oldvalue)
    
    def dict_update (self, dictionary, new_keys, replaced_key_values):
        self._steps.append((self.dict_update_undo, (dictionary, new_keys, replaced_key_values)))
    
    def dict_update_undo (self, dictionary, new_keys, replaced_key_values):
        update_dict ={}
        for key in new_keys:
            update_dict[key] = dict.__getitem__(dictionary, key)
            dict.__delitem__(dictionary, key)
        for key,  value in replaced_key_values:
            update_dict[key] = dict.__getitem__(dictionary, key)
            dict.__setitem__(dictionary, key, value)
        return self.dict_update_redo, (dictionary, update_dict)
          
    def dict_update_redo (self, dictionary, update_dict):
        new_keys = []
        replaced_key_values = []
        for key, value in update_dict.items():
            if key in dictionary:
                replaced_key_values.append((key, dictionary[key]))
            else:
                new_keys.append(key)
            dict.__setitem__(dictionary, key, value)
        return self.dict_update_undo, (dictionary, new_keys, replaced_key_values)
                     
    def dict_setdefault (self, dict_observer, key, value):
        self._steps.append((self.dict_setdefault_undo, (dict_observer, key)))
    
    def dict_setdefault_undo (self, dict_observer, key):
        value = dict.__getitem__(dict_observer, key)
        dict.__delitem__(dict_observer, key)
        return(self.dict_setdefault_redo, (dict_observer, key, value))
        
    def dict_setdefault_redo (self, dict_observer, key, value):
        dict.__setitem__(dict_observer, key, value)
        return(self.dict_setdefault_undo, (dict_observer, key))
    
    def dict_clear (self, dictionary, oldvalue):
        self._steps.append((self.dict_clear_undo, (dictionary, oldvalue)))
    
    def dict_clear_undo (self, dictionary, oldvalue):
        dict.update(dictionary, oldvalue)
        return self.dict_clear_redo, (dictionary, )
    
    def dict_clear_redo (self, dictionary):
        dict.clear(dictionary)
        return self.dict_clear_undo, (dictionary, )
    
    def dict_del (self, dict_observer, key, oldvalue):
        self._steps.append((self.dict_del_undo, (dict_observer, key, oldvalue)))
    
    def dict_del_undo (self, dict_observer, key, oldvalue):
        dict.__setitem__(dict_observer, key, oldvalue)
        return self.dict_del_redo, (dict_observer, key, oldvalue)
    
    def dict_del_redo (self, dict_observer, key, oldvalue):
        oldvalue = dict.__getitem__(dict_observer, key)
        dict.__delitem__(dict_observer, key)
        return self.dict_del_undo, (dict_observer, key, oldvalue)
    
    dict_pop = dict_del 
    
    def dict_popitem (self, dict_observer, key, oldvalue):
        self._steps.append((self.dict_del_undo, (dict_observer, key, oldvalue)))
    
    # The undo machinery
    def add_undo_step (self, undo_step):
        """
        Add an undo step to the undoer.
        undo_step should be a tuple (function, arguments).
        function(*arguments) should undo something, and return the tuple for the redo.
        The redo function, in turn, should return the tuple for the undo.
        """
        self._steps.append(undo_step)
    
    # Queries
    def canUndo (self):
        return self._commands[self._index]is not None and len(self._steps)==0
    
    def canRedo (self):
        return self._commands[self._index+1]is not None and len(self._steps)==0
    
    def commands (self):
        return len(self._commands)-2
    
    def commands_to_undo (self):
        return self._index 
    
    def commands_to_redo (self):
        return self.commands()-self._index 
    
    def steps_stored (self):
        """
        Return the total number of steps stored in the undoer.
        """
        result = 0
        for command in self._commands[1:-1]:
            result+=len(command)
        return result 
    
    def print_commands (self, comment=''):
        """
        Print a readable list of all commands.
        Debugging aid.
        """
        print "===== Commands: %s ========"%comment 
        for i in range(1, len(self._commands)-1):
            # The first and last entry are sentinels.
            print "Command", i 
            steps = self._commands[i]
            if steps:
                for step in steps:
                    function, args = step 
                    print "  ", function.__name__, args 
        print "========================"
    
    # End of query methods.
    def mark (self):
        """
        The current (user level) commmand ends.
        """
        self._commands[self._index+1:] =[self._steps, None]
        self._index+=1
        self._steps =[]
    
    def undo (self):
        assert self.canUndo()
        self._commands[self._index] = self.run_commands(self._commands[self._index])
        self._index-=1
    
    def redo (self):
        assert self.canRedo()
        self._commands[self._index+1] = self.run_commands(self._commands[self._index+1])
        self._index+=1
    
    def rollback (self):
        self.run_commands(self._steps)
    
    def run_commands (self, steps):
        """
        Run the undo / redo _steps.
        Returns the list of steps to redo / undo the steps just made.
        """
        steps.reverse()
        return[func(*args) for func, args in steps]
