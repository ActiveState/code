#!/usr/bin/python

import re

class PyBoolReException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    
class PyBoolRe:
    """ A class to perform boolean word matches in
    a string or paragraph. This class allows you to
    perform complex matches in a string or group of
    words by creating simple boolean expressions,
    grouped by parantheses to create complex match
    expressions.

    Author: Anand B Pillai, http://tinyurl.com/yq3y
    Copyright: None
    LICENSE: GPL
    Version: 0.2
    
    Usage:

    1. Create regular expressions using the boolean
       keywords '|' and '&', standing for 'OR' and
       'AND' respectively.
    2. Use parantheses to group the boolean expressions
       to create complex match expressions.
    3. Caveats:

       1. Fails for expressions with redundant parens such
       as ((A | B)) etc.
       

    Example:
    
    p = PyBoolRe('Guido & Python')
    s = 'Guido created Python'
    mobject = p.match(s)
    
    # Work with 'mobject' like you normally work with
    # regular expression match objects
      
    """
    
    def __init__(self, boolstr):
        # Require whitespace  before words?
        self.__needspace = True
        # whitespace re
        self._wspre = re.compile('^\s*$')
        # create regexp string
        self.__rexplist = []
        oparct = boolstr.count('(')
        clparct = boolstr.count(')')
        if oparct != clparct:
            raise PyBoolReException, 'Mismatched parantheses!'

        self.__parse(boolstr)
        # if NOT is one of the members, reverse
        # the list
        # print self.__rexplist
        if '!' in self.__rexplist:
            self.__rexplist.reverse()

        s = self.__makerexp(self.__rexplist)
        # print s
        self.__rexp = re.compile(s)

    def match(self, data):
        """ Match the boolean expression, behaviour
        is same as the 'match' method of re """
        
        return self.__rexp.match(data)

    def search(self, data):
        """ Search the boolean expression, behaviour
        is same as the 'search' method of re """

        return self.__rexp.search(data)

    def __parse(self, s):
        """ Parse the boolean regular expression string
        and create the regexp list """

        # The string is a nested parantheses with
        # any character in between the parens.

        scopy = s[:]
        oparmatch, clparmatch = False, False

        # Look for a NOT expression
        index = scopy.rfind('(')

        l = []
        if index != -1:
            oparmatch = True
            index2 = scopy.find(')', index)
            if index2 != -1:
                clparmatch = True
                newstr = scopy[index+1:index2]
                # if the string is only of whitespace chars, skip it
                if not self._wspre.match(newstr):
                    self.__rexplist.append(newstr)
                replacestr = '(' + newstr + ')'
                scopy = scopy.replace(replacestr, '')
                    
                self.__parse(scopy)
                
        if not clparmatch and not oparmatch:
            if scopy: self.__rexplist.append(scopy)

    def is_inbetween(self, l, elem):
        """ Find out if an element is in between
        in a list """

        index = l.index(elem)
        if index == -1:
            return False

        if index>2:
            if index in range(1, len(l) -1):
                return True
            else:
                return False
        else:
            return True

    def __makenotexpr(self, s):
        """ Make a NOT expression """

        if s.find('!') == 0:
            return ''.join(('(?!', s[1:], ')'))
        else:
            return s
                          
    def __makerexp(self, rexplist):
        """ Make the regular expression string for
        the boolean match from the nested list """

        
        is_list = True

        if type(rexplist) is str:
            is_list = False
            elem = rexplist
        elif type(rexplist) is list:
            elem = rexplist[0]

        if type(elem) is list:
            elem = elem[0]
            
        eor = False
        if not is_list or len(rexplist) == 1:
            eor = True

        word_str = '.*'
        
        s=''
        # Implementing NOT
        if elem == '!':
            return ''.join(('(?!', self.__makerexp(rexplist[1:]), ')'))
        # Implementing OR
        elif elem.find(' | ') != -1:
            listofors = elem.split(' | ')

            for o in listofors:
                index = listofors.index(o)
                in_bet = self.is_inbetween(listofors, o)

                if o:
                    o = self.__makenotexpr(o)
                    if in_bet:
                        s = ''.join((s, '|', word_str, o, '.*'))
                    else:
                        s = ''.join((s, word_str, o, '.*'))

        # Implementing AND
        elif elem.find(' & ') != -1:
            listofands = elem.split(' & ')
            
            for a in listofands:
                index = listofands.index(a)
                in_bet = self.is_inbetween(listofands, a)                

                if a:
                    a = self.__makenotexpr(a)                   
                    s = ''.join((s, word_str, a, '.*'))

        else:
            if elem:
                elem = self.__makenotexpr(elem)             
                s = ''.join((elem, '.*'))

        if eor:
            return s
        else:
            return ''.join((s, self.__makerexp(rexplist[1:])))
            
                    
if __name__=="__main__":
    p = PyBoolRe('(!Guido)')
    
    s1 = 'Guido invented Python and Larry invented Perl'
    s2 = 'Larry invented Perl, not Python'
    
    if p.match(s1):
       print 'Match found for first string'
    else:
       print 'No match found for first string'

    if p.match(s2):
       print 'Match found for second string'
    else:
       print 'No match found for second string'
        
        

        
