## Reverse the sequence of annotations on a PDF pageOriginally published: 2016-12-13 22:18:02 
Last updated: 2017-01-22 14:02:16 
Author: Jorj X. McKie 
 
Just another demonstration of PyMuPDF's features to deal with annotations:\n\nTake a page with several annotations and let them change places in reverse order: first and last annot exchange their rectangles, second and second to last, etc.\n\nThe annotation images are enlarged or compressed as required to fit into their new areas.