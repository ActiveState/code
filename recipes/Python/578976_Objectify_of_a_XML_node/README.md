## Objectify of a XML node 
Originally published: 2014-12-05 04:39:51 
Last updated: 2014-12-05 04:39:51 
Author: Thomas Lehmann 
 
The script allows you to convert a XML node into an object instance that has the XML node attributes as fields with the given values. The values are converted (when possible):\n\n - from string to int\n - from string to float\n - or remain as string\n\nYou also initially can provide a dictionary of (key,value) to ensure existence of certain fields which might not be provided by the XML node but on the other hand those values might be overwritten by the XML node.\n\nPlease have a look at the docstring for the example ...