# Issued as CC0, 2017, Public Domain, B.Walker, G0LCU.
import sys

echo=sys.stdout.write

newline="\n"
char="!"
num=1
strng1="Python Version "
strng2=".4.0 for the AMIGA to 3.5.x"

echo("This works from %s%u%s on any platform%c%c" %(strng1, num, strng2, char, newline))

# sys.stdout.flush()
