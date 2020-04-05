from typing import List

class Clause:
	def __init__ (self, *litterals) :
		self.c = []
		self.addLitt(*litterals)

	def addLitt(self, *litterals) :
		for l in litterals:
			if (not (type(l) in [str,int])) : raise TypeError(
				"Clauses contains litterals, which should be strings or integers."+
				" The argument '"+str(l)+"' is of type '"+str(type(l))+"'."
			)
			self.c.append(l)
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

	def __str__(self):
		return ("CNF{"+", ".join([str(x) for x in self.c])+"}")

	def __repr__(self):
		return self.__str__()
