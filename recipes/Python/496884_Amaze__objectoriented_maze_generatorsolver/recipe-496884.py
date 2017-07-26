"""
Amaze - A completely object-oriented Pythonic maze generator/solver.
This can generate random mazes and solve them. It should be
able to solve any kind of maze and inform you in case a maze is
unsolveable.

This uses a very simple representation of a mze. A maze is
represented as an mxn matrix with each point value being either
0 or 1. Points with value 0 represent paths and those with
value 1 represent blocks. The problem is to find a path from
point A to point B in the matrix.

The matrix is represented internally as a list of lists.

Have fun :-)

"""

import sys
import random
import optparse

class MazeReaderException(Exception):
    pass

class MazeReader(object):
    """ Read a maze from different input sources """

    STDIN = 0
    FILE = 1
    SOCKET = 2

    def __init__(self):
        self.maze_rows = []
        pass

    def readStdin(self):
        """ Read a maze from standard input """

        print 'Enter a maze'
        print 'You can enter a maze row by row'
        print
        
        data = raw_input('Enter the dimension of the maze as Width X Height: ')
        w, h = data.split()
        w, h  = int(w), int(h)
        
        for x in range(h):
            row = ''
            while not row:
                row = raw_input('Enter row number %d: ' % (x+1))
            row = row.split()
            if len(row) != w:
                raise MazeReaderException,'invalid size of maze row'
            self.maze_rows.append(row)

    def readFile(self):
        """ Read a maze from an input file """

        fname = raw_input('Enter maze filename: ')
        try:
            f = open(fname)
            lines = f.readlines()
            f.close()
            # See if this is a valid maze
            lines = [ line for line in lines if line.strip() ]
            w = len(lines[0].split())
            for line in lines:
                row = line.split()
                if len(row) != w:
                    raise MazeReaderException, 'Invalid maze file - error in maze dimensions'
                else:
                    self.maze_rows.append(row)
        except (IOError, OSError), e:
            raise MazeReaderException, str(e)

    def getData(self):
        return self.maze_rows

    def readMaze(self, source=STDIN):
        """ Read a maze from the input source """

        if source==MazeReader.STDIN:
            self.readStdin()
        elif source == MazeReader.FILE:
            self.readFile()

        return self.getData()

class MazeFactory(object):
    """ Factory class for Maze object """

    def makeMaze(self, source=MazeReader.STDIN):
        """ Create a maze and return it. The source is
        read from the 'source' argument """

        reader = MazeReader()
        return Maze(reader.readMaze(source))

    def makeRandomMaze(self, dimension):
        """ Generate a random maze of size dimension x dimension """

        rows = []
        for x in range(dimension):
            row = []
            for y in range(dimension):
                row.append(random.randrange(2))
            random.shuffle(row)
            rows.append(row)

        return Maze(rows)

        
    
class MazeError(Exception):
    """ An exception class for Maze """
    
    pass

