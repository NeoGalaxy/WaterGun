# INF432 Project

## Issues

- **Discussions**  
[#8](https://github.com/NeoGalaxy/INF432/issues/8) Créer et modifier les formats d'entrée pour la classe Grid  

- **Ajout de fonctionnalités utiles**  
[#8](https://github.com/NeoGalaxy/INF432/issues/8) Créer et modifier les formats d'entrée pour la classe Grid  
[#10](https://github.com/NeoGalaxy/INF432/issues/10) Faire un outil de génération de grille automatique  
[#11](https://github.com/NeoGalaxy/INF432/issues/11) Faire un outil ou une fonction de vérification de solution  

## Organisation du projet

Dans ce projet, il y a 3 répertoires :  

- [*Classes*](#Classes) qui contient toutes les classes implémentés pour le projet. Notre rendu final pourrait se résumer à ce repertoire, car l'idée serait que le type [`Grid`](#Gridpy) puisse prendre une grille, dans l'un des [formats prévus](#inputs), en argument, et donner les solutions de la grille.  

- [*Inputs*](#Inputs) qui sont un ensemble de grilles que l'on peut utiliser comme entrées à la classe [`Grid`](#Gridpy). Les grilles y sont ensuites rangées par syntaxe : pour l'instant il n'y a que la syntaxe **[grid](#format-grid1)**, qui est assez intuitive, mais par la suite, je prévois de créer aussi une syntaxe au format *JSON*.  

- [*Tests*](#Tests) qui contient des fichiers python à exécuter pour faire des tests. C'est aussi ici que vous pouvez implémenter des fonctions ou méthodes avant de les mettre au bon endroit, ou pour faire tout et n'importe quoi. En gros, c'est un peu un bac-à-sable. Vous y trouverez [`classes.py`](https://github.com/NeoGalaxy/INF432/blob/master/Tests/classes.py), qui permet d'importer directement les différentes classes dans le dossier [*Classes*](https://github.com/NeoGalaxy/INF432/tree/master/Classes) en écrivant juste `import classes`, ou alors `from classes import *`.  


## Classes

Voici les différentes classes présentes dans le projet, un exemple d'utilisation, et comment elles fonctionnent. Les morceaux de codes donnés en exemple fonctionnent dans le dossier *Tests* (car le `import` fonctionne grâce au [`classes.py`](https://github.com/NeoGalaxy/INF432/blob/master/Tests/classes.py)).

### [Grid.py](https://github.com/NeoGalaxy/INF432/blob/master/Classes/Grid.py)

```python
from classes import Grid

# Prend la grille grid1.txt, et la parse pour créer une variable de type Grid
grille = Grid("../Inputs/Grids/grid1.txt") 

print(grille) # -> "(6x6 grid)"
print("C'est une grille ",grille.l,"par", grille.h) # affiche la largeur et la hauteur de grille
print(grille.get_grid()) # affiche la grille au format grid
```

La classe `Grid` permet de parser une grille. Les attributs qui sont enregistrés dans la classe `Grid` sont :

- les dimensions (L et H)

- deux tableaux décrivant s'il y a un tableau à chaque intersection de deux cases (pareil que les Bc et Bl dans le rapport)

- deux tableaux décrivant les valeurs sur les cotés

*Vous n'êtes pas obligés de savoir comment ils y sont conservés exactement, et je vais m'arranger pour que ce soit impossible de le modifier de l'exterieur. Mais n'hésitez pas à me demander d'ajouter un moyer de lire directement ces valeurs, et par quelle manière ça vous arrangerait.*

#### Méthodes

**Constructeur** : Le constructeur `Grid()` prend en argument un nom de fichier au format grid et en fait une grille. **/!\\** pour l'instant, `Grid` ne peut lire les grilles dont les valeurs sont supérieures à 10.

**get_grid** : La méthode `get_grid` renvoie un string au format *grid* représentant la grille. **/!\\** la méthode `get_grid` a une sortie indéfinie dans le cas où les valeurs sont supérieures à 10.

**mkGroups** : *Non implémenté -* Lance le regroupement des cases par groupe, afin de reconnaître les formes de la grille

### [CNF.py](https://github.com/NeoGalaxy/INF432/blob/master/Classes/CNF.py)
```python
from classes import CNF

print(CNF(("x","y","z"),("-x","-y","z")))
# -> CNF{Cl['x', 'y', 'z'], Cl['-x', '-y', 'z']}
# i.e. la CNF (x + y + z) * (-x + -y + z)

print(CNF((1,2,3),(-1,-2,3)))
# -> CNF{Cl[1, 2, 3], Cl[-1, -2, 3]}
# i.e. une CNF équivalente à (si <x:= 1>, <y:= 2> et <z:= 3>) : 
# (x + y + z) * (-x + -y + z)

from classes import Clause

print(Clause("x","-y","z"))
# -> Cl['x', '-y', 'z']
# i.e. la Clause x + -y + z

print(CNF(Clause("x","-y","z"), Clause("-x","y")))
# -> CNF{Cl['x', '-y', 'z'], Cl['-x', 'y']}
# i.e. la CNF (x + y + z) * (-x + -y)

```

### La classe `Clause`

La classe `Clause` permet de créer des clauses. Elle sert principalement à être utilisée dans la classe `CNF`, qui permet d'enregister un *conjunctive normal form* en attendant de l'écrire dans un fichier au format *DIMACS*.  
Elle contient des littéraux, que j'ai définit tel des entiers stricement positifs ou des chaines de carractères. Les entiers négatifs ou les chaines commençant par un `-` sont les négations des littéraux qui leur correspondent. Quand le fichier *DIMACS* sera créé, tous les littéraix seront traduits en des entier positifs entre 1 et le nombre de littéraux. 

#### Méthodes

**Constructeur** : Le constructeur `Clause(args...)` crée un objet de classe `Clause`, et exécute `addLitt()` sur les arguments `args`.

**addLitt** : La méthode `addLitt(args...)` prend en argument un nombre non spécifié de littéraux (càd d'entiers non nuls ou de chaînes de charactères) et les ajoute à la clause. La méthode renvoie l'objet (afin de pouvoir cascader les méthodes). Lance une erreur si un argument n'est pas un littéral.  
*Si vous avez une liste `liste` de littéraux que vous voulez ajouter à la clause, pensez à la syntaxe `addLitt(*liste)`*

### La classe `CNF`

La classe `CNF` permet de créer un *conjunctive normal form*, qui est tel une liste de clauses. Elle permet de créer des *conjunctive normal form* qui seront prêts à être écrits dans un fichier *DIMACS*. Des littéraux qui sont égaux (d'après la comparaison `==` de Python) seront considérés tel un même littéral (de même, un entier et son négatifs seront considérés tels des négations l'un de l'autre, et de même pour un string et le même string avec un `-` devant).

### Méthodes

**Constructeur** : Le constructeur `CNF(args...)` crée un objet de classe `CNF`, et exécute `addClause()` sur les arguments `args`.

**addClause** : La méthode `addClause(args...)` prend en argument un nombre non psécifié de clauses et les ajoute au `CNF`. La méthode renvoie l'objet (afin de pouvoir cascader les méthodes). Lance une erreur si un argument n'est pas une clause.  
*Si vous avez une liste `liste` de clauses que vous voulez ajouter à la clause, pensez à la syntaxe `addClause(*liste)`*

## [Inputs](https://github.com/NeoGalaxy/INF432/tree/master/Inputs)

Aujourd'hui, un seul format d'entrée est possible : le format [`grid1`](#Format-grid1). Un format `JSON` est à prévoir, pour par exemple de grandes grilles.

### Format grid1

```
grid1
  _ _ _ _ _ _   # Ligne représentant le "toît" de la grille.
5|_|  _ _ _| |  #|
3|  _|_    |_|  #|
3|_|_  | |_ _|  #|
2|   |_|_|  _|  #|
2| |  _   _|_|  #|
 |_|_|_|_|_ _|  #\-> Lignes de la grille, décrivant les murs et valeurs horizontales
  5 3 2 3 3 4   # Valeurs verticales
```

Le format *grid1* a été créé afin d'avoir une représentation assez visuelle du fichier. 

1- La première ligne contient juste le mot `grid1`, rien de moins, rien de plus.  
2- La seconde ligne est composée essentiellement du toit de la grille, c'est-à-dire d'espaces et d'underscores comme montré ci-dessus.  
3- Les lignes suivantes indiquent le nombre de cases qui doivent être remplies sur la ligne, ainsi que la présence ou l'absence de murs horizontaux sur les cotés de chaque cases et verticaux sur le dessous de chaque case. Vous pouvez remarquer que sur la dernière ligne, les murs horizontaux sont tous présents, ainsi que les murs verticaux en début et fin de ligne (pour que la grille soit fermée).  
4- La dernière ligne est composée des valeurs décrivant le nombre de cases d'eau sur chaque colonne.

#### Règles d'alignement :

Règle 1
> La taille horizontale de chaque case doit être la même. Exemple :
> ```
> [...] __ ___ _ _ [...] # toit
> [...]|  |___| |_|[...] # lignes intermédiaires
> [...]|__|___|_|_|[...] # dernière ligne
> [...] 12  3  1 2 [...] # valeurs verticales
> ``` 
> *Cette règle a été mise-en place pour permettre des valeurs verticales aussi grandes que possibles*

Règle 2
> L'espace devant chaque ligne doit être le même. Exemple :
> ```
>    _ _ _[...] # toit
> 1 | |_| [...] # lignes intermédiaires
> 13|_|_|_[...] # dernière ligne
>    1    [...] # valeurs verticales
> ``` 
> *Cette règle a été mise-en place pour permettre des valeurs horizontales aussi grandes que possibles*
