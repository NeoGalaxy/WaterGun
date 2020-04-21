class Direction:
	NORD = 0
	SUD = 1
	EST = 2
	OUEST = 3
(NORD, SUD, EST, OUEST) = (Direction.NORD, Direction.SUD, Direction.EST, Direction.OUEST)

class Grid:

	groups = []
	def __init__(self, name):
		self.__l = 0
		self.__h = 0
		self.__barrier  = {'v':[], 'h':[]} # AKA. Bc and Bl in the report
		self.__values = {'v':[], 'h':[]} # AKA. Zc and Zl in the report
		self.__groups = None

		f = open(name, "r")

		grid = f.read().split("\n")
		f.close()
		if grid[0] == "grid":
			self.__readGrid(grid[1:])
		else :
			print("Invalid format (the first line '"+grid[0]+"' correspond to no used format)")

	def mkGroups(self) :
		nbGroups = 0
		self.__groups = [[None for i in range(self.__l)] for j in range(self.__h)]
		for i in range(self.__l):
			for j in range(self.__h):
				if (self.__groups[j][i] == None):
					nbGroups += 1
					self.__addToGrp(i,j,nbGroups)


		#return self #-> à décommenter si la valeur de retour est utilisée

	def getBarrier(self,i,j,o):
		if not(0 <= i < self.__l) or not(0 <= j < self.__h) : # Oui c'est autorisé en python xD
			raise KeyError("La case de coordonées ("+str(i)+","+str(j)+") n'existe pas.")

		if (o == NORD) :
			if (j == self.__h-1) : return True # Si on regarde la ligne tout en haut, forcément une "barriere" au dessus
			return (self.__barrier["h"][self.__h-2-j][i])

		if (o == SUD) :
			if (j == 0) : return True # Si on regarde la ligne tout en bas, forcément une "barriere" en dessous
			return (self.__barrier["h"][self.__h-1-j][i])
			
		if (o == EST) :
			if (i == self.__l -1) : return True # Si on regarde la colone tout à droite, forcément un "barrière" à droite
			return (self.__barrier["v"][self.__h-1-j][i])
			
		if (o == OUEST) :
			if (i == 0) : return True # Si on regarde la colone tout à gauche, forcément une "barrière" à gauche
			return (self.__barrier["v"][self.__h-1-j][i-1])
			
				
	def getGrid(self):
		res = "grid\n  " + ("_ " * self.__l) + "\n"
		for y in range(self.__h):
			res += str(self.__values['h'][y]) if self.__values['h'][y] != -1 else " "
			res += '|'
			for x in range(self.__l):
				res += '_' if y == self.__h-1 or self.__barrier['h'][y][x] else ' '
				res += '|' if x == self.__l-1 or self.__barrier['v'][y][x] else ' '
			res += "\n"
		res += "  " + " ".join(str(x) if x != -1 else " " for x in self.__values['v'])
		return res

	###################### Private methods ######################

	def __readGrid(self, textLines):
		for line in textLines:
			#print(line)
			line = line.split("#")[0]    # We don't take in accout the comments
			if len(line) == 0: continue  # If the line is empty, we can skip it
			if line[:2] == "  ":         # if the line starts by two spaces, it is either the first or last line
				if line[2] == '_':       # It is the first line
					self.__l = len(line.split())
				else :                      # It is the last line, so it has the vertical values
					self.__values["v"] = [-1 if line[x] == ' ' else int(line[x]) for x in range(2,len(line), 2)]

			else : # it is a regular line 
				barrier = {"v":[], "h":[]}
				self.__values["h"].append(-1 if line[0] == " " else int(line.split("|")[0]))
				for i in range(2, len(line), 2):

					if line[i] == '_':
						barrier["h"].append(True)
					else :
						barrier["h"].append(False)

					if i != len(line)-2 : 
						if line[i+1] == '|':
							barrier["v"].append(True)
						else :
							barrier["v"].append(False)

				self.__barrier["h"].append(barrier["h"])
				self.__barrier["v"].append(barrier["v"])

		self.__barrier["h"].pop()
		self.__h = len(self.__barrier["v"])

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
	
	def __str__(self):
		return "("+str(self.__l)+"x"+str(self.__h)+" grid)"

	def __repr__(self):
		return self.__str__()