class Maze(object):
    """ A class representing a maze """

    def __init__(self, rows=[[]]):
        self._rows = rows
        self.__validate()
        self.__normalize()

    def __str__(self):

        s = '\n'
        for row in self._rows:
            for item in row:
                s = ''.join((s,' ',str(item),' '))
            s = ''.join((s,'\n\n'))

        return s
                
    def __validate(self):
        """ Validate the maze """

        # Get length of first row
        width = len(self._rows[0])
        widths = [len(row) for row in self._rows]
        if widths.count(width) != len(widths):
            raise MazeError, 'Invalid maze!'

        self._height = len(self._rows)
        self._width = width

    def __normalize(self):
        """ Normalize the maze """

        # This converts any number > 0 in the maze to 1
        for x in range(len(self._rows)):
            row = self._rows[x]
            row = map(lambda x: min(int(x), 1), row) 
            self._rows[x] = row

    def getHeight(self):
        """ Return the height of the maze """

        return self._height

    def getWidth(self):
        """ Return the width of the maze """

        return self._width

    def validatePoint(self, pt):
        """ Validate the point pt """

        x,y = pt
        w = self._width
        h = self._height
        
        # Don't support Pythonic negative indices
        if x > w - 1 or x<0:
            raise MazeError, 'x co-ordinate out of range!'

        if y > h - 1 or y<0:
            raise MazeError, 'y co-ordinate out of range!'        

        pass
    
    def getItem(self, x, y):
        """ Return the item at location (x,y) """

        self.validatePoint((x,y))
        
        w = self._width
        h = self._height

        # This is based on origin at bottom-left corner
        # y-axis is reversed w.r.t row arrangement
        # Get row
        row = self._rows[h-y-1]
        return row[x]

    def setItem(self, x, y, value):
        """ Set the value at point (x,y) to 'value' """

        h = self._height
        
        self.validatePoint((x,y))
        row = self._rows[h-y-1]
        row[x] = value
        

    def getNeighBours(self, pt):
        """ Return a list of (x,y) locations of the neighbours
        of point pt """

        self.validatePoint(pt)

        x,y = pt
        
        h = self._height
        w = self._width
        
        # There are eight neighbours for any point
        # inside the maze. However, this becomes 3 at
        # the corners and 5 at the edges
        poss_nbors = (x-1,y),(x-1,y+1),(x,y+1),(x+1,y+1),(x+1,y),(x+1,y-1),(x,y-1),(x-1,y-1)

        nbors = []
        for xx,yy in poss_nbors:
            if (xx>=0 and xx<=w-1) and (yy>=0 and yy<=h-1):
                nbors.append((xx,yy))

        return nbors
        
    def getExitPoints(self, pt):
        """ Return a list of exit points at point pt """

        # Get neighbour list and return if the point value
        # is 0

        exits = []
        for xx,yy in self.getNeighBours(pt):
            if self.getItem(xx,yy)==0:
                exits.append((xx,yy))

        return exits

    def getRandomExitPoint(self, pt):
        """ Return a random exit point at point (x,y) """

        return random.choice(self.getExitPoints(pt))

    def getRandomStartPoint(self):
        """ Return a random point as starting point """

        return random.choice(self.getAllZeroPoints())

    def getRandomEndPoint(self):
        """ Return a random point as ending point """

        return random.choice(self.getAllZeroPoints())

    def getAllZeroPoints(self):
        """ Return a list of all points with
        zero value """
        
        points = []
        for x in range(self._width):
            for y in range(self._height):
                if self.getItem(x,y)==0:
                    points.append((x,y))

        return points
        
    def calcDistance(self, pt1, pt2):
        """ Calculate the distance between two points """

        # The points should be given as (x,y) tuples
        self.validatePoint(pt1)
        self.validatePoint(pt2)        
        
        x1,y1 = pt1
        x2,y2 = pt2

        return pow( (pow((x1-x2), 2) + pow((y1-y2),2)), 0.5)

    def calcXDistance(self, pt1, pt2):
        """ Calculate the X distance between two points """

        # The points should be given as (x,y) tuples
        self.validatePoint(pt1)
        self.validatePoint(pt2)
        
        x1, y1 = pt1
        x2, y2 = pt2

        return abs(x1-x2)

    def calcYDistance(self, pt1, pt2):
        """ Calculate the Y distance between two points """

        # The points should be given as (x,y) tuples
        self.validatePoint(pt1)
        self.validatePoint(pt2)
        
        x1, y1 = pt1
        x2, y2 = pt2

        return abs(y1-y2)

    def calcXYDistance(self, pt1, pt2):
        """ Calculate the X-Y distance between two points """

        # The points should be given as (x,y) tuples
        self.validatePoint(pt1)
        self.validatePoint(pt2)
        
        x1, y1 = pt1
        x2, y2 = pt2

        return abs(y1-y2) + abs(x1-x2)
        
    def getData(self):
        """ Return the maze data """

        return self._rows

