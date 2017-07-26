## Dictionary with attribute-style access  
Originally published: 2006-01-26 06:18:50  
Last updated: 2006-01-26 06:18:50  
Author: Keith Dart  
  
This supclass of dict allows access the the value using attribute access syntax.

	d = AttrDict()
	d.one = "one"
	print d
	print d.get
	print d.one
	print d["one"]
	d["two"] = 2
	print d.two
	print d["two"]