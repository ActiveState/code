#!/usr/bin/python

import random
from urllib import urlopen

class Trigram:
    """From one or more text files, the frequency of three character
    sequences is calculated.  When treated as a vector, this information
    can be compared to other trigrams, and the difference between them
    seen as an angle.  The cosine of this angle varies between 1 for
    complete similarity, and 0 for utter difference.  Since letter
    combinations are characteristic to a language, this can be used to
    determine the language of a body of text. For example:

        >>> reference_en = Trigram('/path/to/reference/text/english')
        >>> reference_de = Trigram('/path/to/reference/text/german')
        >>> unknown = Trigram('url://pointing/to/unknown/text')
        >>> unknown.similarity(reference_de)
        0.4
        >>> unknown.similarity(reference_en)
        0.95

    would indicate the unknown text is almost cetrtainly English.  As
    syntax sugar, the minus sign is overloaded to return the difference
    between texts, so the above objects would give you:

        >>> unknown - reference_de
        0.6
        >>> reference_en - unknown    # order doesn't matter.
        0.05

    As it stands, the Trigram ignores character set information, which
    means you can only accurately compare within a single encoding
    (iso-8859-1 in the examples).  A more complete implementation might
    convert to unicode first.

    As an extra bonus, there is a method to make up nonsense words in the
    style of the Trigram's text.

        >>> reference_en.makeWords(30)
        My withillonquiver and ald, by now wittlectionsurper, may sequia,
        tory, I ad my notter. Marriusbabilly She lady for rachalle spen
        hat knong al elf

    Beware when using urls: HTML won't be parsed out.

    Most methods chatter away to standard output, to let you know they're
    still there.
    """
    length = 0

    def __init__(self, fn=None):
        self.lut = {}
        if fn is not None:
            self.parseFile(fn)

    def parseFile(self, fn):
        pair = '  '
        if '://' in fn:
            print "trying to fetch url, may take time..."
            f = urlopen(fn)
        else:
            f = open(fn)
        for z, line in enumerate(f):
            if not z % 1000:
                print "line %s" % z
            # \n's are spurious in a prose context
            for letter in line.strip() + ' ':
                d = self.lut.setdefault(pair, {})
                d[letter] = d.get(letter, 0) + 1
                pair = pair[1] + letter
        f.close()
        self.measure()


    def measure(self):
        """calculates the scalar length of the trigram vector and
        stores it in self.length."""
        total = 0
        for y in self.lut.values():
            total += sum([ x * x for x in y.values() ])
        self.length = total ** 0.5

    def similarity(self, other):
        """returns a number between 0 and 1 indicating similarity.
        1 means an identical ratio of trigrams;
        0 means no trigrams in common.
        """
        if not isinstance(other, Trigram):
            raise TypeError("can't compare Trigram with non-Trigram")
        lut1 = self.lut
        lut2 = other.lut
        total = 0
        for k in lut1.keys():
            if k in lut2:
                a = lut1[k]
                b = lut2[k]
                for x in a:
                    if x in b:
                        total += a[x] * b[x]

        return float(total) / (self.length * other.length)

    def __sub__(self, other):
        """indicates difference between trigram sets; 1 is entirely
        different, 0 is entirely the same."""
        return 1 - self.similarity(other)


    def makeWords(self, count):
        """returns a string of made-up words based on the known text."""
        text = []
        k = '  '
        while count:
            n = self.likely(k)
            text.append(n)
            k = k[1] + n
            if n in ' \t':
                count -= 1
        return ''.join(text)


    def likely(self, k):
        """Returns a character likely to follow the given string
        two character string, or a space if nothing is found."""
        if k not in self.lut:
            return ' '
        # if you were using this a lot, caching would a good idea.
        letters = []
        for k, v in self.lut[k].items():
            letters.append(k * v)
        letters = ''.join(letters)
        return random.choice(letters)


def test():
    en = Trigram('http://gutenberg.net/dirs/etext97/lsusn11.txt')
   #NB fr and some others have English license text.
    #   no has english excerpts.
    fr = Trigram('http://gutenberg.net/dirs/etext03/candi10.txt')
    fi = Trigram('http://gutenberg.net/dirs/1/0/4/9/10492/10492-8.txt')
    no = Trigram('http://gutenberg.net/dirs/1/2/8/4/12844/12844-8.txt')
    se = Trigram('http://gutenberg.net/dirs/1/0/1/1/10117/10117-8.txt')
    no2 = Trigram('http://gutenberg.net/dirs/1/3/0/4/13041/13041-8.txt')
    en2 = Trigram('http://gutenberg.net/dirs/etext05/cfgsh10.txt')
    fr2 = Trigram('http://gutenberg.net/dirs/1/3/7/0/13704/13704-8.txt')
    print "calculating difference:"
    print "en - fr is %s" % (en - fr)
    print "fr - en is %s" % (fr - en)
    print "en - en2 is %s" % (en - en2)
    print "en - fr2 is %s" % (en - fr2)
    print "fr - en2 is %s" % (fr - en2)
    print "fr - fr2 is %s" % (fr - fr2)
    print "fr2 - en2 is %s" % (fr2 - en2)
    print "fi - fr  is %s" % (fi - fr)
    print "fi - en  is %s" % (fi - en)
    print "fi - se  is %s" % (fi - se)
    print "no - se  is %s" % (no - se)
    print "en - no  is %s" % (en - no)
    print "no - no2  is %s" % (no - no2)
    print "se - no2  is %s" % (se - no2)
    print "en - no2  is %s" % (en - no2)
    print "fr - no2  is %s" % (fr - no2)

    print "\nmaking up English"
    print en.makeWords(30)
    print "\nmaking up French"
    print fr.makeWords(30)


if __name__ == '__main__':
    test()
