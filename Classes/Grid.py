class Direction:
	NORD = 0
	SUD = 1
	EST = 2
	OUEST = 3


class Grid:

	groups = []
	def __init__(self, name):
		self.l = 0
		self.h = 0
		self.barrier  = {'v':[], 'h':[]} # AKA. Bc and Bl in the report
		self.values = {'v':[], 'h':[]} # AKA. Zc and Zl in the report
		self.groups = {}

		f = open(name, "r")

		grid = f.read().split("\n")
		f.close()
		if grid[0] == "grid":
			self.__readGrid(grid[1:])
		else :
			print("Invalid format (the first line '"+grid[0]+"' correspond to no used format)")

	def mkGroups(self) :
		nbGroups = 0
		for i in range(self.l):
			for j in range(self.h):
				if (self.groups.get((i,j)) == None):
					nbGroups += 1
					self.groups[(i,j)] = nbGroups
					self.addGrp(i,j)

	def addGrp(self,i,j):
		#Begin Debug#
		print(self.groups)
		#End Debug"

		if (not(self.getBarrier(i,j,Direction.NORD)) and self.groups.get((i,j+1)) == None): 
			self.groups[(i,j+1)] = self.groups.get((i,j))
			self.addGrp(i,j+1)

		if (not(self.getBarrier(i,j,Direction.SUD)) and self.groups.get((i,j-1)) == None): 
			self.groups[(i,j-1)] = self.groups.get((i,j))
			self.addGrp(i,j-1)

		if (not(self.getBarrier(i,j,Direction.EST)) and self.groups.get((i+1,j)) == None): 
			self.groups[(i+1,j)] = self.groups.get((i,j))
			self.addGrp(i+1,j)

		if (not(self.getBarrier(i,j,Direction.OUEST)) and self.groups.get((i-1,j)) == None): 
			self.groups[(i-1,j)] = self.groups.get((i,j))
			self.addGrp(i-1,j)

		return self

		def getBarrier(self,i,j,o):
			if (o==Direction.NORD) :
				if (j == self.h-1) : return True # Si on regarde la ligne tout en haut, forcément une "barriere" au dessus
				return (self.barrier.get("h")[i+1][j+1])

			if (o==Direction.SUD) :
				if (j == 0) : return True # Si on regarde la ligne tout en bas, forcément une "barriere" en dessous
				return (self.barrier.get("h")[i+1][j])
				
			if (o==Direction.EST) :
				if (i == self.l -1) : return True # Si on regarde la colone tout à droite, forcément un "barrière" à droite
				return (self.barrier.get("v")[j][i+1])
				
			if (o==Direction.OUEST) :
				if (i == 0) : return True # Si on regarde la colone tout à gauche, forcément une "barrière" à gauche
				return (self.barrier.get("v")[j][i])
				
				
	def get_grid(self):
		res = "grid\n  " + ("_ " * self.l) + "\n"
		for y in range(self.h):
			res += str(self.values['h'][y]) if self.values['h'][y] != -1 else " "
			res += '|'
			for x in range(self.l):
				res += '_' if y == self.h-1 or self.barrier['h'][y][x] else ' '
				res += '|' if x == self.l-1 or self.barrier['v'][y][x] else ' '
			res += "\n"
		res += "  " + " ".join(str(x) if x != -1 else " " for x in self.values['v'])
		return res

	###################### Private methods ######################

	def __readGrid(self, textLines):
		for line in textLines:
			#print(line)
			line = line.split("#")[0]    # We don't take in accout the comments
			if len(line) == 0: continue  # If the line is empty, we can skip it
			if line[:2] == "  ":         # if the line starts by two spaces, it is either the first or last line
				if line[2] == '_':       # It is the first line
					self.l = len(line.split())
				else :                      # It is the last line, so it has the vertical values
					self.values["v"] = [-1 if line[x] == ' ' else int(line[x]) for x in range(2,len(line), 2)]

			else : # it is a regular line 
				barrier = {"v":[], "h":[]}
				self.values["h"].append(-1 if line[0] == " " else int(line.split("|")[0]))
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

				self.barrier["h"].append(barrier["h"])
				self.barrier["v"].append(barrier["v"])

		self.barrier["h"].pop()
		self.h = len(self.barrier["v"])

	def __str__(self):
		return "("+str(self.l)+"x"+str(self.h)+" grid)"

	def __repr__(self):
		return self.__str__()
