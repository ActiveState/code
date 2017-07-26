## typeparser  
Originally published: 2007-04-14 17:54:35  
Last updated: 2007-04-15 04:24:53  
Author: Florian Leitner  
  
Python type-string parser. The code evolved from a post in python-list on 11/22/05 by Fredrik Lundh on a dictionary parser. It parses a type-string to their type objects for all basic types. Raises SyntaxError and SemanticError on failures.

Supported types:
        * containers: defaultdict, deque, dict, list, tuple, set
        * basic types: Decimal, bool, float, int, long, str
        * None type

REQUIRES PYTHON >= 2.5