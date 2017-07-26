# Amazing quick
def expandtab(str,tab=8):
   return reduce(lambda a,b: 
                      a + ' '*(tab-len(a)%tab) + b,
                      str.split('\t')
                )
