## String templates with adaptive indenting  
Originally published: 2014-02-19 12:35:46  
Last updated: 2014-02-19 12:53:03  
Author: Sander Evers  
  
An extension of Python's `'Hello {fieldname}!'.format(fieldname='world')` functionality for multi-line strings. When `{fieldname}` is indented, all the lines in the inserted `fieldvalue` are indented to the same amount.