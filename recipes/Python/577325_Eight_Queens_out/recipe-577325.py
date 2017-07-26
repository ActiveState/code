board = {}
def render():
	s = dict([(i, ['-'] * 8) for i in range(8)]) 
	for (x, y) in board.keys():
		s[x][y] = 'Q'
	for line in s.keys():
		print ''.join(s[line])
	
def gen(row):
	if row == 8: 
		render()
		print "\n"
		return
	else:
		for col in range(8):
			if 	row not in [x for (x,y) in board.keys()] and \
				col not in [y for (x,y) in board.keys()] and \
				len([(x,y) for (x,y) in board.keys() if abs(row-x) == abs(col-y)]) == 0:
				board[(row, col)] = 1
				gen(row+1)
				board.__delitem__((row, col))
		

for i in range(8):
	board[(0, i)] = 1
	gen(1)
	board.__delitem__((0, i))
