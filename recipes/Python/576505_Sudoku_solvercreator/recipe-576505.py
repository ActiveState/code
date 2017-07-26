#!/usr/bin/python

# TODO: Make solve function faster!!! Have it check for singles, doubles,
# triples, and quads both naked and hidden

from random import random

def rand(lst):
	"returns a random element in list or integer"
	if type(lst)==type([]):
		return lst[int(random()*len(lst))]
	elif type(lst)==type(0):
		return int(random()*lst)
	else:
		raise Exception,"don't know what do do with type %s!!!"%type(lst)

def reorder(lst):
	"reorders a list to a random order"
	ret=[]
	for item in lst:
		ret.insert(rand(len(ret)),item)
	return ret

def row(row,puzzle):
	return puzzle[row*9:row*9+9]

def col(col,puzzle):
	ret=[]
	for i in range(9):
		ret.append(row(i,puzzle)[col])
	return ret

def box(box,puzzle):
	x=box%3
	if box<3:
		y=0
	elif box<6:
		y=1
	else:
		y=2
	ret=[]
	for i in range(3):
		ret.extend(row(y*3+i,puzzle)[x*3:x*3+3])
	return ret

def remaining(wcb):
	ret=[]
	for i in range(1,10):
		if not i in wcb:
			ret.append(i)
	return reorder(ret) # does not significantly slow program
						# and allows for generation of random puzzles

def coordToBox(x,y):
	box=0
	if x<3:
		pass
	elif x<6:
		box+=1
	else:
		box+=2
	if y<3:
		pass
	elif y<6:
		box+=3
	else:
		box+=6
	return box

def coordToLinear(x,y):
	return y*9+x

def linearToCoord(index):
	y=8
	for i in range(9):
		if index<i*9:
			y-=1
	x=index%9
	return x,y

def possible(x,y,puzzle):
	if not puzzle[coordToLinear(x,y)]==0:
		return [puzzle[coordToLinear(x,y)]]
	imp=[]
	imp.extend(row(y,puzzle))
	imp.extend(col(x,puzzle))
	imp.extend(box(coordToBox(x,y),puzzle))
	return remaining(imp)

def printPuzzle(puzzle):
	string=((((("%s "*3)+"| ")*2+("%s "*3)+"\n")*3+"------|-------|------\n")*3)[:-22]+"\n"
	text=(string%tuple(puzzle)).replace("0","_")
	print text,
	return text

def check(x,y,puzzle):
	for i in range(9):
		if not i==y and len(possible(x,i,puzzle))==0:
			return False
		if not i==x and len(possible(i,y,puzzle))==0:
			return False
	box_x,box_y=linearToCoord(coordToBox(x,y))
	for i in range(box_x,box_x+3):
		if i==x:
			break
		for j in range(box_y,box_y+3):
			if j==y:
				break
			if len(possible(i,j,puzzle))==0:
				return False
	return True

def solve(puzzle,start=0): # TODO: Make this function faster!!!
	if start==81:
		return [puzzle[:]]
	ret=[]
	x,y=linearToCoord(start)
	possibilities=possible(x,y,puzzle)
	if len(possibilities)==0:
		return
	for possibility in possibilities:
		p=puzzle[:]
		p[coordToLinear(x,y)]=possibility
		x,y=linearToCoord(start)
		if not check(x,y,puzzle):
			continue
		solved=solve(p,start+1)
		if solved:
			ret.extend(solved)
			if 1<len(ret): # there is more than one puzzle
				return ret # enough already!!!
	return ret

def solve_no_check_for_dups(puzzle,start=0):
	"This solver function does not check for multiple solutions."
	if start==81:
		return puzzle[:]
	x,y=linearToCoord(start)
	possibilities=possible(x,y,puzzle)
	if len(possibilities)==0:
		return
	for possibility in possibilities:
		p=puzzle[:]
		p[coordToLinear(x,y)]=possibility
		x,y=linearToCoord(start)
		if not check(x,y,puzzle):
			continue
		solved=solve_no_check_for_dups(p,start+1)
		if solved:
			return solved
	return []

def generate(sym=True,goodness=0): # goodness=0 means evil
	if sym:
		RANGE=41
	else:
		RANGE=81
	puzzle=[0]*81
	soln=solve_no_check_for_dups(puzzle)
	puzzle=soln[:]
	spaces=range(RANGE)
	for i in range(RANGE-goodness):
		space=spaces.pop(rand(len(spaces)))
		puzzle[space]=0
		if sym:
			puzzle[80-space]=0
		if 1<len(solve(puzzle)):
			puzzle[space]=soln[space]
			if sym:
				puzzle[80-space]=soln[80-space]
	return puzzle

#puzzle=[]
#for i in range(9):
#	puzzle.extend(map(int,raw_input().split()))

try:
	import psyco
	psyco.full()
except ImportError:
	print "You do not have psyco installed. The program will run slower."

if __name__=="__main__":
	#puzzle=generate()
	#printPuzzle(puzzle)
	#soln=solve(puzzle)
	#printPuzzle(soln[0])
	#if 1<len(soln):
	#	print "More than one solution!!!"
	#puzzle=generate(sym=False)
	#printPuzzle(puzzle)
	#soln=solve(puzzle)
	#printPuzzle(soln[0])
	#if 1<len(soln):
	#	print "More than one solution!!!"
	from time import sleep
	while True:
		puzzle=generate(sym=False)
		text=printPuzzle(puzzle)
		f=open("./sudoku","a")
		f.write(text)
		f.close()
		sleep(180)
