import re
import random
import os

# GLOBAL VARIABLES
grid_size = 81

def isFull (grid):
    return grid.count('.') == 0
  
# can be used more purposefully
def getTrialCelli(grid):
  for i in range(grid_size):
    if grid[i] == '.':
      print 'trial cell', i
      return i
      
def isLegal(trialVal, trialCelli, grid):

  cols = 0
  for eachSq in range(9):
    trialSq = [ x+cols for x in range(3) ] + [ x+9+cols for x in range(3) ] + [ x+18+cols for x in range(3) ]
    cols +=3
    if cols in [9, 36]:
      cols +=18
    if trialCelli in trialSq:
      for i in trialSq:
        if grid[i] != '.':
          if trialVal == int(grid[i]):
            print 'SQU',
            return False
  
  for eachRow in range(9):
    trialRow = [ x+(9*eachRow) for x in range (9) ]
    if trialCelli in trialRow:
      for i in trialRow:
        if grid[i] != '.':
          if trialVal == int(grid[i]):
            print 'ROW',
            return False
  
  for eachCol in range(9):
    trialCol = [ (9*x)+eachCol for x in range (9) ]
    if trialCelli in trialCol:
      for i in trialCol:
        if grid[i] != '.':
          if trialVal == int(grid[i]):
            print 'COL',
            return False
  print 'is legal', 'cell',trialCelli, 'set to ', trialVal
  return True

def setCell(trialVal, trialCelli, grid):
  grid[trialCelli] = trialVal
  return grid

def clearCell( trialCelli, grid ):
  grid[trialCelli] = '.'
  print 'clear cell', trialCelli
  return grid


def hasSolution (grid):
  if isFull(grid):
    print '\nSOLVED'
    return True
  else:
    trialCelli = getTrialCelli(grid)
    trialVal = 1
    solution_found = False
    while ( solution_found != True) and (trialVal < 10):
      print 'trial valu',trialVal,
      if isLegal(trialVal, trialCelli, grid):
        grid = setCell(trialVal, trialCelli, grid)
        if hasSolution (grid) == True:
          solution_found = True
          return True
        else:
          clearCell( trialCelli, grid )
      print '++'
      trialVal += 1
  return solution_found

def main ():
  #sampleGrid = ['2', '1', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '3', '1', '.', '.', '.', '.', '9', '4', '.', '.', '.', '.', '7', '8', '2', '5', '.', '.', '4', '.', '.', '.', '.', '.', '.', '6', '.', '.', '.', '.', '.', '1', '.', '.', '.', '.', '8', '2', '.', '.', '.', '7', '.', '.', '9', '.', '.', '.', '.', '.', '.', '.', '.', '3', '1', '.', '4', '.', '.', '.', '.', '.', '.', '.', '3', '8', '.']
  #sampleGrid = ['.', '.', '3', '.', '2', '.', '6', '.', '.', '9', '.', '.', '3', '.', '5', '.', '.', '1', '.', '.', '1', '8', '.', '6', '4', '.', '.', '.', '.', '8', '1', '.', '2', '9', '.', '.', '7', '.', '.', '.', '.', '.', '.', '.', '8', '.', '.', '6', '7', '.', '8', '2', '.', '.', '.', '.', '2', '6', '.', '9', '5', '.', '.', '8', '.', '.', '2', '.', '3', '.', '.', '9', '.', '.', '5', '.', '1', '.', '3', '.', '.']
  sampleGrid = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '4', '6', '2', '9', '5', '1', '8', '1', '9', '6', '3', '5', '8', '2', '7', '4', '4', '7', '3', '8', '9', '2', '6', '5', '1', '6', '8', '.', '.', '3', '1', '.', '4', '.', '.', '.', '.', '.', '.', '.', '3', '8', '.']
  printGrid(sampleGrid, 0)
  if hasSolution (sampleGrid):
    printGrid(sampleGrid, 0)
  else: print 'NO SOLUTION'

  
if __name__ == "__main__":
    main()

def printGrid (grid, add_zeros):
  i = 0
  for val in grid:
    if add_zeros == 1:
      if int(val) < 10: 
        print '0'+str(val),
      else:
        print val,
    else:
        print val,
    i +=1
    if i in [ (x*9)+3 for x in range(81)] +[ (x*9)+6 for x in range(81)] +[ (x*9)+9 for x in range(81)] :
        print '|',
    if add_zeros == 1:
      if i in [ 27, 54, 81]:
        print '\n---------+----------+----------+'
      elif i in [ (x*9) for x in range(81)]:
        print '\n'
    else:
      if i in [ 27, 54, 81]:
        print '\n------+-------+-------+'
      elif i in [ (x*9) for x in range(81)]:
        print '\n'
