import json
from .moreIO import MoreIO as mio

class Config:
	config = {}
	usr = {}
	configPath = "InterpreterUtils/config.json"
	userPath = "InterpreterUtils/config-usr.json"
	options = ["gridsPath","svgOutPath","openSvg","width"]
	optDescr = {
		"gridsPath": "Path to the grids to read in grid1 format",
		"svgOutPath": "Path to which the svg files are exported",
		"openSvg": "Command to display the svg file",
		"width": "Number of characters that can fit on the screen"
	}

	def __init__(self):
		if self.config == {} : self.load()

	@staticmethod
	def load():
		f = open(Config.configPath)
		content = json.load(f)
		if set(Config.options).difference(content) != set():
			f.close
			raise ValueError("The config.json file is corrupted")
		Config.config = content
		f.close()
		f = open(Config.userPath)
		Config.usr = json.load(f)
		f.close()

	@staticmethod
	def save():
		f = open(Config.userPath, "w")
		json.dump(Config.usr, f, indent = "\t")
		f.close()

	@staticmethod
	def edit(arg=""):
		while True:
			print("Available options :")
			optWidth = max(len(Config.optDescr[o]) for o in Config.options)
			for i in range(len(Config.options)):
				o = Config.options[i]
				indent = (optWidth-len(Config.optDescr[o]))
				print(" "+str(i+1)+": "+" "*(int(indent/2))+Config.optDescr[o]+" "*(indent-int(indent/2)),":", repr(Config.get(o)))
			print()
			print("Type 'q' to quit configurations editing.")
			(opt,txt) = mio.readNum("What option would you like to edit ? (1/2/3/4/q)\n",
				False,'Error : You should enter an index', hasText = True, specials={"q":None})
			if opt == None: break
			Config.editOpt(Config.options[opt-1],txt)
		Config.save()
		print("Saved configuration")


	@staticmethod
	def editOpt(o, arg):
		if arg.strip() == "":
			print("\nYou are editing the",repr(Config.optDescr[o]), end = ".\n")
			arg = input("What is the new value for this option ? (old : "+repr(Config.get(o))+")\n")
		argtype = type(Config.get(o))
		Config.usr[o] = argtype(arg)
		print("\nThe",repr(Config.optDescr[o]),"has been set to",repr(Config.get(o)),"\n")

	@staticmethod
	def get(arg):
		ret = Config.usr.get(arg)
		return ret if ret != None else Config.config.get(arg)

	def __getitem__(self, arg):
		ret = Config.usr.get(arg)
		return ret if ret != None else Config.config[arg]

	def __setitem__(self, key, value):
		Config.usr[key] = value