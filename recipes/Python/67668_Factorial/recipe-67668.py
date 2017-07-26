#calculates factorial and for n <=1 n! = 1
fac = lambda n:n-1 + abs(n-1)and fac(n-1)*n or 1L
#another version
fac = lambda n:[1,0][n>0] or fac(n-1)*n
#and another
fac = lambda n:reduce(lambda a,b:a*(b+1),range(n),1)
