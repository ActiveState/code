## ConfigObj - Lightweight Config File Parser  
Originally published: 2004-01-09 06:10:29  
Last updated: 2004-01-09 06:10:29  
Author: Michael Foord  
  
# A simple class of config object - allowing simple configs to be read in, updated in the file or rewritten out
# Preserves comments inline with the keywords
# Allows for multiple values - defined by the programmer what type of value a keyword is expected to have
# Will read only the specified values from a file - allows sections of a larger config file to be
# easily read and updated whilst preserving the rest of the file.
# outputs non-fatal error to the stout object - this could be turned into an exception handler if you wanted
# errors to be fatal instead of non-fatal.
#

# Maintained at www.voidspace.org.uk/atlantibots/pythonutils.html