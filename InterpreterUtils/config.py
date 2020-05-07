import json
import os
from .moreIO import MoreIO as mio
printw = mio.printWidth

class Config:
	config = {}
	usr = {}
	configPath = "InterpreterUtils/config.json"
	userPath = "InterpreterUtils/config-usr.json"
	options = ["gridsPath","svgOutPath","askConfirm", "restart","openSvg","width"]
	optDescr = {
		"gridsPath": ("path to the grids to read in grid1 format", ""),
		"svgOutPath": ("path to which the svg files are exported", ""),
		"askConfirm": ("ask before rewriting a file", "Activate this option if you want a confirmation before rewriting a file."),
		"restart": ("automatically restart the 'next' command", "When activated, this option automatically asks a new solution when the 'next' has no more solution."),
		"openSvg": ("command to display the svg file", ""),
		"width": ("number of characters that can fit on the screen", "If set to 0, the width will be dynamically queried form the terminal informations")
	}

	def __init__(self):
		if self.config == {} : self.load()

	@staticmethod
	def load():
		content = {"gridsPath": "Grids/Probs","svgOutPath": "Outputs","askConfirm": True,"restart": False,"openSvg": "eog","width": 0,"defaultWidth": 100}
		Config.config = content

		try:
			f = open(Config.userPath)
			Config.usr = json.load(f)
			f.close()
		except Exception as e:
			Config.usr = {}
		try:
			os.get_terminal_size()
		except OSError as e:
			printw("/!\\ The terminal's width could not be found. If width is set to 0.", width = Config.get("width"))
			printw("     It will be considered as being",Config.get("defaultWidth"),"/!\\")
	@staticmethod
	def save():
		try:
			f = open(Config.userPath, "w")
			json.dump(Config.usr, f, indent = "\t")
			f.close()
			printw("Saved configuration.", width = Config.get("width"))
		except Exception as e:
			printw("An error occurred during save:",e)
			printw("The user configuration will not be saved.")

	@staticmethod
	def edit(arg=""):
		while True:
			printw("Available options :", width = Config.get("width"))
			optWidth = max(len(Config.optDescr[o][0]) for o in Config.options)
			for i in range(len(Config.options)):
				o = Config.options[i]
				indent = (optWidth-len(Config.optDescr[o][0]))
				if type(Config.get2(o)) == bool:
					optVal = "Enabled" if Config.get2(o) else "Disabled"
				else :
					optVal = repr(Config.get2(o))
				printw(" "+str(i+1)+": "+" "*(int(indent/2))+Config.optDescr[o][0]+" "*(indent-int(indent/2))+":", optVal, width = Config.get("width"))
			print()
			printw("Type 'q' to quit configurations editing.", width = Config.get("width"))
			(opt,txt) = mio.readNum("What option would you like to edit ? (1/2/3/4/5/q)\n",
				False,'Error : You should enter an index', hasText = True, specials={"q":None})
			if opt == None: break
			Config.editOpt(Config.options[opt-1],txt)
		Config.save()


	@staticmethod
	def editOpt(o, arg):
		if arg.strip() == "":
			printw("\nYou are editing the",repr(Config.optDescr[o][0]), "option", end = ".\n", width = Config.get("width"))
			printw(Config.optDescr[o][1], width = Config.get("width"))
			if type(Config.get2(o)) == bool:
				optVal = "Enabled" if Config.get2(o) else "Disabled"
			else :
				optVal = repr(Config.get2(o))
			if type(Config.get2(o)) == bool:
				arg = mio.readCommand({"y": lambda: 1,"n": lambda: 0, "": lambda: ""}, "Do you want to activate this option? (y/n)\n", error = 'Enter "y" or "n".', haveArgs = False, width = Config.get("width"))
			else :
				arg = input("What is the new value for this option ? (old : "+optVal+")\n")
		if arg != "":
			argtype = type(Config.get(o))
			Config.usr[o] = argtype(arg)
			printw("\nThe",repr(Config.optDescr[o][0]),"option has been set to",repr(Config.get(o)),"\n", width = Config.get("width"))
		else : printw("\nThe",repr(Config.optDescr[o][0]),"option remains unchanged\n", width = Config.get("width"))

	@staticmethod
	def get(arg):
		try:
			return Config.__getitem__(None, arg)
		except Exception as e:
			return None

	@staticmethod
	def get2(arg):
		ret = Config.usr.get(arg)
		return ret if ret != None else Config.config.get(arg)

	def __getitem__(self, arg):
		ret = Config.usr.get(arg)
		if ret == None : ret = Config.config[arg]
		if ret == 0 and arg == "width": 
			try:
				ret = os.get_terminal_size().columns
			except OSError as e:
				ret = Config.get("defaultWidth")
		return ret

	def __setitem__(self, key, value):
		Config.usr[key] = value