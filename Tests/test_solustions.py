from classes import Grid

grille = Grid("../Inputs/Grids/Probs/example.grid")
print("Grille : \n"+grille.getGrid(),"\n")
print("\nSolutions : \n")
print("\n".join(str(s) for s in grille.getAllSolutions()))
