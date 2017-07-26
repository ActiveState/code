'''
Created on 13 Sep 2013

@author: bakera
'''
import unittest

import numpy as np
import random

from ctypes import *

import sys

if ((sys.platform == 'linux2')):
    from termcolor import colored, cprint


def store_value(option, opt_str, value, parser):
    setattr(parser.values, option.dest, value)

class Cross():
    def __init__(self, n, filename='cross.dat'):
        
        
        if (not (sys.platform == 'linux2')):windll.Kernel32.GetStdHandle.restype = c_ulong
        if (not (sys.platform == 'linux2')):self.h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))    
        
        self.n = n
        np.savetxt('cross.dat', np.reshape(np.array([random.randint(0,1) for a in np.arange(0,self.n**2,1)]), (self.n,self.n))
, fmt="%d")
        self.c = cross = np.loadtxt('cross.dat', dtype='int')
    
        self.colour_map = {1: 12, 2: 12, 3: 13, 4: 14, 5: 15, 6: 9, 0:4} # empty cells colour black

    
    @property
    def grid(self):
        return self.c
       
    def prettyprint(self, special=[]):
        for i, row in enumerate(self.grid.flat):            
            i = i + 1
            color = self.colour_map[row]        
            if (not (sys.platform == 'linux2')):
            	if not i in special:
                	windll.Kernel32.SetConsoleTextAttribute(self.h, color)
                else:
                	windll.Kernel32.SetConsoleTextAttribute(self.h, 2)
                if i == 0:
                    sys.stdout.write("  %d" % (row)) 
                elif (i % self.n == 0) :
                    sys.stdout.write("  %d\n" % (row)) # include 2 spaces for the twissler
                    sys.stdout.flush()
                else:
                    sys.stdout.write("  %d" % (row)) # include 2 spaces for the twissler
                    
        if (not (sys.platform == 'linux2')):windll.Kernel32.SetConsoleTextAttribute(self.h, 15) # return to white        

    
    def iterate_trace(self):
        '''
            assuming smallest cross trace supported is a 3 by 3 matrix
        '''
        for t in np.arange(self.n+2, 2, -1):
        	yield t
    
    def is_cross(self, candidate):
        '''
            first check the trace
            then flip and check the opposite trace
        
        '''
        return (candidate.trace()+np.fliplr(candidate).trace()) == (candidate.shape[0]*2)
            
    def iterate_grid(self, n):
        '''
            iterate over the grid self.c passing back n * n instances that cover the whole grid
            
            n - size of the scan matrix
        
        '''
        for y in np.arange(0, self.grid.shape[1]-n, 1):            
            for x in np.arange(0, self.grid.shape[0]-n, 1):
                yield self.is_cross(self.grid[x:x+n, y:y+n]), self.grid[x:x+n, y:y+n], x, y
                        
if __name__ == "__main__":
    
    from optparse import OptionParser
        
    parser = OptionParser()
        
    # test and verbose flags
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="print debug")
    parser.add_option("-s", "--size", action="callback", callback=store_value, type="int", nargs=1, dest="size", help="specify matrix size")
    
    (options, args) = parser.parse_args()      
    
    if options.size and not options.size == 1:
    
	    c = Cross(n=int(options.size))
	    i = 0; 	    
	    a,b=0,0
	    candidatex = None
	    special=[]
	    for trace_count, t in enumerate(c.iterate_trace()):
		for is_cross, candidate, x, y in c.iterate_grid(t):
		    i+=1
		    if is_cross:
		    	print candidate, 'location ', [x,y], 'trace ', candidate.trace(), 'is_cross ', is_cross
			a,b = x,y
			candidatex = candidate
			break
		    if options.verbose:
		    	print candidate, 'location ', [x,y], 'trace ', candidate.trace(), 'is_cross ', is_cross		
		if not candidatex is None:
		   special=special+[d+b+1+(c.n*(a+d)) for d in np.arange(0, candidatex.trace(), 1)]+[(candidatex.trace()-2*d-1)+(d+b+1+(c.n*(a+d))) for d in np.arange(0, candidatex.trace(), 1)]			    

	    print '\n'	    
	    if not candidatex is None:	    	    	    		    		    	
	    	c.prettyprint(special=special)	    	    	    		    
	    print '\ntested %d matricies across %d trace sizes' % (i+1, trace_count)   
