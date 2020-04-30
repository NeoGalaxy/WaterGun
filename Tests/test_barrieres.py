from classes import Grid, Direction
(NORD, SUD, EST, OUEST) = (Direction.NORD, Direction.SUD, Direction.EST, Direction.OUEST)

grille = Grid("../Inputs/Grids/Probs/grid1.grid")
print("Grille : \n", grille.getGrid(),"\n")

print("NORD de chaque case : ")
for i in range(5,-1,-1):
	print([grille.getBarrier(x,i,NORD) for x in range(6)])

print("SUD de chaque case : ")
for i in range(5,-1,-1):
	print([grille.getBarrier(x,i,SUD) for x in range(6)])

print("EST de chaque case : ")
for i in range(5,-1,-1):
	print([grille.getBarrier(x,i,EST) for x in range(6)])

print("OUEST de chaque case : ")
for i in range(5,-1,-1):
	print([grille.getBarrier(x,i,OUEST) for x in range(6)])
