#this one liner will add each column
#and return the added columns as list

#adds all columns
addCol1 = lambda lines:apply(map,(lambda *args:reduce(lambda a,v:(a and float(a) or 0)+(v and float(v) or 0),args,0),)+tuple(map(lambda l:l.split(),lines)))

#adds only those columns which are complete
addCol2 = lambda lines:[reduce(lambda a,v:float(a)+float(v),col,0) for col in apply(zip,tuple([l.split() for l in lines]))]

#simulating... lines = open(file,'r').readlines()
lines = ['1 2 3 4',
         '3 4 5',
         '5 6 7',
         '8 0 9']

print addCol1(lines)
print addCol2(lines)
