from classes import Grid

grille = Grid("../Inputs/Grids/Probs/grid1x2_multiple_answer.grid")
print("Grille : \n"+grille.getGrid(),"\n")
print("\nSingle solution :")
print(grille.getSolution())
print("\nAll solutions :")
print("\n".join(str(s) for s in grille.getAllSolutions()))
print("\nAll solutions by getNextSolution :")
s = ""
while s != None: # I miss do...while loops, why aren't they in python...?
	s = grille.getNextSolution()
	print(s)

print("\nAll solutions using next :")
try:
	while True:
		s = next(grille)
		print(s)
except Exception as e:
	print("-> Ended")

print("\nAll solutions by for loop :")
for s in (grille):
	print(s)


