class Grid:

	groups = []
	def __init__(self, name):
		self.l = 0
		self.h = 0
		self.barrier  = {'v':[], 'h':[]} # AKA. Bc and Bl in the report
		self.values = {'v':[], 'h':[]} # AKA. Zc and Zl in the report
		self.groups = None

		f = open(name, "r")

		grid = f.read().split("\n")
		f.close()
		if grid[0] == "grid":
			self.readGrid(grid[1:])
		else :
			print("Invalid format (the first line '"+grid[0]+"' correspond to no used format)")

	def readGrid(self, textLines):
		for line in textLines:
			#print(line)
			line = line.split("#")[0]       # We don't take in accout the comments
			if len(line) == 0: continue     # If the line is empty, we can skip it
			if line[:2] == "  ":            # if the line starts by two spaces, it is either the first or last line
				if line[2] == '_':          # It is the first line
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


	def mkGroups(self) :
		for i in range(self.l):
			for j in range(self.h):
				pass
				
	def get_grid(self):
		res = " " + ("_ " * self.l) + "\n"
		for y in range(self.h):
			res += str(self.values['h']) if self.values['h'] != -1 else " "
			res += '|'
			for x in range(self.l):
				res += '_' if y == self.h-1 or self.barrier['h'][y][x] else ' '
				res += '|' if x == self.l-1 or self.barrier['v'][y][x] else ' '

	def __str__(self):
		return "("+str(self.l)+"x"+str(self.h)+" grid)"

	def __repr__(self):
		return self.__str__()