import re
import sys

def copy_board(board, sets):
    """Return a copy of board setting new squares from 'sets' dictionary."""
    return [[sets.get((r, c), board[r][c]) for c in range(9)] for r in range(9)]
            
def get_alternatives_for_square(board, nrow, ncolumn):
    """Return sequence of valid digits for square (nrow, ncolumn) in board."""
    def _box(idx, size=3):
        """Return indexes to cover a box (3x3 sub-matrix of a board)."""
        start = (idx // size) * size
        return range(start, start + size)
    nums_in_box = [board[r][c] for r in _box(nrow) for c in _box(ncolumn)]
    nums_in_row = [board[nrow][c] for c in range(9)]
    nums_in_column = [board[r][ncolumn] for r in range(9)]
    nums = nums_in_box + nums_in_row + nums_in_column
    return sorted(set(range(1, 9+1)) - set(nums)) 

def get_more_constrained_square(board):
    """Get the square in board with more constrains (less alternatives)."""
    ranges = ((x, y) for x in range(9) for y in range(9))
    constrains = [(len(get_alternatives_for_square(board, r, c)), (r, c)) 
        for (r, c) in ranges if not board[r][c]]
    if constrains:
        return min(constrains)[1]
     
def solve(board):
    """Return a solved Sudoku board (None if no solution was found)."""
    pos = get_more_constrained_square(board)
    if not pos:
        return board # all squares are filled, so this board is the solution
    nrow, ncolumn = pos
    for test_digit in get_alternatives_for_square(board, nrow, ncolumn):
        test_board = copy_board(board, {(nrow, ncolumn): test_digit})
        solved_board = solve(test_board)
        if solved_board:
            return solved_board

def lines2board(lines):
    """Parse a text board stripping spaces and setting 0's for empty squares."""
    spaces = re.compile("\s+")
    return [[(int(c) if c in "123456789" else 0) for c in spaces.sub("", line)]
            for line in lines if line.strip()]

def main(args):
    """Solve a Sudoku board read from a text file."""
    from pprint import pprint
    path, = args
    board = lines2board(open(path))
    pprint(board)
    pprint(solve(board))
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