class MazeSolver(object):
    """ Maze solver class """
    
    def __init__(self, maze):
        self.maze = maze
        self._start = (0,0)
        self._end = (0,0)
        # Current point
        self._current = (0,0)
        # Solve path
        self._path = []
        # Number of cyclic loops
        self._loops = 0
        # Solvable flag
        self.unsolvable = False        
        # xdiff
        self._xdiff = 0.0
        # ydiff
        self._ydiff = 0.0
        # List keeping cycles (generations)
        self.cycles = []
        # Number of retraces
        self._numretrace = 0
        # Map for exit points
        self._pointmap = {}
        # Number of all zero points
        self._numzeropts = 0
        # Map for retraced points
        self._retracemap = {}
        # Cache for keys of above
        self._retracekeycache = []
        # Number of times retracemap is not updated
        # with a new point
        self._lastupdate = 0
        
    def setStartPoint(self, pt):

        self.maze.validatePoint(pt)
        self._start = pt

    def setEndPoint(self, pt):

        self.maze.validatePoint(pt)
        self._end = pt

    def boundaryCheck(self):
        """ Check boundaries of start and end points """

        exits1 = self.getExitPoints(self._start)
        exits2 = self.getExitPoints(self._end)        

        if len(exits1)==0 or len(exits2)==0:
            return False

        return True

    def setCurrentPoint(self, point):
        """ Set the current point """

        # print 'Current point is',point
        self._current = point
        self._xdiff = abs(self._current[0] - self._end[0])
        self._ydiff = abs(self._current[1] - self._end[1])
        
        self._path.append(point)

    def isSolved(self):
        """ Whether the maze is solved """

        return (self._current == self._end)

    def checkDeadLock(self, point1, point2):

        pt1 = self.getClosestPoint(self.getExitPoints(point1))
        pt2 = self.getClosestPoint(self.getExitPoints(point2))

        if pt1==point2 and pt2==point1:
            return True

        return False

    def getExitPoints(self, point):
        """ Get exit points for 'point' """

        points = self._pointmap.get(point)

        if points==None:
            # We are using shortest-distance algorithm
            points = self.maze.getExitPoints(point)
            self._pointmap[point] = points

        return points
        
    def getNextPoint(self):
        """ Get the next point from the current point """

        points = self.getExitPoints(self._current)
        point = self.getBestPoint(points)
        
        while self.checkClosedLoop(point):

            if self.endlessLoop():
                point = None
                break
            
            # Save point
            point2 = point

            point = self.getNextClosestPointNotInPath(points, point2)
            if not point:
                # Try retracing path
                point = self.retracePath()
                
        return point

    def retracePath(self):

        # Retrace point by point in path, till
        # you get to a point which provides an
        # alternative.
        
        print 'Retracing...'
        path = self._path[:]
        path.reverse()

        self._numretrace += 1
        
        try:
            idx = path[1:].index(self._current)
        except:
            idx = path.index(self._current)            

        pathstack = []
        
        for x in range(idx+1, len(path)):
            p = path[x]
            if p in pathstack: continue

            pathstack.append(p)
            if p != self._path[-1]:
                # print 'Current point is',p
                self._path.append(p)

            if p != self._start:
                points = self.getExitPoints(p)
                point = self.getNextClosestPointNotInPath(points, self.getClosestPoint(points))
                self._retracemap[p] = self._retracemap.get(p, 0) + 1
            else:
                # Add path to cycle
                path = self.sortPointsByXYDistance(self._path[:-1])
                self.cycles.append((path, self._path[:-1]))
                # Reset solver state
                self._path = []
                self._loops = 0
                self._retracemap[p] = self._retracemap.get(p, 0) + 1
                
                return p

    def endlessLoop(self):

        
        if self._retracemap:
            # If the retrace map has not been updated for a while
            # increment lastupdate count
            if self._retracemap.keys() == self._retracekeycache:
                self._lastupdate += 1
            self._retracekeycache = self._retracemap.keys()

        # If lastupdate count reaches the total number of points
        # it could mean we exhausted all possible paths.
        if self._lastupdate > self.maze.getWidth()*self.maze.getHeight():
            print 'Exited because of retracekeycache overflow'
            return True

        # If retrace has gone through all zero points and not
        # yet found a solution, then we are hitting a dead-lock.
        elif len(self._retracemap.keys())> self._numzeropts - 1:
            print 'Exited because number of points exceeded zero points'            
            return True
        else:
            # If the retrace path contains only one point
            if len(self._retracemap.keys())==1:
                val = self._retracemap.get(self._retracemap.keys()[0])
                # If we hit the same point more than the number of
                # zero points in the maze, it signals a dead-lock.
                if val>self._numzeropts:
                    print 'Exited because we are oscillating'                    
                    return True
        
        return False
        
    def checkClosedLoop(self, point):
        """ See if this point is causing a closed loop """

        l = range(0, len(self._path)-1, 2)
        l.reverse()
        
        for x in l:
            if self._path[x] == point:
                self._loops += 1
                # loop = tuple(self._path[x:])
                # print 'Point=>',point, len(self._path)
                return True

        return False
    
    def getBestPoint(self, points):
        """ Get the best point """

        if len(self.cycles)==0:
            # First try min point
            point = self.getClosestPoint(points)
            # Save point
            point2 = point
            # Point for trying alternate
            altpoint = point

            point = self.getNextClosestPointNotInPath(points, point2)
            if not point:
                point = point2
        else:
            allcycles=[]
            map(allcycles.extend, [item[0] for item in self.cycles])
            if self._current==self._start or self._current in allcycles:
                # print 'FOUND IT =>',self._current
                history = []
                for path in [item[1] for item in self.cycles]:
                    path.reverse()
                    try:
                        idx = path.index(self._current)
                        next = path[idx-1]
                        history.append(next)
                    except:
                        pass
                point = self.getDifferentPoint(points, history)
                if not point:
                    point = self.getAlternatePoint(points, history[-1])
            else:
                # Not there 
                point2 = self.getClosestPoint(points)
                point = self.getNextClosestPointNotInPath(points, point2)
                if not point:
                    point = point2
                
            altpoint = point
            
        return point

    def sortPointsByXYDistance(self, points):
        """ Sort list of points by X+Y distance """

        distances = [(self.maze.calcXYDistance(point, self._end), point) for point in points]
        distances.sort()
            
        points2 = [item[1] for item in distances]

        return points2
    
    def sortPointsByDistances(self, points):
        """ Sort points according to distance from end point """

        if self._xdiff>self._ydiff:
            distances = [(self.maze.calcXDistance(point, self._end), point) for point in points]
        elif self._xdiff<self._ydiff:
            distances = [(self.maze.calcYDistance(point, self._end), point) for point in points]
        else:
            distances = [(self.maze.calcXYDistance(point, self._end), point) for point in points]

        distances.sort()
        points2 = [item[1] for item in distances]

        return points2

    def sortPoints(self, points):

        return self.sortPointsByDistances(points)
        
    def getClosestPoint(self, points):
        """ Return the closest point from current
        to the end point from a list of exit points """

        points2 = self.sortPoints(points)
        
        # Min distance point
        closest = points2[0]
        return closest

    def getDifferentPoint(self, points1, points2):
        """ Return a random point in points1 which is not
        in points2 """

        l = [pt for pt in points1 if pt not in points2]
        if l:
            return random.choice(l)

        return None
        
    def getAlternatePoint(self, points, point):
        """ Get alternate point """

        print 'Trying alternate...',self._current, point
        points2 = points[:]

        if point in points2:
            points2.remove(point)
        if points2:
            return random.choice(points2)
        else:
            return point
        
        return None

    def getNextClosestPoint(self, points, point):
        """ After point 'point' get the next closest point
        to the end point from list of points """

        points2 = self.sortPoints(points)
        idx = points2.index(point)

        try:
            return points2[idx+1]
        except:
            return None

    def getNextClosestPointNotInPath(self, points, point):

        point2 = point
        while point2 in self._path:
            point2 = self.getNextClosestPoint(points, point2)
            
        return point2

    def solve(self):
        """ Solve the maze """

        print 'Starting point is', self._start
        print 'Ending point is', self._end        
        
        # First check if both start and end are same
        if self._start == self._end:
            print 'Start/end points are the same. Trivial maze.'
            print [self._start, self._end]
            return None
        
        # Check boundary conditions
        if not self.boundaryCheck():
            print 'Either start/end point are unreachable. Maze cannot be solved.'
            return None

        # Proper maze
        print 'Maze is a proper maze.'

        # Initialize solver
        self.setCurrentPoint(self._start)
        self._numzeropts = len(self.maze.getAllZeroPoints())
        
        self.unsolvable = False

        print 'Solving...'
        while not self.isSolved():
            pt = self.getNextPoint()
            
            if pt:
                self.setCurrentPoint(pt)
            else:
                print 'Dead-lock - maze unsolvable'
                self.unsolvable = True
                break

        if not self.unsolvable:
            print 'Final solution path is',self._path
            print 'Length of path is',len(self._path)
        else:
            print 'Path till deadlock is',self._path
            print 'Length of path is',len(self._path)            

        # if self.cycles:
        #    print 'Path with all cycles is',
        #    l = []
        #    map(l.extend, [item[1] for item in self.cycles])
        #    l.extend(self._path)
        #    print l
            
        self.printResult()

    def printResult(self):
        """ Print the maze showing the path """

        
        for x,y in self._path:
            self.maze.setItem(x,y,'*')

        self.maze.setItem(self._start[0], self._start[1], 'S')
        self.maze.setItem(self._end[0], self._end[1], 'E')        

        if self.unsolvable:
            print 'Maze with final path'
        else:
            print 'Maze with solution path'
            
        print self.maze

        
