from classes import Grid, Direction

grille = Grid("../Grids/Probs/grid1.grid")
print("Grille : \n"+grille.getGrid(),"\n")
print("Groupes : \n"+"\n".join(
	", ".join(
		str(grille.getGroup(x,y)) for x in range(grille.l())
	) for y in range(grille.h()-1,-1,-1)
))
