# Maze.py
# Last update 20031115-214011

"""
implements class Maze

Three public methods are implemented:
  __init__(rows,cols)
  __str__()
  as_html_table()

Usage:
  maze = Maze( 20, 30 )  # create a maze 20 rows x 30 cols
  print maze             # print out the maze
  print "<html><body>%s</body></html>" % maze.as_html_table() # publish it

To do:
  1. Method find_path() :)
  2. Different algorithms for big mazes (>50x50) or iteration instead of recursion
"""

# Translation to Python (C) 2003 Georgy Pruss

# From http://www.siteexperts.com/tips/functions/ts20/mm.asp
# // Copyright 1999 Rajeev Hariharan. All Rights Reserved.


import random, sys


# Constants -- cell marks
BOTTOMWALL = 0
RIGHTWALL  = 1
VISITED    = 2

NORTH = 0
SOUTH = 1
WEST  = 2
EAST  = 3


class Maze:

  """Creates a maze and formattes it as text or HTML"""


  #*****************************************

  def __init__( self, n_rows, n_cols ):
    """Create a maze with given number of rows and cols.
    The path connects upper left and lower right cells.
    Actually, all cells are connected.
    Can raise 'MemoryError: Stack overflow' for big arguments, e.g. 100,100
    """

    self.n_rows = n_rows
    self.n_cols = n_cols
    self.maze = [None]*n_rows

    # Set up the hedge array - initially all walls intact
    for i in range(n_rows):
      self.maze[i] = [None]*n_cols
      for j in range(n_cols):
        self.maze[i][j] = [True,True,False] # BOTTOMWALL,RIGHTWALL,VISITED

    # Choose a random starting point
    currCol = random.randrange(n_cols)
    currRow = random.randrange(n_rows)

    # The searh can be quite deep
    if n_rows*n_cols > sys.getrecursionlimit():
      sys.setrecursionlimit( n_rows*n_cols+5 )

    # Recursively Remove Walls - Depth First Algorithm
    self._make_path( currRow, currCol )


  #*****************************************

  def _make_path( self, R, C, D=None ):

    maze = self.maze # speed up a bit

    # Knock out wall between this and previous cell
    maze[R][C][VISITED] = True;

    if   D==NORTH: maze[R]  [C]  [BOTTOMWALL] = False
    elif D==SOUTH: maze[R-1][C]  [BOTTOMWALL] = False
    elif D==WEST:  maze[R]  [C]  [RIGHTWALL]  = False
    elif D==EAST:  maze[R]  [C-1][RIGHTWALL]  = False

    # Build legal directions array
    directions = []
    if R>0            : directions.append(NORTH)
    if R<self.n_rows-1: directions.append(SOUTH)
    if C>0            : directions.append(WEST)
    if C<self.n_cols-1: directions.append(EAST)

    # Shuffle the directions array randomly
    dir_len = len(directions)
    for i in range(dir_len):
      j = random.randrange(dir_len)
      directions[i],directions[j] = directions[j],directions[i]

    # Call the function recursively
    for dir in directions:
      if dir==NORTH:
        if not maze[R-1][C][VISITED]:
          self._make_path( R-1,C,NORTH )
      elif dir==SOUTH:
        if not maze[R+1][C][VISITED]:
          self._make_path( R+1,C,SOUTH )
      elif dir==EAST:
        if not maze[R][C+1][VISITED]:
          self._make_path( R,C+1,EAST )
      elif dir==WEST:
        if not maze[R][C-1][VISITED]:
          self._make_path( R,C-1,WEST )
      #else: raise 'bug:you should never reach here'


  #*****************************************

  def __str__(self):
    """Return maze table in ASCII"""

    result = '.' + self.n_cols*'_.'
    result += '\n'

    for i in range(self.n_rows):
      result += '|'

      for j in range(self.n_cols):
        if i==self.n_rows-1 or self.maze[i][j][BOTTOMWALL]:
          result += '_'
        else:
          result += ' '
        if j==self.n_cols-1 or self.maze[i][j][RIGHTWALL]:
          result += '|'
        else:
          result += '.'

      result += '\n'

    return result


  #*****************************************

  def as_html_table(self):
    """Return table"""

    result = "<TABLE ID='TMaze' CELLSPACING=0 CELLPADDING=0>\n"

    for i in range(self.n_rows):
      result += "<TR HEIGHT=25>"

      for j in range(self.n_cols):
        result += "<TD WIDTH=24 style='"
        if i==0:
          result += "BORDER-TOP: 2px black solid;"
        if i==self.n_rows-1 or self.maze[i][j][BOTTOMWALL]:
          result += "BORDER-BOTTOM: 2px black solid;"
        if j==0:
          result += "BORDER-LEFT: 2px black solid;"
        if j==self.n_cols-1 or self.maze[i][j][RIGHTWALL]:
          result += "BORDER-RIGHT: 2px black solid;"
        result += "'>"

        if i==0 and j==0:
          result += 'S' # start
        elif i==self.n_rows-1 and j==self.n_cols-1:
          result += 'E' # end
        else:
          result += "&nbsp;"
        result += "</TD>\n"

      result += "</TR>\n"

    result += "</TABLE>\n"

    return result


#*****************************************

if __name__ == "__main__":

  syntax = ( "Syntax: %s [[-]n_rows [n_cols]]\n\n"
             "If n_cols is missing, it will be the same as n_rows\n"
             "If n_rows is negative, html representation will be generated\n\n"
             "Examples:\n%s 50 39 -- text maze 50 rows by 39 columns\n"
             "%s -40   -- html code of 40 x 40 cell maze"
           )

  # parse arguments if any

  import os.path

  argc = len(sys.argv)
  name = os.path.basename( sys.argv[0] )

  if argc not in (2,3):
    print >>sys.stderr, syntax % (name,name,name)
    sys.exit(1)
  
  elif argc == 2:
    n_rows = n_cols = int(sys.argv[1])

  elif argc == 3:
    n_rows = int(sys.argv[1])
    n_cols = int(sys.argv[2])

  # create and print maze

  try:
    if n_rows > 0:
      print Maze( n_rows, n_cols )
    else:
      maze = Maze( abs(n_rows), abs(n_cols) )
      print maze.as_html_table()
  except MemoryError:
    print "Sorry, n_rows, n_cols were too big"


# EOF