class MazeGame(object):

    def __init__(self, w=0, h=0):
        self._start = (0,0)
        self._end = (0,0)
        
    def createMaze(self):
        return None

    def getStartEndPoints(self, maze):
        return None
    
    def runGame(self):

        maze = self.createMaze()
        if not maze:
            return None
        
        print maze
        self.getStartEndPoints(maze)
        
        # Dump it to maze.txt
        open('maze.txt','w').write(str(maze))
        
        solver = MazeSolver(maze)

        open ('maze_pts.txt','w').write(str(self._start) + ' ' + str(self._end) + '\n')
        solver.setStartPoint(self._start)
        solver.setEndPoint(self._end)
        solver.solve()

class InteractiveMazeGame(MazeGame):

    def createMaze(self):
        f = MazeFactory()
        return f.makeMaze()

    def getStartEndPoints(self, maze):

        while True:
            try:
                pt1 = raw_input('Enter starting point: ')
                x,y = pt1.split()
                self._start = (int(x), int(y))
                maze.validatePoint(self._start)
                break
            except:
                pass

        while True:
            try:
                pt2 = raw_input('Enter ending point: ')
                x,y = pt2.split()
                self._end = (int(x), int(y))        
                maze.validatePoint(self._end)
                break
            except:
                pass        
        
