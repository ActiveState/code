## Dictionary with attribute-style access  
Originally published: 2006-01-26 06:18:50  
Last updated: 2006-01-26 06:18:50  
Author: Keith Dart  
  
This supclass of dict allows access the the value using attribute access syntax.\n\n\td = AttrDict()\n\td.one = "one"\n\tprint d\n\tprint d.get\n\tprint d.one\n\tprint d["one"]\n\td["two"] = 2\n\tprint d.two\n\tprint d["two"]