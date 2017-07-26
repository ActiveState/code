## Decimal Number To Byte(s) And String To Byte(s) Converter.  
Originally published: 2012-01-24 21:11:46  
Last updated: 2012-01-24 21:11:47  
Author: Barry Walker  
  

A function to convert decimal integer numbers, (from 0 to 255), into byte(s) format.
Another function calling the above function to convert ASCII strings into byte(s) format.

Python 3.1.3 (r313:86834, Nov 28 2010, 10:01:07) 
[GCC 4.4.5] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> exec(open('/home/G0LCU/Desktop/Code/d2b.py').read())
>>> a=78
>>> type(a)
<class 'int'>
>>> b=d2b(a)
>>> print(b)
b'N'
>>> type(b)
<class 'bytes'>
>>> text="\x00(C)2012, B.Walker, G0LCU.\xFF"
>>> len(text)
27
>>> type(text)
<class 'str'>
>>> newtext=t2b(text)
>>> len(newtext)
27
>>> print(newtext)
b'\x00(C)2012, B.Walker, G0LCU.\xff'
>>> type(newtext)
<class 'bytes'>

It requires NOTHING special at all to work and can be run like above or imported from
the correct "Lib" drawer/folder/directorfy as:-

>>> import d2b

And when imported called as:-

>>> d2b.d2b(some_number, optional_some_other_mumber)<RETURN/ENTER>

OR

>>> d2b.t2b(some_ASCII_string)<RETURN/ENTER>

Read the code for much more information...

Issued under the GPL2 licence.

Enjoy finding simple solutions to often very difficult problems.

Bazza, G0LCU.
