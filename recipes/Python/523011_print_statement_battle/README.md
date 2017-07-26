## print statement: battle with UnicodeEncodeErrorOriginally published: 2007-07-01 23:35:39 
Last updated: 2009-02-10 07:22:46 
Author: Denis Barmenkov 
 
I received UnicodeEncodeError when playing with various codepages in source code/files/standard streams.\nSometime I receive UnicodeEncodeError when script launched via scheduler or in long running batch when parsing unpredictable [alien ;)] HTML.\n\nFunction console() helps avoid this exceptions by converting erroneous charatcters to standard python representation.\n\nto do in future: make a codec-wrapper for safe using in statements like this:\n\n    sys.stdout=codecs.getwriter('cp866')(sys.stdout)