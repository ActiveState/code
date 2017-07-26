#=======================================================================

__version__ = '''0.0.01'''
__sub_version__ = '''20041028004506'''
__copyright__ = '''(c) Alex A. Naanou 2003'''


#-----------------------------------------------------------------------
#------------------------------------------------------------_Compare---
class _Compare(object):
    '''
    '''
    def __init__(self, eq):
        self._eq = eq
    def __cmp__(self, other):
        return self._eq
    def __eq__(self, other):
        return self._eq == 0
    def __ne__(self, other):
        return self._eq != 0
    def __gt__(self, other):
        return self._eq > 0
    def __ge__(self, other):
        return self._eq >= 0
    def __lt__(self, other):
        return self._eq < 0
    def __le__(self, other):
        return self._eq <= 0

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# this will compare to any value as equal (almost opposite to None)
ANY = _Compare(0)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# this is bigger than any value... (absolute maximum)
MAXIMUM = _Compare(1)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# this is smaller than any value... (absolute minimum)
MINIMUM = _Compare(-1)


#=======================================================================
# NOTE: the MAXIMUM and MINIMUM objects are not discussed here as they 
#       are discussed in depth in PEP326 http://www.python.org/peps/pep-0326.html
if __name__ == '__main__':


    # Example I:
    # compare two objects by their structure...
    print (ANY, (ANY, ANY)) == (1, (2, 3))

    # the above comparison is eqivalent to:
    print (lambda o: \
                type(o) is tuple \
                    and len(o) == 2 \
                    and type(o[1]) is tuple \
                    and len(o[1]) == 2
          )( (1, (2, 3)) )


    # Example II:
    # compare structure and partial value...
    print ([ANY, 123], 'string', (ANY,), ANY) == ([2, 123], 'string', (0.1,), (1, 2,))

    # now try and imagine the explicit code to do the same thing as
    # above! :))



#=======================================================================
#                                            vim:set ts=4 sw=4 nowrap :
