import pycosat as sat

class Clause:
	def __init__ (self, *litterals) :
		self.c = []
		self.addLitt(*litterals)

	def addLitt(self, *litterals) :
		c = list(self.c)
		for l in litterals:
			if (not (type(l) in [str,int])) : raise TypeError(
				"Clauses contains litterals, which should be strings or integers."+
				" The argument '"+str(l)+"' is of type '"+str(type(l))+"'."
			)
			if (l == 0) : raise TypeError("The value 0 is forbidden, since it has virtually no negation.")
			c.append(l)
		self.c = c
		return self

	def fusion (self, *clauses):
		return Clause(*sum((cl.c for cl in clauses), self.c))

	def __str__(self):
		return "Cl"+str(self.c)

	def __repr__(self):
		return self.__str__()


class CNF:
	def __init__(self, *clauses):
		self.dico = {}
		self.c = []
		self.addClause(*clauses)

	def addClause(self, *clauses):
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
		res = CNF(*sum((e.c for e in cnfs), self.c))
		res.dico = self.dico.copy()
		return res

	"""Convert the CNF where a litteral is a string or an int into a CNF coherent with the DIMACS format"""
	def toIntegers(self):
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

	def readSolution(self, sol):
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
		return self.readSolution(sat.solve(self.toIntegers()))

	def readIterSolution(self, itersol):
		return (self.readSolution(s) for s in itersol)


	def itersolve(self):
		return self.readIterSolution(sat.itersolve(self.toIntegers()))

	def ecrDimacs(self, path):
			clauses =  len(self.c)
			tempo = " 0\n".join(" ".join(str(v) for v in l) for l in self.toIntegers())
			
			"""
			if at the beginning whe have : self.dico = {} and self.c = [[5, -2, z],[z, a, -5],[2, -z],[-a]],
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
		res = CNF(*self.c)
		res.dico = self.dico.copy()
		return res

	def __str__(self):
		return ("CNF{"+", ".join([str(x) for x in self.c])+"}")

	def __repr__(self):
		return self.__str__()
