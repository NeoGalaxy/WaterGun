from typing import List

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

	def __str__(self):
		return "Cl"+str(self.c)

	def __repr__(self):
		return self.__str__()


class CNF:
	def __init__(self, *clauses):
		self.c = []#List[Clause] # content
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

	def ecrDimacs(self, path):
			clauses =  len(slef.c)
			maxLitterals = 0
			tempo = ""

			for cl in self.c:
				if (len(cl)>maxLitterals):
					maxLitterals = len(cl)
				for l in cl.c:
					tempo = tempo + str(l) + " "
				tempo = tempo + "0\n"
				
			# we should have : tempo = " l0 l1 0\nl2 l3 l4 0\n ..."		
			
			fichier = open(path,"w")
			fichier.write("c language : DIMACS CNF -> for the sat solver\n")
			fichier.write("p cnf {} {}\n" .format(maxLitterals, clauses))
			fichier.write(tempo)
			fichier.close()
			"""
			Si on a self.c = [[1, -3], [2, 3, -1]] le fichier sera le suivant :
				*************************************************
				* c language : DIMACS CNF -> for the sat solver *
				* p cnf 3 2										*
				* 1 -3 0										*
				* 2 3 -1 0										*
				*												*
				*************************************************
			"""


	def __str__(self):
		return ("CNF{"+", ".join([str(x) for x in self.c])+"}")

	def __repr__(self):
		return self.__str__()
