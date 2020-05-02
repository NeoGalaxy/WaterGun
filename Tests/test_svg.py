from classes import Grid

grille = Grid("../Inputs/Grids/Probs/example.grid")
s = grille.getSolution()
f = open("../Outputs/test1.svg","w")
f.write(grille.solToSvgs(s))
f.close()

grille = Grid("../Inputs/Grids/Probs/example.grid")
s = grille.getSolution()
f = open("../Outputs/test2.svg","w")
grille.solToSvg(s,f)
f.close()