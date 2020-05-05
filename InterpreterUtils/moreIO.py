class CaughtError(Exception):
	pass

class MoreIO:
	caught = CaughtError
	@staticmethod
	def title():
		MoreIO.printLines([
			"==========================================================================",
			"======   Welcome to our INF432 project's command line interpreter   ======",
			"==========================================================================",
			"Project of Eliezer Gwennan, Gansel Antoine and Boucherat Pacôme",
			"Interpreter made by Gwennan",
			""
		])

	@staticmethod
	def printLines(lines, sep = " "):
		for l in lines:
			if type(l) in [list, tuple]:
				print(*l, sep = " ")
			else :
				print(l, sep = " ")
	
	@staticmethod
	def readCommand(commands, prompt, error = 'Error : command {} is unknown', shortcut = False, haveArgs = True):
		while True:
			cmd = input(prompt).strip()
			print()
			if haveArgs : cmd = cmd.split(" ",1)
			try :
				f = commands[cmd[0] if haveArgs else cmd]
			except KeyError as e:
				if cmd[0] != "":
					print(error.replace("{}", cmd[0] if haveArgs else cmd))
			else:
				try:
					return f(cmd[1] if len(cmd) > 1 else "") if haveArgs else f()
				except MoreIO.caught as e:
					print(e)
					return False
				except Exception as e:
					print("An uncaught error Occured !")
					raise(e)
	
	@staticmethod
	def readNum(prompt, isFloat = True, error = "Error : the input should be a number.", hasText = False, specials = {}):
		def check(n) :
			if n in specials : return specials[n]
			else : return float(n) if isFloat else int(n)
	
		while True:
			num = input(prompt).strip().split(" ",1)
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
		return "<class 'moreIO'>"