class FilebasedMazeGame(MazeGame):

    def createMaze(self):
        f = MazeFactory()
        return f.makeMaze(MazeReader.FILE)

    def getStartEndPoints(self, maze):

        filename = raw_input('Enter point filename: ')        
        try:
            line = open(filename).readlines()[0].strip()
            l = line.split(')')
            self._start = eval(l[0].strip() + ')')
            self._end = eval(l[1].strip() + ')')
        except (OSError, IOError, Exception), e:
            print e
            sys.exit(0)
        
class RandomMazeGame(MazeGame):

    def __init__(self, w=0, h=0):
        super(RandomMazeGame, self).__init__(w, h)
        self._dimension = w
        
    def createMaze(self):
        f = MazeFactory()
        return f.makeRandomMaze(self._dimension)    

    def getStartEndPoints(self, maze):

        pt1, pt2 = (0,0), (0,0)
        while pt1 == pt2:
            pt1 = maze.getRandomStartPoint()
            pt2 = maze.getRandomEndPoint()

        self._start = pt1
        self._end = pt2

class RandomMazeGame2(RandomMazeGame):
    """ Random maze game with distant points """

    def getStartEndPoints(self, maze):

        pt1, pt2 = (0,0), (0,0)
        flag = True
        while flag:
            pt1 = maze.getRandomStartPoint()
            pt2 = maze.getRandomEndPoint()
            # Try till points are at least
            # half maze apart
            xdist = maze.calcXDistance(pt1, pt2)
            ydist = maze.calcYDistance(pt1, pt2)            
            if xdist>=float(maze.getWidth())/2.0 or \
               ydist>=float(maze.getHeight())/2.0:
                flag = False
            
        self._start = pt1
        self._end = pt2    

def main():
    
    p = optparse.OptionParser()
    p.add_option('-r','--random',help='Play the random game',
             dest='random',action='store_true',default=False)
    p.add_option('-R','--random2',help='Play the random game with distant points',
             dest='Random',action='store_true',default=False)    
    p.add_option('-f','--file',help='Play the file-based game',
             dest='file',action='store_true',default=False)
    p.add_option('-i','--interactive',help='Play the interactive game',
             dest='interact',action='store_true',default=False)
    p.add_option('-d','--dimension',help='Matrix dimension (required for random games)',
             dest='dimension', metavar="DIMENSION")
             
    options, args = p.parse_args()
    d = options.__dict__

    if d.get('random') or d.get('Random'):
        dim = d.get('dimension')
        if not dim:
            sys.exit('Random games require -d or --dimension option.')
        if d.get('random'):
            game = RandomMazeGame(int(dim))
            game.runGame()
        elif d.get('Random'):
            game = RandomMazeGame2(int(dim))
            game.runGame()
    elif d.get('file'):
        game = FilebasedMazeGame()
        game.runGame()
    elif d.get('interactive'):
        game = InteractiveMazeGame()
        game.runGame()        
        
    
if __name__ == "__main__":
    if len(sys.argv)==1:
        sys.argv.append('-h')
    
    main()



    
