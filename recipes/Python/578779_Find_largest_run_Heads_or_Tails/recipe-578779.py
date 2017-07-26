'''
Created on 3 Dec 2013

@author: bakera
'''
import unittest
import random
import numpy as np
from ctypes import *
import sys

if ((sys.platform == 'linux2')):
    from termcolor import colored, cprint

class Line(object):
    """
        class represents a line or stream of Heads or Tails that we want to search.
        e.g. H H T T H H H
        
        from line import Line
        Line(verbose=True, width=60).search(n=100, tolerance=5)
        
        
    """
    
    
    def __init__(self, n=5, verbose=False, tolerance=1, width=60):
        """
            n : int
                length of the line to create
            
            verbose : bool
                determine whether you want to see all the machinery output to the console, default False
                
            tolerance : int
                how many H or T flips can you allow in your run, default 1 as in original problem
                however, seems fast at multiples. could be a benefit in this method.
            
        
        """
        self.n = n
        self.verbose = verbose
        self.screen_width = width
        self.tolerance = tolerance
        self.__generate()
        self.toss_map = {1:'H', 0:'T'}
        # some output machinery
        if (not (sys.platform == 'linux2')):windll.Kernel32.GetStdHandle.restype = c_ulong
        if (not (sys.platform == 'linux2')):self.h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))    
        # something for nice look
        self.colour_map = {1: 12, 2: 12, 3: 13, 4: 14, 5: 15, 6: 9, 0:4} # empty cells colour black

    @property
    def is_verbose(self):
        return self.verbose
    
    def prettyprintparam(self, start, end):
        """
            start : int
                location of the start of the match array entry in the self.line array
                
            end : int
                location of the end of the match array, relative tothe self.line array
            
            returns : none
            
            some way to nicely format the output, since we are on a dos command line
            let's not get too fancy and just colour the H and T
        """
        for i, row in enumerate(self.line.flat):
            i = i + 1
            color = self.colour_map[row]        
            if (not (sys.platform == 'linux2')):
                windll.Kernel32.SetConsoleTextAttribute(self.h, color)
                if i == 0:
                    sys.stdout.write("\n%s"%(self.toss_map[row]))
                elif (i % self.screen_width == 0) :
                    if (i >= start+1 and i <= (start+end)):
                        # 13 purple, also nice, green 2 default
                        windll.Kernel32.SetConsoleTextAttribute(self.h, 2)
                        sys.stdout.write(" %s\n"%(self.toss_map[row]))
                        windll.Kernel32.SetConsoleTextAttribute(self.h, color)
                    else:
                        sys.stdout.write(" %s\n"%(self.toss_map[row])) 
                        sys.stdout.flush()
                elif (i >= start+1 and i <= (start+end)):
                    # 13 purple, also nice, green 2 default
                    windll.Kernel32.SetConsoleTextAttribute(self.h, 2)
                    sys.stdout.write(" %s"%(self.toss_map[row]))
                    windll.Kernel32.SetConsoleTextAttribute(self.h, color)
                else:
                    sys.stdout.write(" %s"%(self.toss_map[row]))
                    
        if (not (sys.platform == 'linux2')):windll.Kernel32.SetConsoleTextAttribute(self.h, 15) # return to white        
    
    def check_with_tolerance(self, n, h,t, tolerance):
        '''
            n : int
                offset position, relative to the start of the self.line array
            
            h : obejct numpy.array
                array object populated with an array that we are trying to match, represents head version
                
            t : obejct numpy.array
                array object populated with an array that we are trying to match, represents tail version
                
            tolerance : int
                controls how many flips we can tolerate in the search
            
            for heads arrays match based on sum(h) from line = sum(h)
        '''
        if not len(self.line) > 0:
            return [True, 1, h]
        for offset in np.arange(0,len(self.line),1):
            if self.verbose:
                print 'offset', offset, 'n', n, 'offset+n', offset+n, 'self.line[offset:offset+n]', self.line[offset:offset+n]
            if self.line[offset:offset+n].shape[0] >= h.shape[0] and \
                    self.line[offset:offset+n].shape[0] >= t.shape[0]:
                spread = np.abs(np.sum(self.line[offset:offset+n]) - np.sum(h))
                if spread <= tolerance:
                    return [True, offset, h]
        return [False, 0, None]

    def __generate(self):
        """
            build me a random line, size self.n, of H and T. H ==1, T ==0
        """
        self.line = np.reshape(np.array([random.randint(0,1) for a in np.arange(0,self.n,1)]), (self.n))
            
    def search(self, n=5, tolerance=1):
        """
            n : int
                specify the size of the line, before generating and iterating line
        
        """
        self.n = n
        self.tolerance = tolerance
        self.__generate()
        self.__iterate_line()
        sys.stdout.write(" \n") 
        sys.stdout.flush()

    def __iterate_line(self):
        """
            basic idea is that we generate progressively smaller h and t arrays
            and try and match these to the test line, based on match properties
            complexity of this might appear O(n^2) however in practice the number
            of checks is very small
            
        """
        
        if self.n == 0 or self.n == 1:
            if self.is_verbose: 
                print '*********enter line size >= 1, and not 0.'
            return
        # start with same size and iterate down in size.
        # seems unlikely that we will match from start, but possible for smaller run lengths.
        for y in np.arange(self.n, 0, -1):
                #value = self.check(y, np.array([1 for a in np.arange(0,y,1)]), t = np.array([0 for a in np.arange(0,y,1)]))
                value = self.check_with_tolerance(y, \
                np.array([1 for a in np.arange(0,y,1)]), \
                np.array([0 for a in np.arange(0,y,1)]), self.tolerance)
                if value[0]:
                    self.prettyprintparam(value[1],value[2].shape[0])
                    break
        
class Test(unittest.TestCase):
    """
        simple test class
    """
    
    def testLineTolerance(self):
        """
            idea here is that the 
        """
        b = Line(verbose=False, tolerance=2)
        b.search(n=75)

    def testLineSimple(self):
        b = Line()
        b.search(n=48)

    def testLineCorner(self):
        b = Line()
        b.search(n=1)
        c = Line()
        c.search(n=0)

    def testLarge(self):
        # setup some parameters
        max_iteration = 1000
        min_line_size = 10
        max_line_size = 100
        min_tolerance = 1
        max_tolerance = 25
        [Line(tolerance=random.randint(min_tolerance,max_tolerance)).search(n=random.randint(min_line_size,max_line_size)) for x in np.arange(0,max_iteration,1)]
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBuildCross']
    unittest.main()
