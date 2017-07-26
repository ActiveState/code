## Fix up a message returned by Python 2.4's email module's feed parserOriginally published: 2004-09-02 19:00:40 
Last updated: 2004-10-03 17:47:44 
Author: Matthew Cowles 
 
For good reasons, the email module's new feed parser can return a message that's internally inconsistent. This recipe fixes up one sort of inconsistency that I've seen in the wild.