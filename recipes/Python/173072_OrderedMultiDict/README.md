## OrderedMultiDict and UnorderedMultiDict  
Originally published: 2003-01-09 16:13:57  
Last updated: 2003-01-09 16:13:57  
Author: Andrew Dalke  
  
This implements two types of dictionary-like objects where there can be more than one entry with the same key. One is OrderedMultiDict, which preserves the order of all entries across all keys. The other is UnorderedMultidict, which only preserves the order of entries for the same key.

Download MultiDict.py
Example:
>>> import MultiDict
>>> od = MultiDict.OrderedMultiDict()
>>> od["Name"] = "Andrew"; od["Color"] = "Green"
>>> od["Name"] = "Karen"; od["Color"] = "Brown"
>>> od["Name"]
'Karen'
>>> od.getall("Name")
['Andrew', 'Karen']
>>> for k, v in od.allitems():
...     print "%r == %r", (k, v)
...
'Name' == 'Andrew'
'Color' == 'Green'
'Name' == 'Karen'
'Color' == 'Brown'
>>> ud = MultDict.UnorderedMultiDict(od)
>>> for k, v in ud.allitems():
...     print "%r == %r", (k, v)
...
'Name' == 'Andrew'
'Name' == 'Karen'
'Color' == 'Green'
'Color' == 'Brown'
>>>