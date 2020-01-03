# A simple program for solving sudoku puzzles in python

# Board metadata
cols = [1, 2, 3, 4, 5, 6, 7, 8, 9, 
		1, 2, 3, 4, 5, 6, 7, 8, 9, 
		1, 2, 3, 4, 5, 6, 7, 8, 9,
		1, 2, 3, 4, 5, 6, 7, 8, 9,
		1, 2, 3, 4, 5, 6, 7, 8, 9,
		1, 2, 3, 4, 5, 6, 7, 8, 9,
		1, 2, 3, 4, 5, 6, 7, 8, 9, 
		1, 2, 3, 4, 5, 6, 7, 8, 9, 
		1, 2, 3, 4, 5, 6, 7, 8, 9]
rows = sorted(cols)
boxs = [1, 1, 1, 4, 4, 4, 7, 7, 7, 
		1, 1, 1, 4, 4, 4, 7, 7, 7, 
		1, 1, 1, 4, 4, 4, 7, 7, 7, 
		2, 2, 2, 5, 5, 5, 8, 8, 8, 
		2, 2, 2, 5, 5, 5, 8, 8, 8, 
		2, 2, 2, 5, 5, 5, 8, 8, 8, 
		3, 3, 3, 6, 6, 6, 9, 9, 9, 
		3, 3, 3, 6, 6, 6, 9, 9, 9, 
		3, 3, 3, 6, 6, 6, 9, 9, 9]

# Indices in the same row, column, or box for each element
ind_list = [[] for l in range(81)]
for i in range(81):
	for j in range(81):
		if i != j:
			if cols[i] == cols[j] or rows[i] == rows[j] or boxs[i] == boxs[j]:
				ind_list[i].append(j)

# Numbers in a sudoku puzzle
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]




# Print a puzzle
def print_sudoku(values):
	v = [v if v != 0 else " " for v in values]
	row_block = "+ - - - + - - - + - - - +"
	for r in range(13):
		if r in [0, 4, 8, 12]: print row_block
		else:
			for c in range(13):
				if c in [0, 4, 8]: print "|",
				elif c in [12]: print "|"
				else: 
					print v[0],
					v = v[1:len(v)]

# Get number of empty elements remaining
def num_empties(s): 
	return(sum([1 for i in range(81) if s[i][0] == 0]))

# Get everything an element can't be
def get_cant_bes(s, element):
	res = [s[i][0] for i in ind_list[element]]
	return(set([r for r in res if r > 0]))

# If an element can only be one number, it's that
def populate_cant_bes(s):
	for i in range(81):
		if s[i][0] == 0:
			cbs = get_cant_bes(s, i)
			if len(cbs) == 8:
				s[i][0] = [n for n in nums if n not in cbs][0]
	return(s)

# If there's a number that can't be anywhere else in (row, col, box), it's that
def populate_exclusive(s, element, dim):
	in_already = [s[i][0] for i in range(81) if s[i][dim] == s[element][dim] and s[i][0] != 0]
	empty_in_dim = 0
	cb_in_dim = []
	flat_list = []
	for i in range(81):
		if s[i][dim] == s[element][dim]:
			if s[i][0] == 0:
				if i != element:
					cb_in_dim.append(get_cant_bes(s, i))
					empty_in_dim += 1
	for sublist in cb_in_dim:
	    for item in sublist:
	        flat_list.append(item)
	for n in range(1, 10):
		if flat_list.count(n) == empty_in_dim:
	 		if n not in in_already:
	 			s[element][0] = n
	return(s)

# Attempt to solve with logic using strategies in previous two functions
def solve_logic(s):
	empty_start, empty_finish = 1, 0
	while(empty_finish != empty_start):
		empty_start = num_empties(s)
		for j in range(1, 4):
			s = populate_cant_bes(s)
			for i in range(81):
				if s[i][0] == 0:
					s = populate_exclusive(s, i, j)
		empty_finish = num_empties(s)
	return(s)

# Solve with backtracking - guaranteed solution if one exists
def solve_backtracking(s, empties):
	if len(empties) == 0:
		return(True)
	empty = empties[0]
	options = [n for n in nums if n not in get_cant_bes(s, empty)]
	for o in options:
		s[empty][0] = o
		if solve_backtracking(s, empties[1:]): return(True)
		else: s[empty][0] = 0
	return(False)

# Full Solver - first try logic, then backtracking
def solve_sudoku(values):
	s = {}
	for i in range(81):
		s[i] = [values[i], rows[i], cols[i], boxs[i]]
	solve_logic(s)
	if num_empties(s) == 0:
		print_sudoku(s[i][0] for i in range(81))
		return(s)
	else:
		empties = [i for i in range(81) if s[i][0] == 0]
		nopts = [(9-len(get_cant_bes(s, i))) for i in empties]
		empties = [x for _,x in sorted(zip(nopts, empties))]
		solve_backtracking(s, empties)
		if num_empties(s) == 0:
			print_sudoku(s[i][0] for i in range(81))
			return(s)
		else: 
			print("no solution found")

# An example puzzle
values = [2, 1, 0, 0, 0, 0, 0, 0, 0, 
		  4, 0, 8, 0, 0, 1, 0, 2, 0, 
	      0, 6, 5, 0, 2, 0, 0, 0, 4, 
		  0, 0, 2, 5, 0, 3, 0, 9, 0, 
		  8, 0, 7, 0, 0, 0, 5, 0, 2, 
		  0, 5, 0, 2, 0, 4, 7, 0, 0, 
		  5, 0, 0, 0, 1, 0, 4, 7, 0, 
		  0, 2, 0, 7, 0, 0, 6, 0, 1, 
		  0, 0, 0, 0, 0, 0, 0, 8, 9]


# Execute
if __name__ == "__main__":
	print("\nan empty sudoku puzzle:")
	print_sudoku(values)
	print("\nsolved!")
	solve_sudoku(values)