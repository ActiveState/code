def get_cell_value(cell):
    return type(lambda: 0)(
        (lambda x: lambda: x)(0).func_code, {}, None, None, (cell,)
    )()



# longer and more verbose version:
import new
def get_cell_value(cell):
    def make_closure_that_returns_value(use_this_value):
        def closure_that_returns_value():
            return use_this_value
        return closure_that_returns_value
    dummy_function = make_closure_that_returns_value(0)
    dummy_function_code = dummy_function.func_code
    our_function = new.function(dummy_function_code, {}, None, None, (cell,))
    value_from_cell = our_function()
    return value_from_cell



# examples
>>> def make_list_appender(mylist):
...   def append_to_mylist(newvalue):
...     mylist.append(newvalue)
...     return newvalue
...   return append_to_mylist
... 
>>> somelist = []
>>> somelist_appender = make_list_appender(somelist)
>>> somelist_appender(2)
2
>>> somelist_appender(3)
3
>>> somelist
[2, 3]
>>> somelist_appender
<function append_to_mylist at 0xb7df556c>
>>> somelist_appender.func_closure
(<cell at 0xb7e1d38c: list object at 0xb7e0f26c>,)
>>> cell = somelist_appender.func_closure[0]
>>> get_cell_value(cell)
[2, 3]
>>> get_cell_value(cell) is somelist
True
