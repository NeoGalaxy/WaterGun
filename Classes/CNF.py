
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

	def ecrDimacs(self, path):
			clauses =  len(self.c)
			tempo = ""

			for cl in self.c:
				for l in cl.c:
					l = str(l)
					
					if (l[0] == '-') :
						l = l[1:]
						if not (l in list(self.dico.keys())) :
							self.dico[l] = str(len(self.dico)+1)
						l = '-' + self.dico.get(l)

					else :
						if not (l in list(self.dico.keys())) :
							self.dico[l] = str(len(self.dico)+1)
						l = self.dico.get(l)

					tempo += l + " "

				tempo += "0\n"

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


	def __str__(self):
		return ("CNF{"+", ".join([str(x) for x in self.c])+"}")

	def __repr__(self):
		return self.__str__()
