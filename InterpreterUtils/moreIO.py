class CaughtError(Exception):
	pass

class MoreIO:
	caught = CaughtError
	@staticmethod
	def title(width = 74):
		MoreIO.printLines([
			"="*width,
			' '*(int((width-56)/2))+"Welcome to our INF432 project's command line interpreter",
			"="*width,
			"",
			"Project of Eliezer Gwennan, Gansel Antoine and Boucherat Pacôme",
			"Interpreter made by Gwennan",
			""
		], width = width)

	@staticmethod
	def printWidth(*elements, width = None, sep = " ", indent = "", ws = " ", end = "\n"):
		if width == None: return print(*elements, sep = " ", end = end)
		remaining = sep.join(str(x) for x in elements).split(ws)
		line = remaining[0]
		for word in remaining[1:]:
			if line != indent and line != "" and (len(line) + len(word) + len(ws)) > width:
				print(line, end = "\n")
				line = indent + word
			else: line += ws + word
		print(line, end = end)

	@staticmethod
	def printLines(lines, sep = " ", width = None, indent1 = "", indent2 = "", ws = " ", end = "\n"):
		for l in lines:
			if type(l) in [list, tuple]:
				l = l.copy()
				l[0] = indent1 + str(l[0])
				MoreIO.printWidth(*l, sep = sep, ws = ws, indent = indent2, end = end, width = width)
			else :
				MoreIO.printWidth(indent1+str(l), sep = sep, ws = ws, indent = indent2, end = end, width = width)
	
	@staticmethod
	def readCommand(commands, prompt, error = 'Error : command {} is unknown', width = None, shortcut = False, haveArgs = True):
		while True:
			MoreIO.printWidth(prompt, width = width, end = "")
			cmd = input().strip()
			print()
			if haveArgs : cmd = cmd.split(" ",1)
			try :
				f = commands[cmd[0] if haveArgs else cmd]
			except KeyError as e:
				if haveArgs and cmd[0] != "":
					MoreIO.printWidth(error.replace("{}", cmd[0]), width = width)
				elif (not haveArgs) and cmd != "":
					MoreIO.printWidth(error.replace("{}", cmd), width = width)
			else:
				try:
					return f(cmd[1] if len(cmd) > 1 else "") if haveArgs else f()
				except MoreIO.caught as e:
					MoreIO.printWidth(e, width = width)
					return False
				except Exception as e:
					MoreIO.printWidth("An uncaught error Occured !", width = width)
					raise(e)
	
	@staticmethod
	def readNum(prompt, isFloat = True, error = "Error : the input should be a number.", width = None, hasText = False, specials = {}):
		def check(n) :
			if n in specials : return specials[n]
			else : return float(n) if isFloat else int(n)
	
		while True:
			MoreIO.printWidth(prompt, width = width)
			num = input().strip().split(" ",1)
			if num[0] == "":
				continue
			try:
				if hasText:
					num.append("")
					return (check(num[0]),(num)[1]) 
				else :
					if len(num) > 1: raise ValueError(error.replace("{}", " ".join(num)))
					return check(num[0])
			except ValueError as e:
				print(error.replace("{}", " ".join(num)))

	def __repr__(self):
		return "<object 'moreIO'>"

	@staticmethod
	def __repr__():
		return "<object 'moreIO'>"
