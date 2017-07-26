## Restrictive APIs for PythonOriginally published: 2006-12-15 06:28:20 
Last updated: 2006-12-15 06:28:20 
Author: Will Ware 
 
Python has no inherent provision for a restrictive API that blocks accesses to methods and variables outside an allowed set. Inexperienced Python programmers may fail to adhere to an agreed-upon API, directly accessing the private internals of a class. Adherence to defined APIs is a good thing. This function allows a class to specify its API, and raise AttributeErrors for disallowed accesses.