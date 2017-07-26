It's easy, once you accept the need
to explicitely convert between a bytestring and a unicode string:

    >>> german_ae = unicode('\xc3\xa4', 'utf8')

Here german_ae is a unicode string representing the german
"lowercase a with umlaut".  It has been constructed from interpreting the bytestring '\xc3\xa4' according to the specified UTF8 encoding.
There are many encodings, but UTF8 is often used because it is
universal and yet fully compatible with the 7-bit ASCII set (any ASCII bytestring is a correct UTF8-encoded string).


Once you crossed this barrier, life is easy!  You can manipulate this
unicode string in practically the same way as a plain str string:

   >>> sentence = "This is a " + german_ae
   >>> sentence2 = "Easy!"
   >>> para = ". ".join([sentence, sentence2])

Note that para is a unicode string, because operations between a
unicode string and a byte string always result in a unicode string...
unless they fail and raise an exception:


   >>> bytestring = '\xc3\xa4'     # Uuh, some non-ASCII bytestring!
   >>> german_ae += bytestring
   UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in
   position 0: ordinal not in range(128)

The byte '0xc3' is not a valid character in the 7-bit
ASCII encoding, and Python refuses to guess an encoding.  So,
being explicit about encodings is the crucial point about successfully
using unicode strings with Python.
