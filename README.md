# INF432 Project

## Organisation du projet

Dans ce projet, il y a 3 répertoires :  

- [*Classes*](#Classes) qui contient toutes les classes implémentés pour le projet. Notre rendu final pourrait se résumer à ce repertoire, car l'idée serait que le type [`Grid`](#Grid.py) puisse prendre une grille en argument, et donner les solutions de la grille.  

- *Inputs* qui sont un ensemble de grilles que l'on peut utiliser comme entrées à la classe `Grid` (c.f. l'explication de comment [`Grid`](#Grid.py) fonctionne). Les grilles y sont ensuites rangées par syntaxe : pour l'instant il n'y a que la syntaxe **grid**, qui est assez intuitive, mais par la suite, je prévois de créer aussi une syntaxe au format *JSON*, que je vous expliquerais et qui est simple à comprendre.  

- *Tests* qui contient des fichiers python à exécuter pour faire des tests. C'est aussi ici que vous pouvez implémenter des fonctions ou méthodes avant de les mettre au bon endroit, ou pour faire tout et n'importe quoi. En gros, c'est un peu un bac-à-sable. Vous y trouverez `classes.js`, qui permet d'importer directement les différentes classes dans le dossier *Classes* en écrivant juste `import classes`, ou alors `from classes import *`.  


## Classes

Voici les différentes classes présentes dans le projet, un exemple d'utilisation, et comment elles fonctionnent. Les morceaux de codes donnés en exemple fonctionnent dans le dossier *Tests* (car le `import` fonctionne grâce au **classes.py**).

### Grid.py

```python
from classes import Grid

# Prend la grille grid1.txt, et la parse pour créer une variable de type Grid
grille = Grid("../Inputs/Grids/grid1.txt") 

print(grille) # -> "(6x6 grid)"
print("C'est une grille ",grille.l,"par", grille.h) # affiche la largeur et la hauteur de grille
print(grille.get_grid()) # affiche la grille au format grid
```

La classe `Grid` permet de parser une grille. Les attributs qui sont enregistrés dans la classe `Grille` sont :

- les dimensions (L et H)

- deaux tableaux décrivant s'il y a un tableau à chaque intersection de deux cases (pareil que les Bc et Bl dans le rapport)

- deaux tableaux décrivant les valeurs sur les cotés

*Vous n'êtes pas obligés de savoir comment ils y sont conservés exactement, et je vais m'arranger pour que ce soit impossible de le modifier de l'exterieur. Mais n'hésitez pas à me demander d'ajouter un moyer de lire directement ces valeurs, et par quelle manière ça vous arrangerait.*

#### Méthodes

**Constructeur** : Le constructeur `Grid()` prend en argument un nom de fichier au format grid et en fait une grille. **/!\\** pour l'instant, `Grid` ne peut lire les grilles dont les valeurs sont supérieures à 10.

**get_grid** : La méthode `get_grid` renvoie un string au format *grid* représentant la grille. **/!\\** la méthode `get_grid` a une sortie indéfinie dans le cas où les valeurs sont supérieures à 10.

**mkGroups** : *Non implémenté -* Lance le regroupement des cases par groupe, afin de reconnaître les formes de la grille

### CNF.py
```python
from classes import CNF

print(CNF(("x","y","z"),("-x","-y","z")))
# -> CNF{Cl['x', 'y', 'z'], Cl['-x', '-y', 'z']}

print(CNF((1,2,3),(-1,-2,3)))
# -> CNF{Cl['x', 'y', 'z'], Cl['-x', '-y', 'z']}

from classes import Clause

print(Clause("x","-y","z"))
# -> Cl['x', '-y', 'z']

print(CNF(Clause("x","-y","z"), Clause("-x","y")))
# -> CNF{Cl['x', '-y', 'z'], Cl['-x', 'y']}

```

La classe (i.e. le type) `CNF` permet de créer un *conjunctive normal form*, qui est équivalent à une liste de clauses. J'ai alors défini le type `Clause`, qui est une liste de litteraux. Tout cela est défini dans *Classes/CNF.py*.

### La classe `Clause`

Pour utiliser la classe `Clause`, il faut l'importer des classes. 
```python
from Classes import Clause
```
Ensuite, il faut 
