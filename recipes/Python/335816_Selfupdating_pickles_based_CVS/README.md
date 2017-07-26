## Self-updating pickles, based on CVS revision string  
Originally published: 2004-11-16 11:39:03  
Last updated: 2004-11-16 11:39:03  
Author: Lonnie Princehouse  
  
One of the problems with persistent objects is that one often needs a mechanism to keep them in sync with the codebase.  This provides such a mechanism for pickled objects under the control of CVS via the magic CVS $Revision$ string, which CVS will automatically update to match a file's revision number.