from classes import Grid #assuming you are in /Tests

# Case where the arg is a path
gridN1 = Grid("../Grids/Probs/grid1.grid")
# Case where the arg is a file
with open("../Grids/Probs/example.grid")as f:
	gridN2 = Grid(f)
# Case where the arg is a string
with open("../Grids/Probs/grid4x5N.grid")as f:
	txt = f.read()
	gridN3 = Grid(txt)
# Case where the arg is a list
with open("../Grids/Probs/bigGrid.grid")as f:
	txt = f.read().split("\n")
	gridN4 = Grid(txt)
print("grid number 1 : ")
print(gridN1.getGrid()) # print the grid in grid1 format
print("grid number 2 : ")
print(gridN2.getGrid()) # print the grid in grid1 format
print("grid number 3 : ")
print(gridN3.getGrid()) # print the grid in grid1 format
print("grid number 4 : ")
print(gridN4.getGrid()) # print the grid in grid1 format

from classes import CNF

a = CNF()
print(a)

print(CNF(("x","y","z"),("-x","-y","z")))
# -> CNF{Cl['x', 'y', 'z'], Cl['-x', '-y', 'z']}

print(CNF((1,2,3),(-1,-2,3)))
# -> CNF{Cl['x', 'y', 'z'], Cl['-x', '-y', 'z']}

from classes import Clause

print(Clause("x","-y","z"))
# -> Cl['x', '-y', 'z']

print(CNF(Clause("x","-y","z"), Clause("-x","y")))
# -> CNF{Cl['x', '-y', 'z'], Cl['-x', 'y']}
