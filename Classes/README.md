# Classes README

There are 2 files, and 3 classes : the class `Grid` in **Grid.py** and the classes `CNF` and `Clause` in **CNF.py**.  
To have a list of their methods and their usage, use `help(<class>)` in a python interpreter. Warning : don't use these methods with a different type as the ones specified, or the result will be undefined. 

### The class `Grid` 
It is the main class of the project : from it you can parse a grid and solve it. To parse a grid, simply do `Grid(<grid to parse>)`, with the argument being a file, a path, or the grid itself in a string (or a list). 

### The class `Clause` 
It is used to define the class `CNF`. It is a class that represent a clause, and that is implemented as a list of literals. A literal is defined as a strictly positive or negative integer, or as a string (that starts with a `'-'` if it is a negation of the string without the `'-'`). Note that the definition of a literal here is weaker as a literal in the DIMACS format, and this is the purpose of the classes `CNF` and `Clause` (see next paragraph).

### The class `CNF`
It is used as intermediate between the project and the SAT-solver. It is here in order to have more flexibilities on the literals format. This class is implemented as a list of clauses (as described above). If a list or a tuple is given to a `CNF` instead of a clause, it will first create a clause out of it. Objects of type `CNF` can be added a clause anytime or can be merged with another CNF. The CNF object is able to translate itself into a list of integers that is coherent with the DIMACS format (simply maps the first encountered literal to 1, the second to 2, and so on...), and to revert this operation.
