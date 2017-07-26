## Generator Attributes  
Originally published: 2002-11-24 16:25:15  
Last updated: 2002-12-09 08:44:56  
Author: Raymond Hettinger  
  
Function to enable attribute access for generator instances. Simplifies data sharing for advanced uses of generators and provides much of the functionality sought by PEP 288.
<br>
Most uses of generators have no need for data sharing.  This recipe is for the few tough cases which can be written more elegantly when attribute access is enabled.
