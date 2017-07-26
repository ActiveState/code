import sys

printf = lambda fmt,*args: sys.stdout.write(fmt%args)

printf ("This is a %s of %is of possibilities of %s","test",1000,printf)
