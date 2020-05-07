import io
import warnings
from itertools import groupby as gb
from itertools import combinations
from .CNF import CNF

class Direction:
	NORD = 0
	SUD = 1
	EST = 2
	OUEST = 3
(NORD, SUD, EST, OUEST) = (Direction.NORD, Direction.SUD, Direction.EST, Direction.OUEST)

class Grid:
	def __init__(self, arg):
		"""Parse a specified grid.
		The arg should be of type :
		- 'str' if it contains a path to a grid or the content of the grid itself
		- '_io.TextIOWrapper' if the opened file contains the grid
		- 'list' if it contains each line of the grid"""
		self.__l = 0
		self.__h = 0
		self.__barrier  = {'v':[], 'h':[]} # AKA. Bc and Bl in the report
		self.__values = {'v':[], 'h':[]} # AKA. Zc and Zl in the report
		self.__groups = None
		self.__waterPhysicsCNF = None
		self.__tilesNbCNF = None
		self.__cnf = None
		self.__solutions = None

		try:
			if (type(arg) == io.TextIOWrapper) :
				grid = arg.read().split("\n")
			elif (type(arg) == str) :
				if ('\n' in arg) :
					grid = arg.split("\n")
				else :
					f = open(arg, "r")
					grid = f.read().split("\n")
					f.close()
				
			elif (type(arg) == list) :
				grid = arg
			else :
				raise TypeError("The argument should be a string containing the grid, a list of strings, each being a line of the grid, a string containing a file's name or directly the file.")
		except Exception as e:
			raise e

		if grid[0] == "grid1":
			self.__readGrid(grid[1:])
		else :
			raise ValueError("Invalid format (the first line '"+grid[0]+"' does not correspond to grid1).\n")
		self.__mkGroups()
		self.__waterPhysicsCNF = self.__getWaterPhys()
		self.__tilesNbCNF = self.__getTilesNbCNF()
		self.__cnf = self.__waterPhysicsCNF.fusion(self.__tilesNbCNF)

	def getBarrier(self, i:int, j:int, o:Direction):
		"""Returns True if and only if the grid has a barrier on the o border of the tile i,j"""
		if not(0 <= i < self.__l) or not(0 <= j < self.__h) : # Yes, it is allowed in python xD
			raise KeyError("The node of coordinates ("+str(i)+","+str(j)+") doesn't exist.")

		if (o == NORD) :
			if (j == self.__h-1) : return True # The first line always have a barrier above
			return (self.__barrier["h"][self.__h-2-j][i])

		if (o == SUD) :
			if (j == 0) : return True # The last line always have a barrier under
			return (self.__barrier["h"][self.__h-1-j][i])
			
		if (o == EST) :
			if (i == self.__l -1) : return True # The line on the left always have a barrier on its left
			return (self.__barrier["v"][self.__h-1-j][i])
			
		if (o == OUEST) :
			if (i == 0) : return True # The line on the right always have a barrier on its right
			return (self.__barrier["v"][self.__h-1-j][i-1])

	def getValVert(self, i:int):
		"""returns the value on the column number i, or None if the column doesn't have any"""
		v = self.__values["v"][i]
		return None if v == -1 else v

	def getValHor(self, j:int):
		"""returns the value on the line number j, or None if the line doesn't have any"""
		v = self.__values["h"][self.h()-j-1]
		return None if v == -1 else v

	def getGrid(self):
		"""returns a string representing the grid in grid1 format. 
		(Warning: the method is not totally finished, and the output is not valid if a value has more than 1 digit.)"""
		maxLen = max(len(str(v)) for v in self.__values['h'])
		colsWidth = [(len(str(v)) if v != -1 else 1) for v in self.__values['v']]
		res = "grid1\n#Automatically generated grid\n "+ " "*maxLen+ (" ".join("_"*v for v in colsWidth)) + " \n"
		for y in range(self.__h):
			val = str(self.__values['h'][y]) if self.__values['h'][y] != -1 else " "
			res += " "*(maxLen - len(val)) + val
			res += '|'
			for x in range(self.__l):
				res += ('_' if y == self.__h-1 or self.__barrier['h'][y][x] else ' ')*colsWidth[x]
				res += '|' if x == self.__l-1 or self.__barrier['v'][y][x] else ' '
			res += "\n"
		res += " "*maxLen + " " + " ".join(str(x) if x != -1 else " " for x in self.__values['v'])
		return res

	def getGroup(self,x:int,y:int) :
		"""returns the group number of the tile of indexes x,y."""
		if self.__groups == None:
			raise NotImplementedError("Not working until .mkGroups() is not successfully run.")
		try:
			return self.__groups[self.__h-y-1][x]
		except IndexError as e:
			warnings.warn("The index is out of the grid, returning 0.",RuntimeWarning,2)
			return 0

	def getWaterPhys(self) :
		"""returns the CNF object representing the water physics."""
		if self.__waterPhysicsCNF == None: return None
		return self.__waterPhysicsCNF.copy()

	def getTilesNbCNF(self) :
		"""returns the CNF object representing the tile number."""
		if self.__tilesNbCNF == None: return None
		return self.__tilesNbCNF.copy()

	def getCNF(self) :
		"""returns the CNF object representing the whole grid."""
		if self.__cnf == None: return None
		return self.__cnf.copy()

	def getSolution(self):
		"""returns an array of string, representing a solution of the grid, or returns 'UNSAT' if the grid is unsatisfiable."""
		if self.__cnf == None:
			raise NotImplementedError("The CNF is not generated yet")
		return self.__cnf.solve()

	def getNextSolution(self):
		"""returns a new array of string on each call, each array representing a solution of the grid.
		If there is no more solution remaining, returns None and reset itself.
		The internal iterator is the same as the one in Grid.__next__()."""
		try:
			return self.__next__()
		except StopIteration as e:
			self.__solutions = None
			return None

	def getAllSolutions(self):
		"""Returns an iterator, with each value of the iterator being an array of string representing a solution of the grid"""
		return self.__cnf.itersolve()

	def writeSvg(self,f, sol:list = []):
		"""Transform the grid into an svg picture, and write it in the file f. 
		If sol is specified, it will color the tiles full of water in blue and the empty tiles in gray.
		Note : sol should be an array returned by getSolution(), getNextSolution() or by the iterator obtained in getAllSolutions()"""
		f.write('<?xml version="1.1" encoding="UTF-8"?>\n')
		length = self.l()
		height = self.h()

		### Cases
		f.write('<svg width="{}" height="{}" viewBox="-1 -1 {} {}">\n'.format(100*(length+2),100*(height+2),(length+2),(height+2)))
		f.write('\t<rect x="-1" y="-1" width="100%" height="100%" fill="white"/>\n')

		f.write('\t<g>\n')
		for case in sol:
			if case[0] == "-":
				case = case[1:]
				color = "#b3b3b0"
			else: 
				color = "#038"
			(x,y) = (int(i) for i in case.split(","))
			f.write('\t\t<rect x="{}" y="{}" width="1" height="1" fill="{}"/>\n'.format(x,height - y -1,color))
		f.write('\t</g>\n')

		### Murs
		f.write('\t<path stroke="black" stroke-linecap="round" stroke-width="0.1" d="M 0 0 L 0 {}" />\n'.format(height))
		f.write('\t<g>\n')
		for x,y in ((i,j) for i in range(length) for j in range(height)):
			if self.getBarrier(x,y,SUD):
				f.write('\t\t<path stroke="black" stroke-linecap="round" stroke-width="0.1" d="M {} {} L {} {}" />\n'.format(x,height-y,x+1,height-y))
			if self.getBarrier(x,y,EST):
				f.write('\t\t<path stroke="black" stroke-linecap="round" stroke-width="0.1" d="M {} {} L {} {}" />\n'.format(x+1,height-y,x+1,height-(y+1)))
		f.write('\t</g>\n')

		### Valeurs
		f.write('\t<g>\n')
		for i in range(len(self.__values['v'])):
			val = self.__values['v'][i]
			if val != -1:
				f.write('\t\t<text x="{}" y="{}" font-size="1">{}</text>\n'.format(i+0.25,height+1,val))
		f.write('\t</g>\n')
		f.write('\t<g>\n')
		for j in range(len(self.__values['h'])):
			val = self.__values['h'][j]
			if val != -1:
				f.write('\t\t<text x="{}" y="{}" font-size="1">{}</text>\n'.format(length+0.25,j+0.9,val))
		f.write('\t</g>\n')
		f.write('</svg>\n')

	def writeSvgs(self, sol:list = []):
		"""Transform the grid into an svg picture, and return it as a string.
		Typically the same effect as Grid.writeSvg(f,sol), but returns the content instead of writing it."""
		svg = '<?xml version="1.1" encoding="UTF-8"?>\n'
		length = self.l()
		height = self.h()

		### Cases
		svg += '<svg width="{}" height="{}" viewBox="-1 -1 {} {}">\n'.format(100*(length+2),100*(height+2),(length+2),(height+2))
		svg += '\t<rect x="-1" y="-1" width="100%" height="100%" fill="white"/>\n'

		svg += '\t<g>\n'
		for case in sol:
			if case[0] == "-":
				case = case[1:]
				color = "#b3b3b0"
			else: 
				color = "#038"
			(x,y) = (int(i) for i in case.split(","))
			svg += '\t\t<rect x="{}" y="{}" width="1" height="1" fill="{}"/>\n'.format(x,height - y -1,color)
		svg += '\t</g>\n'

		### Murs
		svg += '\t<path stroke="black" stroke-linecap="round" stroke-width="0.1" d="M 0 0 L 0 {}" />\n'.format(height)
		svg += '\t<g>\n'
		for x,y in ((i,j) for i in range(length) for j in range(height)):
			if self.getBarrier(x,y,SUD):
				svg += '\t\t<path stroke="black" stroke-linecap="round" stroke-width="0.1" d="M {} {} L {} {}" />\n'.format(x,height-y,x+1,height-y)
			if self.getBarrier(x,y,EST):
				svg += '\t\t<path stroke="black" stroke-linecap="round" stroke-width="0.1" d="M {} {} L {} {}" />\n'.format(x+1,height-y,x+1,height-(y+1))
		svg += '\t</g>\n'

		### Valeurs
		svg += ('\t<g>\n')
		for i in range(len(self.__values['v'])):
			val = self.__values['v'][i]
			if val != -1:
				svg += ('\t\t<text x="{}" y="{}" font-size="1">{}</text>\n'.format(i+0.25,height+0.9,val))
		svg += ('\t</g>\n')
		svg += ('\t<g>\n')
		for j in range(len(self.__values['h'])):
			val = self.__values['h'][j]
			if val != -1:
				svg += ('\t\t<text x="{}" y="{}" font-size="1">{}</text>\n'.format(length+0.25,j+0.9,val))
		svg += '\t</g>\n'
		svg += '</svg>\n'
		return svg

	def h(self) :
		"""The height of the grid"""
		return self.__h

	def l(self) :
		"""The length of the grid"""
		return self.__l

	#########################################################################
	############################ Private methods ############################
	#########################################################################

	#======================#   From Grid to CNF   #======================#

	""" algo :
		my_CNF=create_CNF_vide()
		for all case1[x1][y] in grille :
			if case[x1][y-1] is in the same group as case1 then:
				add (-[x1,y] + [x1,y-1]) to my_CNF (i.e case[x1,y] => case[x1,y-1])

			for all case2[x2][y] different from case1:
				if case2 is in the same group as case1 then:
					add (-[x1,y] + [x2,y]) to my_CNF (i.e case[x1,y] => case[x2,y])

	"""
	def __getWaterPhys(self) :
		myCNF = CNF()
		for x,y in ((i,j) for j in range (0, self.__h) for i in range (0, self.__l) ):
			if y > 0 and self.getGroup(x,y) == self.getGroup(x,y-1) :
				myCNF.addClause(["-"+str(x)+","+str(y) , str(x)+","+str(y-1)])
			
			for x2 in range (0, self.__l):
				if x != x2 and (self.getGroup(x,y) == self.getGroup(x2,y)) :
					myCNF.addClause(["-"+str(x)+","+str(y) , str(x2)+","+str(y)])

		return myCNF


	def __getTilesNbCNF(self) :
		myCNF = CNF()
		for y in range(self.h()):
			hVal = self.getValHor(y)
			if hVal == None: continue # On saute les lignes qui n'ont pas de val
			for indexes in combinations(range(self.l()), self.l()-hVal+1):
				myCNF.addClause([str(i)+","+str(y) for i in indexes])
			for indexes in combinations(range(self.l()), hVal+1):
				myCNF.addClause(["-"+str(i)+","+str(y) for i in indexes])

		for x in range(self.l()):
			vVal = self.getValVert(x)
			if vVal == None: continue # On saute les lignes qui n'ont pas de val
			for indexes in combinations(range(self.h()), self.h()-vVal+1):
				myCNF.addClause([str(x)+","+str(i) for i in indexes])
			for indexes in combinations(range(self.h()), vVal+1):
				myCNF.addClause(["-"+str(x)+","+str(i) for i in indexes])

		return myCNF


	#======================#   Utilities   #======================#

	def __readGrid(self, textLines):
		"""Parse the iterable textLines into a grid"""
		colsIndex = None
		for line in textLines:
			line = line.split("#",1)[0].rstrip() # We don't take in account the comments and whitespaces at the end
			if len(line) == 0: continue          # If the line is empty, we can skip it

			"""Parse the first line"""
			if colsIndex == None:
				colsIndex = [(0,len(line.split("_",1)[0])-1)] # give the width of the first column of the lines
				if line[0] != " " : 
					raise ValueError("The first line should start with white spaces.")
				for char, nb in ((label, sum(1 for _ in group)) for label, group in gb(line)):
					if not char in " _":
						raise ValueError("The first line should only contain white spaces and underscores.")
					if char == " " and nb > 1 and len(colsIndex) > 1:
						raise ValueError("The column separator between col "+str(len(colsIndex)-1)+" and col "+str(len(colsIndex))+" is too wide.")
					if char == "_":
						colsIndex.append(((colsIndex[-1][1]+1), (nb+colsIndex[-1][1]+1)))
				self.__l = len(colsIndex)-1
				continue

			"""Prepare the parsing of other lines"""
			"""try:
				splitted_line = [line[x:y] for x,y in colsIndex]
			except Exception as e:
				raise e"""

			"""Parse the last line"""
			if line[colsIndex[0][1]] != "|": 
				self.__values["v"] = [self.__strToVal(line[x:y],len(self.__barrier["v"])) for x,y in colsIndex[1:]]

				"""Parse all the other lines"""
			else : 
				barrier = {"v":[], "h":[]}
				self.__values["h"].append(self.__strToVal(line[0:colsIndex[0][1]], len(colsIndex)-1))
				for x,y in colsIndex[1:] :
					s = line[x:y]
					if not (s[0] in " _") or len(list(gb(s))) > 1 :
						raise ValueError("La grille a une erreur ligne "+str(len(self.__values["h"])))

					if s[0] == '_':
						barrier["h"].append(True)
					else :
						barrier["h"].append(False)

					if line[y] == '|':
						barrier["v"].append(True)
					else :
						barrier["v"].append(False)

				self.__barrier["h"].append(barrier["h"])
				barrier["v"].pop()
				self.__barrier["v"].append(barrier["v"])

		self.__barrier["h"].pop()
		self.__h = len(self.__barrier["v"])

	"""add (i,j) the the group n"""
	def __addToGrp(self,i,j,n):
		self.__groups[j][i] = n
		self.groups = self.__groups
		if (not(self.getBarrier(i,self.__h-1-j, SUD)) and self.__groups[j+1][i] == None): 
			self.__addToGrp(i,j+1,n)

		if (not(self.getBarrier(i,self.__h-1-j, NORD)) and self.__groups[j-1][i] == None): 
			self.__addToGrp(i,j-1,n)

		if (not(self.getBarrier(i,self.__h-1-j, EST)) and self.__groups[j][i+1] == None): 
			self.__addToGrp(i+1,j,n)

		if (not(self.getBarrier(i,self.__h-1-j, OUEST)) and self.__groups[j][i-1] == None): 
			self.__addToGrp(i-1,j,n)
	
	"""Group the tiles of the grid"""
	def __mkGroups(self) :
		nbGroups = 0
		self.__groups = [[None for i in range(self.__l)] for j in range(self.__h)]
		for i in range(self.__l):
			for j in range(self.__h):
				if (self.__groups[j][i] == None):
					nbGroups += 1
					self.__addToGrp(i,j,nbGroups)

	"""Parse a value on the border of the grid"""
	def __strToVal(self, elem, s) :
		elem = elem.strip()
		if elem == "":
			return -1
		if elem.isdigit():
			elem = int(elem)
			if not(0 <= elem <= s):
				raise ValueError("The values should be between 0 and the size. "+str(elem)+" is not in these bounds.")
			return elem
		else:
			raise ValueError("The last line should contain only digits and spaces, "+repr(elem)+" is not valid.")

	def __next__(self):
		if self.__cnf == None:
			raise NotImplementedError("The CNF is not generated yet")
		if self.__solutions == None:
			self.__solutions = self.__cnf.itersolve()
		return next(self.__solutions)

	def __iter__(self): return self.getAllSolutions()

	def __str__(self):
		return "("+str(self.__l)+"x"+str(self.__h)+" grid)"

	def __repr__(self):
		return self.__str__()

