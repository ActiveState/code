## C#-Style Events in PythonOriginally published: 2005-04-24 21:57:07 
Last updated: 2008-10-26 06:35:11 
Author: Zoran Isailovski 
 
IMPROVED. The concept of events is heavily used in GUI libraries and is the foundation for most implementations of the MVC (Model, View, Controller) design pattern (the latter being my prime motivation for this recipe). Another prominent use of events is in communication protocol stacks, where lower protocol layers need to inform upper layers of incoming data and the like. Here is a handy class that encapsulates the core to event subscription and event firing and feels like a "natural" part of the language.