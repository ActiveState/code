##
## pgenerate.py v0.1
##
## Randomly creates a password with specified length, or picks
## a password from a dictionary. Also randomly warps the characters,
## making passwords from a dictionary more or less readable but
## slightly more difficult to crack.
##
##
## Author: Rikard Bosnjakovic <bos@hack.org>, 2001-06-12
##
from whrandom import choice, randint

# choose your dictionary
dictionary_file = '/usr/lib/ispell/american.med+'

class Pgenerate:
    """This class is a password generator.
Just inherit it (with optional arguments) and find the password in the class variable 'password'."""
    def __init__(self, min_chars = 6, use_dictionary = 0):
        # auto-generate a password with minimum 6 chars when inherited
        self.password = ""
        self.create_password(min_chars, use_dictionary)

    def fetch_word_from_dictionary(self, min_chars):
        """Get a word from a dictionary with minimum [min_chars] characters."""
        word  = ""
        words = open(dictionary_file, "r").readlines()
        while len(word) < min_chars:
            word = choice(words)

        word = word.lower().strip()
        return word

    def warp_password(self):
        """Warps around the chars in the password."""
        import string

        warps = {}
        # add the alphabet to the warplist
        for x in xrange(ord('a'), ord('z')+1):
            x = chr(x)
            warps[x] = [x, x.upper()]

        # add some specials
        specialchars = (("a", ["@", "4"]),
                        ("e", ["3"]),
                        ("g", ["6"]),
                        ("i", ["1", "|", "!"]),
                        ("l", ["1", "|", "!"]),
                        ("o", ["0"]),
                        ("s", ["5", "z", "Z"]),
                        ("t", ["+", "7"]),
                        ("z", ["s", "S", "2"]))

        for (a,b) in specialchars:
            warps[a] += b

        randoms = 0
        warped_password = ""
        # warp the chars in the password
        for i in self.password:
            if i in warps.keys():
                # 75% probability
                if randint(0, 3):
                    warped_password += choice(warps[i])
                else:
                    warped_password += i
            else:
                warped_password += i

            # add a random character (max two)
            if randint(0, 5) == 0 and randoms < 2:
                warped_password += choice("\/_.,!;:'+-=")
                randoms += 1

#        print "unwarped pass = ", self.password
#        print "warped pass   = ", warped_password

        return warped_password

    def generate_password(self, min_chars):
        """generate_password(min_chars):
Randomly creates a password with minimum [min_chars] length."""

        valid_chars = "abcdefghijklmnopqrstuvwxyz0123456789,.-;:_\/!\"'#%&()="
        password = ""

        # the length will be min_chars plus a random value up to
        # and including min_chars
        for i in xrange(0, min_chars+randint(0, min_chars)):
            password += choice(valid_chars)

        return password

    def create_password(self, min_chars, use_dictionary):
        """create_password([min_chars = 4, use_dictionary = 0]):
Either picks a password from a dictionary or generates one randomly, with minimum chars as specified (default 4)."""
        if use_dictionary:
            self.password = self.fetch_word_from_dictionary(min_chars)
        else:
            self.password = self.generate_password(min_chars)

        self.password = self.warp_password()


    def __repr__(self):
        return self.password
