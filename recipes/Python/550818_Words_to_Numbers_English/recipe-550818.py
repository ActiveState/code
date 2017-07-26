import re

class WordsToNumbers():
    """A class that can translate strings of common English words that
    describe a number into the number described
    """
    # a mapping of digits to their names when they appear in the
    # relative "ones" place (this list includes the 'teens' because
    # they are an odd case where numbers that might otherwise be called
    # 'ten one', 'ten two', etc. actually have their own names as single
    # digits do)
    __ones__ = { 'one':   1, 'eleven':     11,
                 'two':   2, 'twelve':     12,
                 'three': 3, 'thirteen':   13,
                 'four':  4, 'fourteen':   14,
                 'five':  5, 'fifteen':    15,
                 'six':   6, 'sixteen':    16,
                 'seven': 7, 'seventeen':  17,
                 'eight': 8, 'eighteen':   18,
                 'nine':  9, 'nineteen':   19 }
    
    # a mapping of digits to their names when they appear in the 'tens'
    # place within a number group
    __tens__ = { 'ten':     10,
                 'twenty':  20,
                 'thirty':  30,
                 'forty':   40,
                 'fifty':   50,
                 'sixty':   60,
                 'seventy': 70,
                 'eighty':  80,
                 'ninety':  90 }
    
    # an ordered list of the names assigned to number groups
    __groups__ = { 'thousand':  1000,
                   'million':   1000000,
                   'billion':   1000000000,
                   'trillion':  1000000000000 }

    # a regular expression that looks for number group names and captures:
    #     1-the string that preceeds the group name, and
    #     2-the group name (or an empty string if the
    #       captured value is simply the end of the string
    #       indicating the 'ones' group, which is typically
    #       not expressed)
    __groups_re__ = re.compile(
        r'\s?([\w\s]+?)(?:\s((?:%s))|$)' %
        ('|'.join(__groups__))
        )

    # a regular expression that looks within a single number group for
    # 'n hundred' and captures:
    #    1-the string that preceeds the 'hundred', and
    #    2-the string that follows the 'hundred' which can
    #      be considered to be the number indicating the
    #      group's tens- and ones-place value
    __hundreds_re__ = re.compile(r'([\w\s]+)\shundred(?:\s(.*)|$)')

    # a regular expression that looks within a single number
    # group that has already had its 'hundreds' value extracted
    # for a 'tens ones' pattern (ie. 'forty two') and captures:
    #    1-the tens
    #    2-the ones
    __tens_and_ones_re__ =  re.compile(
        r'((?:%s))(?:\s(.*)|$)' %
        ('|'.join(__tens__.keys()))
        )

    def parse(self, words):
        """Parses words to the number they describe"""
        # to avoid case mismatch, everything is reduced to the lower
        # case
        words = words.lower()
        # create a list to hold the number groups as we find them within
        # the word string
        groups = {}        
        # create the variable to hold the number that shall eventually
        # return to the caller
        num = 0
        # using the 'groups' expression, find all of the number group
        # an loop through them
        for group in WordsToNumbers.__groups_re__.findall(words):
            ## determine the position of this number group
            ## within the entire number
            # assume that the group index is the first/ones group
            # until it is determined that it's a higher group
            group_multiplier = 1
            if group[1] in WordsToNumbers.__groups__:
                group_multiplier = WordsToNumbers.__groups__[group[1]]
            ## determine the value of this number group
            # create the variable to hold this number group's value
            group_num = 0
            # get the hundreds for this group
            hundreds_match = WordsToNumbers.__hundreds_re__.match(group[0])
            # and create a variable to hold what's left when the
            # "hundreds" are removed (ie. the tens- and ones-place values)
            tens_and_ones = None
            # if there is a string in this group matching the 'n hundred'
            # pattern
            if hundreds_match is not None and hundreds_match.group(1) is not None:
                # multiply the 'n' value by 100 and increment this group's
                # running tally
                group_num = group_num + \
                            (WordsToNumbers.__ones__[hundreds_match.group(1)] * 100)
                # the tens- and ones-place value is whatever is left
                tens_and_ones = hundreds_match.group(2)
            else:
            # if there was no string matching the 'n hundred' pattern,
            # assume that the entire string contains only tens- and ones-
            # place values
                tens_and_ones = group[0]
            # if the 'tens and ones' string is empty, it is time to
            # move along to the next group
            if tens_and_ones is None:
                # increment the total number by the current group number, times
                # its multiplier
                num = num + (group_num * group_multiplier)
                continue
            # look for the tens and ones ('tn1' to shorten the code a bit)
            tn1_match = WordsToNumbers.__tens_and_ones_re__.match(tens_and_ones)
            # if the pattern is matched, there is a 'tens' place value
            if tn1_match is not None:
                # add the tens
                group_num = group_num + WordsToNumbers.__tens__[tn1_match.group(1)]
                # add the ones
                if tn1_match.group(2) is not None:
                    group_num = group_num + WordsToNumbers.__ones__[tn1_match.group(2)]
            else:
            # assume that the 'tens and ones' actually contained only the ones-
            # place values
                group_num = group_num + WordsToNumbers.__ones__[tens_and_ones]
            # increment the total number by the current group number, times
            # its multiplier
            num = num + (group_num * group_multiplier)
        # the loop is complete, return the result
        return num            
        
if __name__ == "__main__":
    # here is an example you can use to test the results
    nums = [
        "one", "twenty six", "one hundred", "five thousand nineteen",
        "one hundred forty", "three hundred forty five",
        "sixteen hundred", "one thousand six hundred",
        "fifty five thousand", "fifty five thousand six",
        "six hundred twenty three million twenty one thousand forty one"
        ]
    wtn = WordsToNumbers()
    for num in nums:
        print num, ": ", wtn.parse(num)
