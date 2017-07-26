'''
Created on 6 June 2012

@author: bakera

Each cell needs to be considered with neighbours

0 0 0 0 0 
0 0 0 0 0
0 0 0 0 0

http://en.wikipedia.org/wiki/Conway's_Game_of_Life

'''

import numpy as np
import time
import sys
from ctypes import *

def check(grid, row,col, countNumberOfAdjoiningCellsActive, verbose=False):
	try:		
		#if verbose:
		#	print 'before row %d, col %d, value %d, count %d' % (row, col, grid[row, col], len(countNumberOfAdjoiningCellsActive)) 
		if (col >= 0) and (row >=0): # protect 
			if grid[row,col] != 0:
				countNumberOfAdjoiningCellsActive.append(grid[row,col])
				if verbose:
					print 'after row %d, col %d, value %d, count %d' % (row, col, grid[row, col], len(countNumberOfAdjoiningCellsActive))
	except :
		pass

def isalive((r,c), (lr,lc), grid, location, verbose= False):
	''' apply rules against the r,c based on the local grid[lr,lc]
	
	Parameters
	------------
	
		all parameters are keyword parameters
		
		(r,c) : interger tuple
			represents the location of the cell in the global matrix
			
		(lr,lc) : integer tuple
			represents the location in the local grid matrix
		
		grid : matrix
			represents the neighbours to analyse
		
		location: string
			either corner, edge, top or body
	
	'''
	
	countNumberOfAdjoiningCellsActive = []
	
	check(grid, lr, lc+1, countNumberOfAdjoiningCellsActive, verbose)
	check(grid, lr, lc-1, countNumberOfAdjoiningCellsActive, verbose )	
	
	check(grid, lr+1, lc, countNumberOfAdjoiningCellsActive, verbose )	
	check(grid, lr+1, lc+1, countNumberOfAdjoiningCellsActive, verbose )	
	check(grid, lr+1, lc-1, countNumberOfAdjoiningCellsActive, verbose )	
		
	
	check(grid, lr-1, lc, countNumberOfAdjoiningCellsActive, verbose )	
	check(grid, lr-1, lc+1, countNumberOfAdjoiningCellsActive, verbose )	
	check(grid, lr-1, lc-1, countNumberOfAdjoiningCellsActive, verbose )		
	
	if verbose:
		if len(countNumberOfAdjoiningCellsActive) != 0:
			print 'value %d, countNumberOfAdjoiningCellsActive %d' % (grid[lr,lc], len(countNumberOfAdjoiningCellsActive))

	isAlive = False
	#Any live cell with fewer than two live neighbours dies, as if caused by under-population.
	#Any live cell with more than three live neighbours dies, as if by overcrowding.
	if grid[lr,lc] == 1 and (len(countNumberOfAdjoiningCellsActive) < 2 
		or len(countNumberOfAdjoiningCellsActive) > 3) : # under or over populated then die out
		isAlive = False
	#Any live cell with two or three live neighbours lives on to the next generation.
	elif grid[lr,lc] == 1 and (len(countNumberOfAdjoiningCellsActive) == 2 or len(countNumberOfAdjoiningCellsActive) == 3): 	
		isAlive = True
	#Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
	elif grid[lr,lc] == 0 and (len(countNumberOfAdjoiningCellsActive) == 3): 
		isAlive = True
		
	return isAlive
	

def iterate_grid(a, (p,q)):    
    ''' generate the next sub matrix from the original matrix
    
    yield the sub matrix back to be consumed

    Parameters
    ----------

        all parameters are keyword parameters

        a : parent matrix
            represents the larger parent matrix

        (p,q): tuple
            represents the dimensions of each sub
            matrix to generate

    Returns
    -------
        
        yields the next sub matrix 

    '''
    row, col = np.shape(a)
    #print row,col
    for (r,c) in ((r,c) for r in np.arange(row-p+2) for c in np.arange(col-q+2)):   	
	 if r ==0 and c == 0: #corner
		yield (r,r+q, c,c+q), (r,c), (0,0), np.matrix(a[r:r+q, c:c+q]), 'corner'   
	 elif r ==0 and c != 0: #top
		yield (r,r+q, c-1,c+q), (r,c), (0,1), np.matrix(a[r:r+q, c-1:c+q]) , 'top'
	 elif r !=0 and c == 0: # edge,
		yield (r-1,r+q, c,c+q), (r,c), (1,0), np.matrix(a[r-1:r+q, c:c+q]) , 'edge'   
	 else: # normal body 
		yield (r-1,r+p, c-1,c+q), (r,c), (1,1), np.matrix(a[r-1:r+p, c-1:c+q])  , 'body'  


def prettyprint(state):
       colours = {1: 'red', 2: 'red', 3: 'red', 4: 'red', 5: 'red', 6: 'red'}
       colour_map = {1: 10, 2: 12, 3: 13, 4: 14, 5: 15, 6: 9, 0:5} # empty cells colour black
       if (not (sys.platform == 'linux2')):windll.Kernel32.GetStdHandle.restype = c_ulong
       if (not (sys.platform == 'linux2')):h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
       for i, row in enumerate(state.flat):
           i = i + 1
    	   color = colour_map[row]		
           if (not (sys.platform == 'linux2')):
               windll.Kernel32.SetConsoleTextAttribute(h, color)
	       
	       r, c = np.shape(state)
	       
               if i == 0:
        			sys.stdout.write("  %d" % (row)) 
               elif (i % 10 == 0) :
        			sys.stdout.write("  %d\n" % (row)) # include 2 spaces for the twissler
        			sys.stdout.flush()
               else:
        			sys.stdout.write("  %d" % (row)) # include 2 spaces for the twissler
                    
       if (not (sys.platform == 'linux2')):windll.Kernel32.SetConsoleTextAttribute(h, 15) # return to white

def test_sharing_array(model, steps=10, verbose=False):

	start = np.loadtxt(model)
	next = np.loadtxt('empty.dat')
	#print start

	for step in np.arange(steps):
		time.sleep(1)
		prettyprint(start)
		for (r1,r2,c1,c2), (r,c), (lr,lc), grid, location in iterate_grid(start, (2,2)): # data is a 2-D array
			# r,c - location in the parent matrix
			# lr, lc - location in the child grid of the cell to evaluate
			#print (r,c), (lr,lc), grid, grid[lr,lc], location
			if isalive((r,c), (lr,lc), grid, location, verbose):
				next[r,c] = 1
			else:
				next[r,c] = 0				
		start = next.copy()	# independent copy of next	
		
	
if __name__ == '__main__':
   
   verboseFlag = False   
   test_sharing_array('glider.dat', 5, verboseFlag)   
  

glider.dat

0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
