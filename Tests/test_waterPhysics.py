from classes import Grid

grille = Grid("../Grids/Probs/example.grid")
cnf = grille.getWaterPhys()
n = 0
for clause in cnf:
	n += 1
	print(clause, end = ", ")
	if n == 4:
		n = 0
		print()
print()
print(grille.getGrid())
