def groupbyhead(items,headsize=1):
    '''
    groupbyhead(items,headsize=1)
    =============================
    
    Group a list of items according to the starting character(s) of items.
    Return a dictionary.

    :Author:  Runsun Pan
    :Date:    1/1/06
    :Required: Raymond Hettinger's groupby class
               http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/259173
    Usage
    -----
    ::
    
        >>> states = ['Alaska','Arizona','Arkansas','California','Colorado',
        'Connecticut','Georgia','Idaho','Illinois','Indiana','Iowa','Kansas',
        'Kentucky','Maine','Maryland', 'Michigan','Minnesota','Missouri','Montana']

        >>> x= groupbyhead(states)
        >>> print prndict(x, sortkey=1) #
        {
         'A':['Alaska', 'Arizona', 'Arkansas'],
         'C':['California', 'Colorado', 'Connecticut'],
         'G':['Georgia'],
         'I':['Idaho', 'Illinois', 'Indiana', 'Iowa'],
         'K':['Kansas', 'Kentucky'],
         'M':['Maine', 'Maryland',  'Michigan', 'Minnesota', 'Missouri', 'Montana']
        }
        
        >>> x= groupbyhead(states,2)
        >>> print prndict(x, sortkey=1)   # 
        {
         'Al':['Alaska'],
         'Ar':['Arizona', 'Arkansas'],
         'Ca':['California'],
         'Co':['Colorado', 'Connecticut'],
         'Ge':['Georgia'],
         'Id':['Idaho'],
         'Il':['Illinois'],
         'In':['Indiana'],
         'Io':['Iowa'],
         'Ka':['Kansas'],
         'Ke':['Kentucky'],
         'Ma':['Maine', 'Maryland'],
         'Mi':['Michigan', 'Minnesota', 'Missouri'],
         'Mo':['Montana']
        }

     # prndict: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/327142
     '''
    return dict( [(k,g) for k, g in groupby(items, key=lambda x:x[0:headsize])] )
