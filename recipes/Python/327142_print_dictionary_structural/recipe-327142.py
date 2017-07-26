def prnDict(aDict, br='\n', html=0,
            keyAlign='l',   sortKey=0,
            keyPrefix='',   keySuffix='',
            valuePrefix='', valueSuffix='',
            leftMargin=0,   indent=1 ):
    '''
return a string representive of aDict in the following format:
    {
     key1: value1,
     key2: value2,
     ...
     }

Spaces will be added to the keys to make them have same width.

sortKey: set to 1 if want keys sorted;
keyAlign: either 'l' or 'r', for left, right align, respectively.
keyPrefix, keySuffix, valuePrefix, valueSuffix: The prefix and
   suffix to wrap the keys or values. Good for formatting them
   for html document(for example, keyPrefix='<b>', keySuffix='</b>'). 
   Note: The keys will be padded with spaces to have them
         equally-wide. The pre- and suffix will be added OUTSIDE
         the entire width.
html: if set to 1, all spaces will be replaced with '&nbsp;', and
      the entire output will be wrapped with '<code>' and '</code>'.
br: determine the carriage return. If html, it is suggested to set
    br to '<br>'. If you want the html source code eazy to read,
    set br to '<br>\n'

version: 04b52
author : Runsun Pan
require: odict() # an ordered dict, if you want the keys sorted.
         Dave Benjamin 
         http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/161403
    '''
   
    if aDict:

        #------------------------------ sort key
        if sortKey:
            dic = aDict.copy()
            keys = dic.keys()
            keys.sort()
            aDict = odict()
            for k in keys:
                aDict[k] = dic[k]
            
        #------------------- wrap keys with ' ' (quotes) if str
        tmp = ['{']
        ks = [type(x)==str and "'%s'"%x or x for x in aDict.keys()]

        #------------------- wrap values with ' ' (quotes) if str
        vs = [type(x)==str and "'%s'"%x or x for x in aDict.values()] 

        maxKeyLen = max([len(str(x)) for x in ks])

        for i in range(len(ks)):

            #-------------------------- Adjust key width
            k = {1            : str(ks[i]).ljust(maxKeyLen),
                 keyAlign=='r': str(ks[i]).rjust(maxKeyLen) }[1]
            
            v = vs[i]        
            tmp.append(' '* indent+ '%s%s%s:%s%s%s,' %(
                        keyPrefix, k, keySuffix,
                        valuePrefix,v,valueSuffix))

        tmp[-1] = tmp[-1][:-1] # remove the ',' in the last item
        tmp.append('}')

        if leftMargin:
          tmp = [ ' '*leftMargin + x for x in tmp ]
          
        if html:
            return '<code>%s</code>' %br.join(tmp).replace(' ','&nbsp;')
        else:
            return br.join(tmp)     
    else:
        return '{}'

'''
Example:

>>> a={'C': 2, 'B': 1, 'E': 4, (3, 5): 0}

>>> print prnDict(a)
{
 'C'   :2,
 'B'   :1,
 'E'   :4,
 (3, 5):0
}

>>> print prnDict(a, sortKey=1)
{
 'B'   :1,
 'C'   :2,
 'E'   :4,
 (3, 5):0
}

>>> print prnDict(a, keyPrefix="<b>", keySuffix="</b>")
{
 <b>'C'   </b>:2,
 <b>'B'   </b>:1,
 <b>'E'   </b>:4,
 <b>(3, 5)</b>:0
}

>>> print prnDict(a, html=1)
<code>{
&nbsp;'C'&nbsp;&nbsp;&nbsp;:2,
&nbsp;'B'&nbsp;&nbsp;&nbsp;:1,
&nbsp;'E'&nbsp;&nbsp;&nbsp;:4,
&nbsp;(3,&nbsp;5):0
}</code>

>>> b={'car': [6, 6, 12], 'about': [15, 9, 6], 'bookKeeper': [9, 9, 15]}

>>> print prnDict(b, sortKey=1)
{
 'about'     :[15, 9, 6],
 'bookKeeper':[9, 9, 15],
 'car'       :[6, 6, 12]
}

>>> print prnDict(b, keyAlign="r")
{
        'car':[6, 6, 12],
      'about':[15, 9, 6],
 'bookKeeper':[9, 9, 15]
}
'''
