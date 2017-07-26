## Error propagating class for uncertain numeric quantitiesOriginally published: 2007-12-11 02:11:00 
Last updated: 2007-12-11 02:11:00 
Author: sasa sasa 
 
This class permits full error propagation for numeric values.\nIt wraps a value and an associated error (standard deviation, measurement uncertainty...). Numeric operations are overloaded and permit use with other Uncertain objects, precise values without errors, generally speakin gmost other numeric (even array) objects. The "traitification" can easily be reverted by dumping all references to traits.