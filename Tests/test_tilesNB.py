from classes import Grid

grille = Grid("../Grids/Probs/example.grid")
print(grille.getGrid())
cnf = grille.getTilesNbCNF()
print(cnf)
