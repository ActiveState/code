#!/usr/bin/python
# Program to delete *.info files
#
# Copyleft  2011  Samuele Millevolte
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# print progress bar given the max level and what has been done
# max: it indicates the 100% level
# done: it indicates  ( done <= max )
def print_progress_bar(max, done):
	sys.stdout.write ("\r")
	sys.stdout.write ("[")
	x = int((done/max)*100)
	inner_bar = ['#' for i in range(x/10)] + [" " for i in range(10 - (x/10))]
	sys.stdout.write("".join(inner_bar))
	sys.stdout.write("]")
	sys.stdout.write(" "+str(x))
	sys.stdout.write("%")
	sys.stdout.flush()
	time.sleep(1) # only for test
	

# test code
if __name__ == '__main__':
	for i in range(1,101):
		print_progress_bar(100.0, float(i))
