import pycosat as sat

class Clause:
	def __init__ (self, *litterals) :
		"""Create a clause, and add to it each of the literals given in argument.
		A literal should be :
		- An integer different of 0. If the integer is negative, it is considered as the negation of the positive integer
		- Or a string. It it starts by a minus ('-'), it is the negation of the same string without the minus
		  Caution : strings starting by at least two minuses gives unexpected results.
		"""
		self.c = []
		self.addLitt(*litterals)

	def addLitt(self, *litterals) :
		"""Add to a clause each of the literals given in argument. 
		See help on the initializer (Clause.__init__) to know what is a literal"""
		c = list(self.c)
		for l in litterals:
			if (not (type(l) in [str,int])) : raise TypeError(
				"Clauses contains literals, which should be strings or integers."+
				" The argument '"+str(l)+"' is of type '"+str(type(l))+"'."
			)
			if (l == 0) : raise TypeError("The value 0 is forbidden, since it has virtually no negation.")
			c.append(l)
		self.c = c
		return self

	def fusion (self, *clauses):
		"""Merge the clause self with the given clauses"""
		return Clause(*sum((cl.c for cl in clauses), self.c))

	def __str__(self):
		return "Cl"+str(self.c)

	def __repr__(self):
		return self.__str__()


class CNF:
	def __init__(self, *clauses):
		"""Create a CNF, and add to it each of the clause given in argument.
		A tuple or a list can be given instead of a clause, in which case a clause will be created of it.
		"""
		self.dico = {}
		self.c = []
		self.addClause(*clauses)

	def addClause(self, *clauses):
		"""Add to a CNF each of the clause given in argument.
		A tuple or a list can be given instead of a clause, in which case a clause will be created of it.
		"""
		for cl in clauses:
			t = type(cl)
			if (t == Clause) :
				self.c.append(cl)
			elif (t in [list, tuple]) :
				self.c.append(Clause(*cl))
			else : raise TypeError(
				"CNFs contains only clauses (or lists of litterals), the argument '"
				+str(cl)+"' is of type '"+str(type(cl))+"'."
			)
		return self

	def fusion (self, *cnfs):
		"""Merge the CNF self with the given CNFs"""
		res = CNF(*sum((e.c for e in cnfs), self.c))
		res.dico = self.dico.copy()
		return res

	def toIntegers(self):
		"""Convert the CNF where a literal is a string or an int into a CNF coherent with the DIMACS format"""
		ret = []
		for cl in self.c:
			intCl = []
			for litt in cl.c:

				isNeg = False
				if (type(litt) == str and litt[0] == '-') or (type(litt) == int and litt < 0) :
					isNeg = True
					if type(litt) == str:
						litt = litt[1:]
					else :
						litt = -litt

				if not (litt in self.dico.keys()) :
					self.dico[litt] = len(self.dico)+1
				intLitt = self.dico[litt]
				if isNeg: intLitt = -intLitt

				intCl.append(intLitt)
			ret.append(intCl)
		return ret

	def readSolution(self, sol:list):
		"""Convert the solution sol being a list of integers into a list of literals.
		The input should be a result from a SAT solver's execution over the CNF self."""
		if sol == 'UNSAT': return "UNSAT"
		inverted = {v: k for k, v in self.dico.items()}
		ret = []
		for litt in sol:
			isNeg = False
			if litt < 0: 
				isNeg = True
				litt = -litt
			try:
				litt = inverted[litt]
			except KeyError as e:
				raise ValueError("The litteral "+str(litt)+" is not produced by the CNF")

			if isNeg: 
				if type(litt) == str : litt = "-"+litt
				else : litt = -litt
			ret.append(litt)
		return ret


	def solve(self):
		"""Return a list of literals being a solution of the CNF self, or 'UNSAT' if self is unsatisfiable."""
		return self.readSolution(sat.solve(self.toIntegers()))

	def readIterSolution(self, itersol):
		"""Returns a generator applying CNF.readIterSolution to each element of the iterator given in argument. 
		The input is expected to be an iterator over results from a SAT solver's execution over this CNF."""
		return (self.readSolution(s) for s in itersol)


	def itersolve(self):
		"""Return an iterator over the solutions of the CNF self."""
		return self.readIterSolution(sat.itersolve(self.toIntegers()))

	def ecrDimacs(self, path:str):
		"""Writes a file at the path given in argument in the format DIMMACS."""
		clauses =  len(self.c)
		tempo = " 0\n".join(" ".join(str(v) for v in l) for l in self.toIntegers()) + " 0\n"
		
		"""
		if at the beginning we have : self.dico = {} and self.c = [[5, -2, z],[z, a, -5],[2, -z],[-a]],
		we should obtain :
			# self.dico = {"5" : "1", "2" : "2", "z" : "3", "a" : "4"}
			# tempo = "1 -2 3 0\n3 4 -1 0\n2 -3 0\n-4 0\n"
			maxLiterals = 4
		"""

		fichier = open(path,"w")
		fichier.write("c language : DIMACS CNF -> for the sat solver\n")
		fichier.write("p cnf {} {}\n" .format(len(self.dico), clauses))
		fichier.write(tempo)
		fichier.close()
		"""
		Si on a self.c = [[5, -2, z],[z, a, -5],[2, -z],[-a]] le fichier sera le suivant :
			*************************************************
			* c language : DIMACS CNF -> for the sat solver *
			* p cnf 4 4										*
			* 1 -2 3 0										*
			* 3 4 -1 0										*
			* 2 -3 0										*
			* -4 0											*
			*												*
			*************************************************
		"""

	def copy(self) :
		"""Returns a shallow copy of self."""
		res = CNF(*self.c)
		res.dico = self.dico.copy()
		return res

	def __iter__(self):
		return (x for x in self.c.copy())

	def __str__(self):
		return ("CNF{"+", ".join([str(x) for x in self.c])+"}")

	def __repr__(self):
		return self.__str__()
