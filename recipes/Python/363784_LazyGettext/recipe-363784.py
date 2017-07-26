"""Lazily translate strings declared as globals."""

from UserString import UserString


class LazyGettext(UserString, object):

    def get_data(self): 
        return self.translate(self.__data)

    def set_data(self, value):
        self.__data = value

    data = property(get_data, set_data, None,
        """UserString stores the underlying string here.

        I have a set method that accepts the untranslated string.  I have a get
        method that returns the translated version of the string.

        """)

    def translate(self, s):
        """This is just "sample code", but you get the idea."""
        print "What language would you like to translate s to?"
        return "%s: %s" % (raw_input(), s)

    def __mod__(self, arg):
        """Fix UserString.__mod__ which will fail here.

        Somehow, it evaluates the data twice.
        
        """
        s = self.data
        return s % arg 


# Initially:
module_string = "Hi, my name is %s"

# Later, from another module:
module_string = LazyGettext(module_string)
print module_string % "JJ"
