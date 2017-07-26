import new, dis

cell_changer_code = new.code(
    1, 1, 2, 0,
    ''.join([
        chr(dis.opmap['LOAD_FAST']), '\x00\x00',
        chr(dis.opmap['DUP_TOP']),
        chr(dis.opmap['STORE_DEREF']), '\x00\x00',
        chr(dis.opmap['RETURN_VALUE'])
    ]), 
    (), (), ('newval',), '<nowhere>', 'cell_changer', 1, '', ('c',), ()
)

def change_cell_value(cell, newval):
    return new.function(cell_changer_code, {}, None, (), (cell,))(newval)


"""
Example use:

>>> def constantly(n):
...   def return_n():
...     return n
...   return return_n
... 
>>> f = constantly("Hi, Mom")
>>> f()
'Hi, Mom'
>>> f()
'Hi, Mom'
>>> f.func_closure   
(<cell at 0xb7e1d56c: str object at 0xb7ded620>,)
>>> change_cell_value(f.func_closure[0], 46)
46
>>> f()
46

"""
