# strings are immutable, so you need to make a copy -- and a list
# is the right intermediate datastructure, as it has a .reverse()
# method that does just what we want -- it works in-place, so...:
revchars = list(astring)        # string -> list of chars
revchars.reverse()              # inplace reverse the list
revchars = ''.join(revchars)    # list of strings -> string

# to flip words, we just work with a list-of-words instead:
revwords = astring.split()      # string -> list of words
revwords.reverse()              # inplace reverse the list
revwords = ' '.join(revwords)   # list of strings -> string

# note we use a ' ' (space) joiner for the list of words, but
# a '' (empty string) joiner for the list of characters.

# if you INSIST on oneliners, you need an auxiliary function
# (you can stick it in your builtins from sitecustomize.py...)
def reverse(alist):
    temp = alist[:]
    temp.reverse()
    return temp
# or maybe (NOT a good idea... it's messier & slower!!!):
def reverse_alternative(alist):
    return [alist[i] for i in range(-1, -len(alist)-1, -1)]
# which is "inlineable"... but *NOT* worth it...!!!

# anyway, now you CAN do brave oneliners such as:
revchars = ''.join(reverse(list(astring)))
revwords = ' '.join(reverse(astring.split()))

# the three-liners are faster and more readable, as well as
# more-idiomatic Python, but in the end Python does *NOT*
# twist your arm to make you choose the obviously-right approach:
# Python gives you the right tools, it's up to you to use them:-).

# to reverse-by-words while preserving untouched the intermediate
# whitespace, regular expression splitting can be used:
import re
revwords = re.split(r'(\s+)', astring)    # separators too since '(...)'
revwords.reverse()              # inplace reverse the list
revwords = ''.join(revwords)    # list of strings -> string
# *NOTE* the nullstring-joiner once again!
