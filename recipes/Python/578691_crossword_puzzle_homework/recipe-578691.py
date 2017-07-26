import sys
def read_board(board_filename):
	bd = []
	for line in open(board_filename):
		bd.append(line.strip())
	return bd

def print_board(board):
	for i in range(0,len(board)):
		for j in range(0,len(board[i])):
			sys.stdout.write(board[i][j])
			sys.stdout.write(' ')
		print
		
	# This function should take in a list of strings and print the board
def word_going_right(board,word,row,col):
	i = 0
	f = 0
	v = True
	while v == True:
		if word[i] == board[row][col]:
			f += 1
		if f == len(word):
			v = True
			break
		if word[i] != board[row][col]:
			v = True
			break
		i += 1
		f += 1
		if col >= len(board[0]):
			v = False
			break
	return v
def word_going_left(board,word,row,col):
	i = 0
	f = 0
	v = True
	while v == True:
		if word[i] == board[row][col]:
			f += 1
		if f == len(word):
			v = True
			break
		if word[i] != board[row][col]:
			v = False
			break
		i += 1
		f += 1
		col -= 1
		if col <= 0:
			v = False
			break
	return v
def word_going_up(board,word,row,col):
	i = 0
	f = 0
	v = True
	while v == True:
		if word[i] == board[row][col]:
			f += 1
		if f == len(word):
			v = True
			break
		if word[i] != board[row][col]:
			v = False
			break
		i += 1
		f += 1
		row -= 1
		if row <= 0:
			v = False
			break
	return v
def word_going_down(board,word,row,col):
	i = 0
	f = 0
	v = True
	while v == True:
		if word[i] == board[row][col]:
			f += 1
		if f == len(word):
			v = True
			break
		if word[i] != board[row][col]:
			v = False
			break
		i += 1
		row += 1
		if row >= len(board):
			v = False
			break
	return v

def word_going_downright(board,word,row,col):
	i = 0
	f = 0
	v = True
	while v == True:
		if word[i] == board[row][col]:
			f += 1
		if f == len(word):
			v = True
			break
		if word[i] != board[row][col]:
			v = False
			break
		i += 1
		row += 1
		col += 1
		if row >= len(board) or col >= len(board[0]):
			v = False
			break
	return v
def word_going_downleft(board,word,row,col):
	i = 0
	f = 0
	v = True
	while v == True:
		if word[i] == board[row][col]:
			f += 1
		if f == len(word):
			v = True
			break
		if word[i] != board[row][col]:
			v = False
			break
		i += 1
		row += 1
		col -= 1
		if row >= len(board) or col <= 0:
			v = False
			break
	return v
def word_going_upright(board,word,row,col):
	i = 0
	f = 0
	v = True
	while v == True:
		if word[i] == board[row][col]:
			f += 1
		if f == len(word):
			v = True
			break
		if word[i] != board[row][col]:
			v = False
			break
		i += 1
		f += 1
		row -= 1
		col += 1
		if row <= 0 or col >= len(board[0]):
			v = False
			break
	return v
def word_going_upleft(board,word,row,col):
	i = 0
	f = 0
	v = True
	while v == True:
		if word[i] == board[row][col]:
			f += 1
		if f == len(word):
			v = True
			break
		if word[i] != board[row][col]:
			v = False
			break
		i += 1
		row -= 1
		col -= 1
		if row <= 0 or col <= 0:
			v = False
			break
	return v


def find_word_in_puzzle(board,word):
	value = True
	new_row = 0
	new_col = 0
	direction = ''
	for r in range(0,len(board)):
		for c in range(0,len(board)):
			if word_going_right(board,word,r,c) == True:
				new_row = r
				new_col = c
				direction = 'right'
				value = True
				break
			if word_going_left(board,word,r,c) == True:
				new_row = r
				new_col = c
				direction = 'left'
				value = True
				break
			if word_going_up(board,word,r,c) == True:
				new_row = r
				new_col = c
				direction = 'up'
				value = True
				break
			if word_going_down(board,word,r,c) == True:
				new_row = r
				new_col = c
				direction = 'down'
				value = True
				break
			if word_going_downright(board,word,r,c) == True:
				new_row = r
				new_col = c
				direction = 'down and right'
				value = True
				break
			if word_going_downleft(board,word,r,c) == True:
				new_row = r
				new_col = c
				direction = 'down and left'
				value = True
				break
			if word_going_upright(board,word,r,c) == True:
				new_row = r
				new_col = c
				direction = 'up and right'
				value = True
				print "%s starts at (%d, %d) going %s" % (word,new_row,new_col,direction)
				break
			if word_going_upleft(board,word,r,c) == True:
				new_row = r
				new_col = c
				direction = 'up and left'
				value = True
				break
	if value == True:
		print "%s starts at (%d, %d) going %s" % (word,new_row,new_col,direction)
	if value == False:
		print "%s can't be found" % (word)
		
	# This function shoud call eight functions (one for each direction)
	# An example call:  is_word_going_right(board, word, row, col)
        # See the HW 5 pdf.
	

if __name__ == '__main__':
	board_filename = raw_input("Enter the file containing the board ==> ")
	print board_filename
	print # print an empty line

	# board is a list of strings (a bit simpler than the Sudoku structure)
	board = read_board(board_filename)

	# print the board, you must write this function
	print_board(board)

	print # print an empty line
	words_filename = raw_input("Enter the file containing the words ==> ")
	print words_filename

	print # print an empty line
	for line in open(words_filename):
		word = line.strip()
		find_word_in_puzzle(board, word)
