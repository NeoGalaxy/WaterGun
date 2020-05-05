from classes import Grid #assuming you are in /Inputs

gridN1 = Grid("../Inputs/Grids/Probs/grid1.grid")
with open("../Inputs/Grids/Probs/example.grid")as f:
	gridN2 = Grid(f)
with open("../Inputs/Grids/Probs/grid4x5N.grid")as f:
	txt = f.read()
	gridN3 = Grid(txt)
print("grid number 1 : ",gridN1) # -> "(6x6 grid)"
print(gridN1.getGrid()) # print the grid in grid1 format
print("grid number 2 : ",gridN2) # -> "(6x6 grid)"
print(gridN2.getGrid()) # print the grid in grid1 format
print("grid number 3 : ",gridN3) # -> "(6x6 grid)"
print(gridN3.getGrid()) # print the grid in grid1 format

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
