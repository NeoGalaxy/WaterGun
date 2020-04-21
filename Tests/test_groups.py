from classes import Grid, Direction

grille = Grid("../Inputs/Grids/grid1.txt")
print("Grille : \n", grille.getGrid(),"\n")
grille.mkGroups()
print("\n".join(str(x) for x in grille.groups))
