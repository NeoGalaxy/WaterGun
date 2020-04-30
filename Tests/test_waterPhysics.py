from classes import Grid

grille = Grid("../Inputs/Grids/Probs/grid1.grid").mkGroups()
cnf = grille.getWaterPhys()
n = 0
for clause in cnf.c:
	n += 1
	print(clause, end = ", ")
	if n == 4:
		n = 0
		print()
print()
print(grille.getGrid())
