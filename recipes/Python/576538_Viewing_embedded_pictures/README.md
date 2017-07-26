## Viewing embedded pictures within docstrings 
Originally published: 2008-10-15 01:27:26 
Last updated: 2008-10-15 01:27:26 
Author: Andre Roberge 
 
Python docstrings are textual information about objects.  They can be displayed via help(obj).  However, they can not contain images.  This recipe allows the inclusion of images (encoded in base 64 in the Python file) inside docstrings in a transparent way.  The images are indicated as "docpicture = file_name.ext" inside the docstring, and the encoded data is in variable "file_name" inside the same module.