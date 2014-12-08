#!/usr/bin/env python
#coding:utf-8
# Author: Ramzi Abdoch

from collections import deque
import operator

ROW = "ABCDEFGHI";
COL = "123456789";

# Reading of sudoku list from file
try:
    f = open("sudokus.txt", "r")
    sudokuList = f.read()
except:
	print "Error in reading the sudoku file."
	exit()

#######################
## Utility Functions ##
#######################

# Print each sudoku
def printSudoku(sudoku):
	print "-----------------"
	for i in ROW:
		for j in COL:
			print sudoku[i + j],
		print ""	

def get_neighbors(loc):
	neighbors = set()

	# add row neighbors
	for col in COL.replace(loc[1],""):
		neighbors.add(loc[0] + col) 

	# add column neighbors
	for row in ROW.replace(loc[0], ""):
		neighbors.add(row + loc[1])

	# add box neighbors
	box = list()
	centroid = [None, None]

	def mod3(x):
		return x % 3

	# find centroid of the box
	offset = [int(ROW.index(loc[0])), int(loc[1])]
	mod_offset = map(mod3, offset)

	# Row
	if mod_offset[0] == 0:
		centroid[0] = offset[0] + 1
	elif mod_offset[0] == 1:
		centroid[0] = offset[0]
	elif mod_offset[0] == 2:
		centroid[0] = offset[0] - 1
	
	# Column
	if mod_offset[1] == 1:
		centroid[1] = offset[1] + 1
	elif mod_offset[1] == 2:
		centroid[1] = offset[1]
	elif mod_offset[1] == 0:
		centroid[1] = offset[1] - 1

	# Get all squares in box
	for i in range(centroid[0] - 1, centroid[0] + 2):
		for j in range(centroid[1] - 2, centroid[1] + 1):
			if [i,j+1] != offset:
 				neighbors.add(ROW[i] + COL[j])

	return neighbors

#########
## AC3 ##
#########

# AC3 Algorithm (pg. 146 - Russell, Norvig)
def ac3(sudoku):
	queue = deque()
	domain = {}

	# Check if sudoku is solved
	def solved(sudoku):
		solved = True
		for i in ROW:
			for j in COL:
				if sudoku[i + j] == 0:
					solved = False
		return solved

	# Add arcs to queue
	def build_arcs(queue, sudoku):
		for i in ROW:
			for j in COL:
				for neighbor in get_neighbors(i + j):
					queue.append([i+j, neighbor])

	# Setup domains
	for i in ROW:
		for j in COL:
			if sudoku[i + j] == 0:
				domain[i+j] = range(1,10)
			else:
				domain[i+j] = [sudoku[i+j]]

	# Setup Arcs
	build_arcs(queue, sudoku)

	# Remove inconsistent values
	def rem_inc_vals(arc):
		removed = False

		for x in domain[arc[0]]:
			# If x is only variable in constraint's domain, remove x
			if len(domain[arc[1]]) == 1 and x in domain[arc[1]]:
				domain[arc[0]].remove(x)
				removed = True
		return removed

	while queue:
		arc = queue.popleft()
		if rem_inc_vals(arc):
			for loc in get_neighbors(arc[0]):
				queue.append([loc, arc[0]])

	# Assign values from created domains
	for i in ROW:
		for j in COL:
			#print domain[i+j], len(domain[i+j])
			if len(domain[i+j]) == 1:
				sudoku[i+j] = domain[i+j][0]
			else:
				sudoku[i+j] = 0

	return sudoku

# 1.5 count number of sudokus solved by AC-3
# num_ac3_solved = 0

# for line in sudokuList.split("\n"):
# 	# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
# 	sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}

# 	# write your AC3 algorithms here, update num_ac3_solved	
# 	sudoku = ac3(sudoku)

# 	# Update num_ac3_solved
# 	if(solved(sudoku)):
# 		num_ac3_solved += 1;

# print num_ac3_solved

#########################
## Backtracking Search ##
#########################

# Backtracking Search Algorithm (pg. 142; Russell, Norvig)
def bt_search(sudoku):

	## Helper Functions ##

	# Check if assignment is complete
	def complete(assignment):
		complete = True
		for var in get_vars(sudoku):
			if var not in assignment:
				complete = False
		return complete

	# Get variables of sudoku
	def get_vars(sudoku):
		variables = []
		for i in ROW:
			for j in COL:
				if sudoku[i+j] == 0:
					variables.append(i+j)
		return variables

	def build_constraints(sudoku):
		results = {}

		# Iterate through whole puzzle
		for i in ROW:
			for j in COL:
				# Find neighbors
				neighbors = get_neighbors(i+j)
				results[i+j] = []

				# Iterate through neighbors to find assigned values, add as constraint
				for nbr in neighbors:
					if sudoku[nbr] != 0 and sudoku[nbr] not in results[i+j]:
						results[i+j].append(sudoku[nbr])

		return results

	# Select Unassigned Variable
	# Use MRV (minimum remaining values) heuristic
	def sel_ua_var(variables, assignment, sudoku):
		
		# Find all unassigned vars
		ua_vars = [v for v in variables if len(values[v]) > 1]

		# Compare number of remaining values
		def cmp_num_vars(x, y):
			return len(values[x]) - len(values[y])

		results = sorted(ua_vars, cmp=cmp_num_vars)
		#print results

		# Naïve selection of results, could choose better
		return results[0]

	# Order Domain Values based on LCV (least constraining value) heuristic
	def order_dom_vals(var, assignment, sudoku):

		# Count domain reductions for each val
		counts = []

		for val in values[var]:

			count = 0
			neighbors = get_neighbors(var)

			for nbr in neighbors:
				if val in values[nbr]:
					count += 1

			counts.append([val,count]) 

		# Order them by value
		srtd_cts = sorted(counts, key=operator.itemgetter(1))

		ordered_vals = []
		for ct in srtd_cts:
			ordered_vals.append(ct[0])

		return ordered_vals

	# Forward Checking
	def chk_fwd(var, val):
		# Get neighbors
		neighbors = get_neighbors(var)

		# Iterate through neighbors and remove selected val
		for nbr in neighbors:
			if val in values[nbr]:
				values[nbr].remove(val)

	# Check if val is consistent for var
	def consistent(var, val):
		return val not in constraints[var]

	# Recursively call algo
	def recursive_bt(assignment, sudoku):
		if complete(assignment): return assignment

		var = sel_ua_var(get_vars(sudoku), assignment, sudoku)

		for val in order_dom_vals(var, assignment, sudoku):
			if consistent(var, val):
				assignment[var] = val
				chk_fwd(var, val)
				result = recursive_bt(assignment, sudoku)
				if result != "failure":
					return result
				assignment.pop(var, None)
			return "failure"

	## Execute bt_search ##

	# Initialize
	values = {}
	constraints = {}

	# Setup possible values for all variables
	for var in get_vars(sudoku):
		values[var] = range(1,10)

	# Assign values for given squares
	for i in ROW:
		for j in COL:
			if sudoku[i+j] != 0:
				values[i+j] = [sudoku[i+j]]

	# Build constraints
	# constraint[i] = [1-9] disallowed numbers
	constraints = build_constraints(sudoku)

	return recursive_bt({}, sudoku)

# 1.6 solve all sudokus by backtracking
for line in sudokuList.split("\n"):
	# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
	sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}

	solution = bt_search(sudoku)

	print solution
