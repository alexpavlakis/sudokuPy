from timeit import default_timer as timer
from sudoku_puzzles import *

# Print a puzzle
def print_sudoku(s):
	v = [v if v != 0 else " " for v in s]
	row_block = "+ - - - + - - - + - - - +"
	for r in range(13):
		if r in [0, 4, 8, 12]: print(row_block)
		else:
			for c in range(13):
				if c in [0, 4, 8]: print("|", end = " "),
				elif c in [12]: print("|")
				else: 
					print(v[0], end = " "),
					v = v[1:len(v)]


# Get options for each
def getCandidates(s):
	out = [[] for i in range(81)]
	for i in range(81):
		if s[i] > 0:
			out[i] = [s[i]]
		else:
			options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
			for j in range(20):
				if s[peers[i][j]] > 0:
					if s[peers[i][j]] in options:
						options.remove(s[peers[i][j]])
			out[i] = options
	return out

# Get lengths. 
def getLengths(candidates, s): return [len(candidates[i]) for i in range(81) if s[i] == 0]

# Get empties
def getEmpties(s): return [i for i in range(81) if s[i] == 0]

# Sort empties by length
def sortEmpties(empties, lengths): return [x for _,x in sorted(zip(lengths, empties))]


def solveBacktracking(s, empties, candidates):
	if len(empties) == 0: return True
	index = empties[0]
	n_cand = len(candidates[index])
	if n_cand > 1:
		for e in empties[1:]:
			if len(candidates[e]) < n_cand:
				n_cand = len(candidates[e])
				index = e
				if n_cand == 1: break
	options = candidates[index]
	legal = True
	for o in options:
		to_update = []
		for p in peers[index]:
			if o in candidates[p]:
				if len(candidates[p]) == 1:
					legal = False
					break
				candidates[p].remove(o)
				to_update.append(p)
		if legal:
			s[index] = o
			empties.remove(index)
			if solveBacktracking(s, empties, candidates):
				return True
			# Backtrack
			s[index] = 0
			empties.append(index)
		for p in to_update:
			candidates[p].append(o)
		legal = True
	return False


def solveSudoku(s):
	candidates = getCandidates(s)
	lengths = getLengths(candidates, s)
	empties = getEmpties(s)
	empties = sortEmpties(empties, lengths)
	solveBacktracking(s, empties, candidates)
	return s

# Execute
if __name__ == "__main__":

	# Solve an easy puzzle
	print("\n easy sudoku")
	print_sudoku(easy_sudoku)
	start = timer()
	solveSudoku(easy_sudoku)
	end = timer()
	print_sudoku(easy_sudoku)
	print("time to complete (seconds):")
	print(round(end - start, 4))

	# Solve a hard puzzle
	print("\n hard sudoku")
	print_sudoku(hard_sudoku)
	start = timer()
	solveSudoku(hard_sudoku)
	end = timer()
	print_sudoku(hard_sudoku)
	print("time to complete (seconds):")
	print(round(end - start, 4))

	# Solve a very hard puzzle
	print("\n evil sudoku")
	print_sudoku(evil_sudoku)
	start = timer()
	solveSudoku(evil_sudoku)
	end = timer()
	print_sudoku(evil_sudoku)
	print("time to complete (seconds):")
	print(round(end - start, 4))
