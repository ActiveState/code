###Get configured!

Originally published: 2004-09-03 14:41:32
Last updated: 2004-09-03 14:41:32
Author: Martin Bless

In recipe http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52308 Alex Martelli showed how a collection of stuff can be organized as a "Bunch". This recipe recommends a specialized dictionary to reach the same goal. Since Python 2.2 the new dictionary-class can easily be created by subclassing the built in 'dict' type. Adding a special method to (re)present the proposed BunchDict()-class we arrive at CfgBunch(), which is very well suited to contain bunches of configuration data.\n\nIt is further shown how these - in itself - rather unspectacular components gain considerable power when applied in a programming technique where "all sorts of sets of parameters" are stored in separate CfgBunch()-instances. Referencing a parameter according to the proposed technique makes as little difference as writing "self.clevername" versus "self.cfg.clevername". The benefits are:\n- having as many namespaces as needed to organize parameters\n- ease of use\n- possibility to easily pass sets of parameters around\n- great help in documentation