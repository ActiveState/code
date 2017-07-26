## Named Values 
Originally published: 2011-07-28 00:23:01 
Last updated: 2011-07-28 00:23:34 
Author: Nick Coghlan 
 
NamedValue is a mixin class that modifies the signature of the class constructor to accept a name as the first positional argument and modifies repr() to display the name without affecting the result of str() (even for peer classes that rely on the str->repr fallback for their str implementation).