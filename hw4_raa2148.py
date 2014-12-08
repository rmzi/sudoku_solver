#!/usr/bin/env python
#coding:utf-8
# Author: Ramzi Abdoch

from collections import deque

ROW = "ABCDEFGHI";
COL = "123456789";

# utility function to print each sudoku
def printSudoku(sudoku):
	print "-----------------"
	for i in ROW:
		for j in COL:
			print sudoku[i + j],
		print ""	

# Reading of sudoku list from file
try:
    f = open("sudokus.txt", "r")
    sudokuList = f.read()
except:
	print "Error in reading the sudoku file."
	exit()

#########
## AC3 ##
#########

def mod3(x):
	return x % 3

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
				#print sorted(get_neighbors(i+j))
				queue.append([i+j, neighbor])

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

# AC3 Algorithm (pg. 146 - Russell, Norvig)
def ac3(sudoku):
	queue = deque()
	domain = {}

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
num_ac3_solved = 0

for line in sudokuList.split("\n"):
	# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
	sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}

	# write your AC3 algorithms here, update num_ac3_solved	
	sudoku = ac3(sudoku)

	# Update num_ac3_solved
	if(solved(sudoku)):
		num_ac3_solved += 1;

print num_ac3_solved

#########################
## Backtracking Search ##
#########################

def bt_search(sudoku):
	variables = list()
	values = {}

	for var in variables:
		values.append()

	# Check if assignment is complete
	def complete(assignment):
		complete = True
		for var in get_vars(sudoku):
			if var not in assignment:
				complete = False
		return complete

	# Select Unassigned Variable
	# Use MRV (minimum remaining values) heuristic
	def sel_var(vars, assignment, sudoku):
		pass

	def recursive_bt(assignment, sudoku):
		if complete(assignment): return assignment

		var = sel_var(get_vars(csp), assignment, sudoku)

		

	return recursive_bt({}, sudoku)

# 1.6 solve all sudokus by backtracking
for line in sudokuList.split("\n"):
	# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
	sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}

	solution = bt_search(sudoku)
