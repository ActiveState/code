## Mixins for equality, rich comparisons and hashingOriginally published: 2007-03-21 13:20:30 
Last updated: 2007-04-10 16:49:41 
Author: Steven Bethard 
 
Many comparable or hashable classes calculate all comparison and hash results from the same simple calculation. The mixins in this recipe allow such classes to define a single __key__() method from which all the __eq__(), __lt__(), __hash__(), etc. methods are automatically defined.