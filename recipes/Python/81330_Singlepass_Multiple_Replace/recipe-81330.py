# Tested with Python 2.1
from __future__ import nested_scopes

import re 

#
# The simplest, lambda-based implementation
#

def multiple_replace(dict, text): 

  """ Replace in 'text' all occurences of any key in the given
  dictionary by its corresponding value.  Returns the new tring.""" 

  # Create a regular expression  from the dictionary keys
  regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 

#
# You may combine both the dictionnary and search-and-replace
# into a single object using a 'callable' dictionary wrapper
# which can be directly used as a callback object.
# 

# In Python 2.2+ you may extend the 'dictionary' built-in class instead
from UserDict import UserDict 
class Xlator(UserDict):

  """ An all-in-one multiple string substitution class """ 

  def _make_regex(self): 

    """ Build a regular expression object based on the keys of
    the current dictionary """

    return re.compile("(%s)" % "|".join(map(re.escape, self.keys()))) 

  def __call__(self, mo): 
    
    """ This handler will be invoked for each regex match """

    # Count substitutions
    self.count += 1 # Look-up string

    return self[mo.string[mo.start():mo.end()]]

  def xlat(self, text): 

    """ Translate text, returns the modified text. """ 

    # Reset substitution counter
    self.count = 0 

    # Process text
    return self._make_regex().sub(self, text)

#
# Test
# 

if __name__ == "__main__": 

  text = "Larry Wall is the creator of Perl"

  dict = {
    "Larry Wall" : "Guido van Rossum",
    "creator" : "Benevolent Dictator for Life",
    "Perl" : "Python",
  } 

  print multiple_replace(dict, text) 

  xlat = Xlator(dict)
  print xlat.xlat(text)
  print "Changed %d thing(s)" % xlat.count 
