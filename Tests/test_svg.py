from classes import Grid

grille = Grid("../Inputs/Grids/Probs/example.grid")
s = grille.getSolution()
f = open("../Outputs/test1.svg","w")
f.write(grille.writeSvgs(s))
f.close()

grille = Grid("../Inputs/Grids/Probs/example.grid")
s = grille.getSolution()
f = open("../Outputs/test2.svg","w")
grille.writeSvg(f,s)
f.close()