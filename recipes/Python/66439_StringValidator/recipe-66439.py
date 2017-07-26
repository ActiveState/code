import re
true = 1
false = 0

class StringValidator:
	RE_ALPHA = None
	RE_ALPHANUMERIC = None
	RE_NUMERIC = None
	RE_EMAIL = None

	validateString = ""
        _patterns = {}

	def __init__(self, validateString):
		self.validateString = validateString

	def isAlpha(self):
                if not self.__class__.RE_ALPHA:
                        self.__class__.RE_ALPHA = re.compile("^\D+$")
                return self.checkStringAgainstRe(self.__class__.RE_ALPHA)

	def isAlphaNumeric(self):
                if not self.__class__.RE_ALPHANUMERIC:
                        self.__class__.RE_ALPHANUMERIC = re.compile("^[a-zA-Z0-9]+$")
                return self.checkStringAgainstRe(self.__class__.RE_ALPHANUMERIC)

	def isNumeric(self):
                if not self.__class__.RE_NUMERIC:
                        self.__class__.RE_NUMERIC = re.compile("^\d+$")
                return self.checkStringAgainstRe(self.__class__.RE_NUMERIC)

	def isEmail(self):
                if not self.__class__.RE_EMAIL:
                        self.__class__.RE_EMAIL = re.compile("^.+@.+\..{2,3}$")
                return self.checkStringAgainstRe(self.__class__.RE_EMAIL)

	def isEmpty(self):
		return self.validateString == ""

        def definePattern(self, re_name, re_pat):
                self._patterns[re_name] = re_pat

        def isValidForPattern(self, re_name):
                if self._patterns.has_key(re_name):
                        if type(self._patterns[re_name]) == type(''):
                                self._patterns[re_name] = re.compile(self._patterns[re_name])
                                return self.checkStringAgainstRe(self._patterns[re_name])
                else:
                        raise KeyError, "No pattern name '%s' stored."

	# this method should be considered to be private (not be be used via interface)

	def checkStringAgainstRe(self, regexObject):
		if regexObject.search(self.validateString) == None:
			return false
		return true

# example usage

sv1 = StringValidator("joe@testmail.com")
sv2 = StringValidator("rw__343")

if sv1.isEmail(): print sv1.validateString + " is a valid e-mail address"
else: print sv1.validateString + " is not a valid e-mail address"

if sv2.isAlphaNumeric(): print sv2.validateString + " is a valid alpha-numeric string"
else: print sv2.validateString + "i is not a valid alpha-numeric string"

# note, this is basically the same as the e-mail checker, just it shows
# how to do a custom re
sv2.definePattern("custom_email", "^.+@.+\..{2,3}$")

if sv1.isValidForPattern("custom_email"): print sv1.validateString + " is a valid e-mail address"
else: print sv1.validateString + " is a invalid e-mail address"
