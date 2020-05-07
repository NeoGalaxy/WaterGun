# INF432 Project : Water Fun grid solver

## Organization

The Grid solver is implemented in the directory [`/Classes`](https://github.com/NeoGalaxy/INF432/tree/master/Classes), see [`/Classes/README.md`](https://github.com/NeoGalaxy/INF432/tree/master/Classes/README.md) to know more.


The directory [`/Inputs`](https://github.com/NeoGalaxy/INF432/tree/master/Inputs) is meant to contain the different grids to use as input, and their solutions.


The directory [`/Outputs`](https://github.com/NeoGalaxy/INF432/tree/master/Outputs) is meant to contain the svg files produced by the solver. Indeed, the solver can produce a SVG file (or a svg formatted string) to represent a grid or a grid's solution.


The directory [`/Tests`](https://github.com/NeoGalaxy/INF432/tree/master/Tests) contains some tests using the different functionalities of the solver, as well as the file [`classes.py`](https://github.com/NeoGalaxy/INF432/blob/master/Tests/classes.py) allowing to import [`/Classes`](https://github.com/NeoGalaxy/INF432/blob/master/Classes) inside [`/Tests`](https://github.com/NeoGalaxy/INF432/blob/master/Tests). If you want or need to implement and test your own code, it is a good place to do it. (Be careful to keep the file `classes.py`, otherwise the other tests won't run anymore)


The directory [`/InterpreterUtils`](https://github.com/NeoGalaxy/INF432/tree/master/InterpreterUtils) contains some code used by the interpreter [`main.py`](https://github.com/NeoGalaxy/INF432/tree/main.py).

## Usage

You have 3 ways to use our solver : 
1. Launch the interpreter [`main.py`](https://github.com/NeoGalaxy/INF432/tree/main.py) after moving the grid(s) you want to resolve into the directory [`/Inputs`](https://github.com/NeoGalaxy/INF432/tree/master/Inputs) or set the *path to the grids to read* configuration to the directory where your grid is located if it is not already done.
2. Write your code in the directory [`/Tests`](https://github.com/NeoGalaxy/INF432/tree/master/Tests). 
3. Copy the directory [`/Classes`](https://github.com/NeoGalaxy/INF432/tree/master/Classes) into your project, and use it.

If you use the interpreter, refer to its help command in order to understand how it works.

For the two other solutions, you will need to first import the classes. If you are in the directory [`/Inputs`](https://github.com/NeoGalaxy/INF432/tree/master/Inputs), you can simply import `classes.py` or import from it the classes you need:
```python
from classes import *
```
Otherwise, you'll need to import the directory [`/Classes`](https://github.com/NeoGalaxy/INF432/tree/master/Classes). If it is in your current directory, you can simply do the following :
```python
from Classes import *
```
Otherwise, you'll have to find a way to import it (like done in `classes.py`).

_____________
Now that the classes are imported, to create a grid from a file or a string, use the class `Grid`. The `Grid` class' constructor can take many different kinds of variables as argument (A string containing the file's path, an opened file, a string containing the grid, a list of strings with each element of the list being a line of the grid):
```python
from classes import Grid #assuming you are in /Inputs
gridN1 = Grid("../Inputs/Grids/Probs/grid1.grid")
with f as open("../Inputs/Grids/Probs/example.grid")
	gridN2 = Grid(f)
with f as open("../Inputs/Grids/Probs/grid2x5N.grid")
	txt = f.read()
	gridN3 = Grid(txt)
print("grid number 1 : ",gridN1) # -> "(6x6 grid)"
print(gridN1.getGrid()) # print the grid in grid1 format
print("grid number 2 : ",gridN2) # -> "(6x6 grid)"
print(gridN2.getGrid()) # print the grid in grid1 format
print("grid number 3 : ",gridN3) # -> "(6x6 grid)"
print(gridN3.getGrid()) # print the grid in grid1 format
```

_____________
Now, to get a solution, just use `Grid.getSolution()`. The return value of this call is a list of strings, each string being of the form `"i,j"` or `"-i,j"`, `i` and `j` being the coordinates of the tile from the bottom left. If there is a `-`, then the tile should be empty, and if there is no `-`, the tile should have water (and if there is neither, this tile can be empty as well as full of water).  
You can also use `Grid.getNextSolution()`, which gives a new solution on each call until it returns `None` (which means there are no other solution), or `Grid.getAllSolutions()` which returns a generator (a kind of iterator) over the different solutions, or even iterate through grid (with `next()` or with a for loop). Here is an example:
```python
from classes import Grid

mygrid = Grid("../Inputs/Grids/Probs/grid1x2_multiple_answer.grid")
print("Grid : \n"+mygrid.getGrid(),"\n")

######## using Grid.getSolution() ########
print("\nSingle solution :")
print(mygrid.getSolution())

######## using Grid.getAllSolution() ########
print("\nAll solutions :")
print("\n".join(str(s) for s in mygrid.getAllSolutions()))

######## using Grid.getNextSolution() ########
print("\nAll solutions by getNextSolution :")
s = ""
while s != None: # I miss do...while loops, why aren't they in python...?
	s = mygrid.getNextSolution()
	print(s)

######## using next(Grid) ########
print("\nAll solutions using next :")
try:
	while True:
		s = next(mygrid)
		print(s)
except Exception as e:
	print("-> Ended")

######## using for loop ########
print("\nAll solutions by for loop :")
for s in (mygrid):
	print(s)
```
> **/!\\** Note the following : The iterator used by Grid.getNextSolution() and next(Grid) are the same. So mixing both methods will result in iterating thought the same iterator (and **not** though two different iterators). The difference between them is that `next(Grid)` will throw an error after the last element (as expected for an iterator), whereas `Grid.getNextSolution()` will return a `None` **and reset the iterator** (allowing to re-use Grid.getNextSolution() and next(Grid) after it has returned None).
