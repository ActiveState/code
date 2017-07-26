## Simple Python Checker  
Originally published: 2012-01-22 16:41:07  
Last updated: 2012-01-24 21:37:33  
Author: Thomas Lehmann  
  
**Why this recipe?**:
 * pylint is great but I does not support newer python versions.
 * I intended to write an own more simple parser recognizing that Python is doing the job for me and so I started to learn - a little - how to use AST.

**In scope (for this recipe)**:
 * scanning a single python file displaying warnings and errors when breaking rules.
 * easy to maintain and easy extensible.
 * reporting messages in a way - when displayed in an editor - you can click on them to jump to the location for the relating message.
 * Lines of code means: without blanks (later: also without comments)

**Out of scope (for this recipe)**:
 * For the recipe the folder/path support would break my limits. This include also the possible limits for this.
 * Checking for comments (SIngle line comments, block comments, checking for parameter documentation)

**Future:**
 * I'm thinking about putting this on a project base location (issue tracker, versioning, ...).
 * Of course same free license.
 * Providing a link here.
 * Checking for comments to handle further limits (LOC/COM, COM, checking for tags vs. parameters).
 * Allow to handle a path/folder with Python files (another statistic output)
