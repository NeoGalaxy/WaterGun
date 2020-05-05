import InterpreterUtils as Utils
import InterpreterUtils.moreIO as mio
import os
import subprocess
from Classes import *

grids = {}
current = None
currentName = ""
config = Utils.Config()

def iolist(arg):
	arg = arg.lstrip()
	if len(grids) == 0 :
		raise mio.caught('No Loaded Grid.')
	else:
		print("Loaded grids :")
		for k in grids:
			print(" -> " if grids[k] == current else "    ",k,":",grids[k])
	if (arg != "") : 
		print("\nWarning : the '{}' in the command has been ignored.".format(arg))

def load(arg):
	global current
	global currentName
	args = arg.lstrip().split(" ",1)
	fname = args[0]
	if fname == "":
		nameLength = 0
		files = []
		for f in os.scandir(config["gridsPath"]) :
			if os.path.isfile(os.path.join(config["gridsPath"], f)) :
				continue
			f = f.name
			files.append(f)
			if nameLength < len(f):
				nameLength = len(f)

		print("\Files available : ")
		lineLen = 0
		for f in files:
			if lineLen > 0 and lineLen+nameLength > config["width"]:
				print()
				lineLen = 0
			print(f," "*(nameLength-len(f)), end = " ")
			lineLen += nameLength+1
		print()
		fname = input("\nWhich file would you like to open?\n").strip()

	try:
		f = open(os.path.join(config["gridsPath"], fname)) 
		newGrid = Grid(f)
		f.close()
	except FileNotFoundError as e:
		raise mio.caught("Error : file not found")
	except ValueError as e:
		raise mio.caught(str(e))
	else : 
		gname = args[1] if len(args) > 1 else input("Give the grid a name : \n").strip()
		grids[gname] = newGrid
		print("The loading ended successfully!")
		if args[0] == "": 
			print("Note : next time you can write the command 'load {} {}' to make this same loading.".format(fname, gname))
		current = grids[gname]
		currentName = gname

def switch(arg):
	arg = arg.lstrip()
	global current
	newGrid = arg
	if newGrid == "":
		iolist("")
		newGrid = input("\nWhich is the name of the grid to switch to ?\n").strip()
	try:
		current = grids[arg]
	except KeyError as e:
		raise mio.caught("Grid not found.")

def ioprint(arg):
	print("Here is the grid :")
	print(current.getGrid().split('\n',1)[1])

def export(arg, ask = True):
	arg = arg.lstrip()
	fname = arg
	if fname == "": fname = input("\nIn which file would you like to write the output ?\n").strip()
	if not fname.endswith(".svg"): fname += ".svg"

	if ask and os.path.isfile(os.path.join(config["svgOutPath"], fname)) :
		print("Warning : There already exists a file named",fname, end = ".\n")
		exit = "n" == mio.readCommand({
			"y": lambda: "y",
			"n": lambda: "n"
		}, "Rewrite the file ? (y/n)\n", error = 'Enter "y" or "n".', haveArgs = False)
		if exit:
			print("Aborting")
			return

	try:
		f = open(os.path.join(config["svgOutPath"], fname), "w") 
		current.solToSvg([],f)
		f.close()
	except ValueError as e:
		raise mio.caught(str(e))
	else :
		print("Export done successfully.")
		openFile = "y" == mio.readCommand({
			"y": lambda: "y",
			"n": lambda: "n"
		}, "Do you want to open the file ? (y/n)\n", error = 'Enter "y" for yes or "n" for no.', haveArgs = False)
		if openFile:
			cmd = [config["openSvg"], os.path.join(config["svgOutPath"], fname)]
			subprocess.Popen(cmd,stdin=None, stdout=None, stderr=None, close_fds=True)


def solve(arg, ask = True):
	global current
	if current == None :
		raise mio.caught('No Loaded Grid.')
	s = current.getSolution()
	if s == "UNSAT":
		raise mio.caught("The grid has no solution")

	arg = arg.lstrip()
	fname = arg
	if fname == "": fname = input("\nIn which file would you like to write the output ?\n").strip()
	if not fname.endswith(".svg"): fname += ".svg"

	if ask and os.path.isfile(os.path.join(config["svgOutPath"], fname)) :
		print("Warning : There already exists a file named",fname, end = ".\n")
		exit = "n" == mio.readCommand({
			"y": lambda: "y",
			"n": lambda: "n"
		}, "Rewrite the file ? (y/n)\n", error = 'Enter "y" or "n".', haveArgs = False)
		if exit:
			print("Aborting")
			return

	try:
		f = open(os.path.join(config["svgOutPath"], fname), "w") 
		current.solToSvg(s,f)
		f.close()
	except ValueError as e:
		raise mio.caught(str(e))
	else :
		print("Export done successfully.")
		openFile = "y" == mio.readCommand({
			"y": lambda: "y",
			"n": lambda: "n"
		}, "Do you want to open the file ? (y/n)\n", error = 'Enter "y" for yes or "n" for no.', haveArgs = False)
		if openFile:
			cmd = [config["openSvg"], os.path.join(config["svgOutPath"], fname)]
			subprocess.Popen(cmd,stdin=None, stdout=None, stderr=None, close_fds=True)

def iohelp(arg):
	allHelps = {
		"list" : ("","List the loaded grids"),
		"load" : (" <file> <name>","Load the specified file in the Grids directory specified in the configurations and use it as current grid. If no file or name is specified, they will be asked."),
		"switch" : (" <name>","Switch the current grid with the specified name. If no name is specified, it will be asked."),
		"print" : ("","Prints a representation of the grid."),
		"export" : ("","Export a representation of the grid in SVG."),
		"solve" : (" <file>","Exports a solution of the current grid into the specified file. If no file is specified, it will be asked."),
		"config" : ("","Edit the configurations."),
		"help" : ("","Print this help."),
		"exit" : ("","Exit the program.")
	}
	
	print("Available commands :")
	for cmd in allHelps:
		out = " -> "+cmd+allHelps[cmd][0]+" :"
		print(out)
		indend = "      "
		out = indend
		for word in allHelps[cmd][1].split(" "):
			if len(out) + len(word) + 1 > config["width"]:
				print(out)
				out = indend
			out += " "+word
		print(out)

commands = {
	"list" : iolist,
	"load" : load,
	"switch" : switch,
	"print" : ioprint,
	"export" : export,
	"solve" : solve,
	"config" : config.edit,
	"help" : iohelp,
	"exit" : lambda x: True
}

mio.title()
def main():
	while mio.readCommand(commands, "What do you want to do ? ('help' : list the commands)\n") != True:
		print()
		if current != None : print("Current grid :", currentName, current)
try:
	main()
	print("Note : Run the function 'main()' to go back in the interpreter")
except Exception as e:
	print("=========================================================================")
	print("=======> Run the function 'main()' to go back in the interpreter <=======")
	print("=========================================================================")
	raise e