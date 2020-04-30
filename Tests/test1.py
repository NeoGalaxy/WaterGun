from classes import Grid

# Prend la grille grid1.txt, et la parse pour créer une variable de type Grid
grille = Grid("../Inputs/Grids/Probs/grid1.grid") 

print(grille) # -> "(6x6 grid)"
#print("C'est une grille ",grille.l,"par", grille.h) # affiche la largeur et la hauteur de grille
print(grille.getGrid()) # affiche la grille au format grid

from classes import CNF

a = CNF()
print(a)

print(CNF(("x","y","z"),("-x","-y","z")))
# -> CNF{Cl['x', 'y', 'z'], Cl['-x', '-y', 'z']}

print(CNF((1,2,3),(-1,-2,3)))
# -> CNF{Cl['x', 'y', 'z'], Cl['-x', '-y', 'z']}

from classes import Clause

print(Clause("x","-y","z"))
# -> Cl['x', '-y', 'z']

print(CNF(Clause("x","-y","z"), Clause("-x","y")))
# -> CNF{Cl['x', '-y', 'z'], Cl['-x', 'y']}
