## Parsing out EDI messages 
Originally published: 2004-08-12 09:36:18 
Last updated: 2004-08-12 09:36:18 
Author: Chris Cioffi 
 
A parser I designed to work with HIPAA EDI files.  It reads in files and spits out the individual segments without terminators.\n\nRequires Python 2.3 or greater.  (Use can probably use Python 2.2 with from __future__ import generators at the top...)