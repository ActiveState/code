class RichCmpMixin(object):
    """
    Define __cmp__, and inherit from this class to provide full rich
    comparisons.
    """

    def __eq__(self, other):
        return self.__cmp__(other)==0
    
    def __ne__(self, other):
        return self.__cmp__(other)!=0

    def __lt__(self, other):
        return self.__cmp__(other)==-1
    
    def __le__(self, other):
        return self.__cmp__(other)!=1

    def __gt__(self, other):
        return self.__cmp__(other)==1

    def __ge__(self, other):
        return self.__cmp__(other)!=-1
