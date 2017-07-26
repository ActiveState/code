## word wrap long line Java to limited line length with explicit backslashes  
Originally published: 2005-09-30 10:45:11  
Last updated: 2005-09-30 17:54:57  
Author: Christopher Morley  
  
This recipe is based off of
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061

I found and used the recipe above, however, I took issue with the results.  See, I wanted to use it on a big Java file that had lots of long lines.  With extra long package names, and extra long lines containing multiple semicolons without spaces after them, I found it necessary to modify this algorithm to suit my specific purposes.

If you have a line like this:

import com.jobsintheus.vaccinium.controller.ejb.stateful.VacciniumStatefulSessionRemoteHome;

you're going to have problems using the above algorithm, but the one herein does something useful with that - splitting the line on the periods too.  It works for semicolons too.

Inserted line breaks will become the visible backslash charater plus the line break.

Otherwise, line breaks that existed before stay as is (with no visible backslash character).

The point is to have the Java code be a readable addition as an input file to (la)tex verbatim.