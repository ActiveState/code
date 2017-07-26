###string Formatter that renders None values as empty strings

Originally published: 2010-05-14 18:35:26
Last updated: 2010-05-14 18:35:27
Author: Antonio Cuni

This string Formatter works exactly as the default string.Formatter one (i.e., as str.format), with the exception that None values are rendered as empty strings instead of "None".  Moreover, any attempt to access attributes or items of None values is rendered as an empty string as well, instead of raising an exception.  \nE.g. fmt.format('{a}{a.foo}{a[0]}', a=None) == ''\n\nThis is useful e.g. when filling a template with values that are fetched from a DB, where usually None means empty.