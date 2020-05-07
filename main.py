import InterpreterUtils as Utils
import InterpreterUtils.moreIO as mio
import os
import subprocess
from Classes import *
printw = mio.printWidth

grids = {}
current = None
currentName = ""
config = Utils.Config()
def width():
	return config["width"]

def inputw(prompt):
	printw(prompt, width = width(), end = "")
	return input()

def iolist(arg):
	arg = arg.lstrip()
	print("-"*width())
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

		print("Files available : ")
		lineLen = 0
		for f in files:
			if lineLen > 0 and lineLen+nameLength > config["width"]:
				print()
				lineLen = 0
			print(f," "*(nameLength-len(f)), end = " ")
			lineLen += nameLength+1
		print()
		fname = inputw("\nWhich file would you like to open?\n").strip()

	try:
		f = open(os.path.join(config["gridsPath"], fname)) 
		newGrid = Grid(f)
		f.close()
	except (FileNotFoundError, IsADirectoryError) as e:
		raise mio.caught("Error : file '"+fname+"' not found the directory '"+config["gridsPath"]+"'\n(You can change the directory in the configurations)")
	except ValueError as e:
		raise mio.caught(str(e))
	else : 
		if len(args) > 1:
			gname = args[1]
		else :
			alter = os.path.splitext(os.path.basename(fname))[0]
			gname = inputw("Give the grid a name : (empty for "+repr(alter)+")\n").strip()
			if gname == "": gname = alter
		grids[gname] = newGrid
		print("The loading ended successfully!")
		if args[0] == "": 
			print("Note : next time you can write the command 'load {} {}' to make this same loading.".format(fname, gname))
		current = grids[gname]
		currentName = gname

def switch(arg):
	arg = arg.lstrip()
	global current
	global currentName
	newGrid = arg
	if newGrid == "":
		iolist("")
		newGrid = inputw("\nWhich is the name of the grid to switch to?\n").strip()
	try:
		current = grids[newGrid]
		currentName = newGrid
		printw("Switch done successfully", width = width())
	except KeyError as e:
		raise mio.caught("Grid "+repr(newGrid)+" not found.")

def ioprint(arg):
	print("-"*width())
	print("Here is the grid :")
	print(current.getGrid().split('\n',1)[1])

def export(arg):
	ask = config["askConfirm"]
	arg = arg.lstrip()
	print("-"*width())
	arg = arg.lstrip().split(" ",1)
	fname = arg[0]
	if fname == "": fname = inputw("\nIn which file would you like to write the output?\n").strip()
	if not fname.endswith(".svg"): fname += ".svg"

	if ask and os.path.isfile(os.path.join(config["svgOutPath"], fname)) :
		print("Warning : There already exists a file named",fname, end = ".\n")
		exit = "n" == mio.readCommand({
			"y": lambda: "y",
			"n": lambda: "n"
		}, "Rewrite the file? (y/n)\n", error = 'Enter "y" or "n".', haveArgs = False, width = width())
		if exit:
			print("Aborting")
			return

	try:
		f = open(os.path.join(config["svgOutPath"], fname), "w") 
		current.writeSvg(f,[])
		f.close()
	except ValueError as e:
		raise mio.caught(str(e))
	else :
		print("Export done successfully.")
		if len(arg) > 1:
			if not arg[1] in ["y","n"]:
				printw("Warning : the argument",repr(arg[1]),"is ignored.")
			else :
				openFile = arg[1] == "y"
		if openFile == None: 
			openFile = mio.readCommand({
				"y": lambda: True,
				"n": lambda: False
			}, "Do you want to open the file? (y/n)\n", error = 'Enter "y" for yes or "n" for no.', haveArgs = False, width = width())
		if openFile:
			cmd = [config["openSvg"], os.path.join(config["svgOutPath"], fname)]
			subprocess.Popen(cmd,stdin=None, stdout=None, stderr=None, close_fds=True)

def solve(arg, usenext = False):
	global current
	ask = config["askConfirm"]
	print("-"*width())
	if current == None :
		raise mio.caught('No Loaded Grid.')
	if usenext:
		s = current.getNextSolution()
		if s == None:
			if current.getSolution() == "UNSAT":
				raise mio.caught("The grid has no solution")
			if not config["restart"] and not mio.readCommand({"y": lambda: True,"n": lambda: False}, 
				"All the solutions of this grid have been explored. Do you want to export the first solution? (y/n)\n", error = 'Enter "y" or "n".', haveArgs = False, width = width()): 
				printw("Aborting. Note: the solutions have been reinitialized, so the next sol. will be the first one.")
				return
			s = current.getNextSolution()
	else:
		s = current.getSolution()
		if s == "UNSAT":
			raise mio.caught("The grid has no solution")

	arg = arg.lstrip().split(" ",1)
	fname = arg[0]
	if fname == "": fname = inputw("\nIn which file would you like to write the output?\n").strip()
	if not fname.endswith(".svg"): fname += ".svg"

	if ask and os.path.isfile(os.path.join(config["svgOutPath"], fname)) :
		print("Warning : There already exists a file named",fname, end = ".\n")
		exit = "n" == mio.readCommand({
			"y": lambda: "y",
			"n": lambda: "n"
		}, "Rewrite the file? (y/n)\n", error = 'Enter "y" or "n".', haveArgs = False, width = width())
		if exit:
			print("Aborting")
			return

	try:
		f = open(os.path.join(config["svgOutPath"], fname), "w") 
		current.writeSvg(f,s)
		f.close()
	except ValueError as e:
		raise mio.caught(str(e))
	else :
		print("Export done successfully.")
		openFile = None
		if len(arg) > 1:
			if not arg[1] in ["y","n"]:
				printw("Warning : the argument",repr(arg[1]),"is ignored.")
			else :
				openFile = arg[1] == "y"
		if openFile == None: 
			openFile = mio.readCommand({
				"y": lambda: True,
				"n": lambda: False
			}, "Do you want to open the file? (y/n)\n", error = 'Enter "y" for yes or "n" for no.', haveArgs = False, width = width())
		if openFile:
			cmd = [config["openSvg"], os.path.join(config["svgOutPath"], fname)]
			subprocess.Popen(cmd,stdin=None, stdout=None, stderr=None, close_fds=True)

def iohelp(arg):
	allHelps = {
		"list" : ("","List the loaded grids"),
		"load" : (" <file> <name>","Load the specified file in the Grids directory specified in the configurations and use it as current grid. If no file or name is specified, they will be asked."),
		"switch" : (" <name>","Switch the current grid with the specified name. If no name is specified, it will be asked."),
		"print" : ("","Prints a representation of the grid."),
		"export" : (" <file> <y/n>","Export a representation of the grid in SVG. The second argument should be 'y' if you wish to open the result, and 'n' otherwise. Both arguments will be asked if not specified."),
		"solve" : (" <file> <y/n>","Exports a solution of the current grid into the specified file. The second argument should be 'y' if you wish to open the result, and 'n' otherwise. Both arguments will be asked if not specified."),
		"next" : (" <file>","Same as 'solve', but with a different solution on each call."),
		"config" : ("","Edit the configurations."),
		"help" : ("","Print this help."),
		"exit" : ("","Exit the program.")
	}
	
	print("-"*width())
	print("Available commands :")
	for cmd in allHelps:
		out = "" if width() < 24 else " -> "
		indent = "     "
		printw(out+cmd+allHelps[cmd][0]+" :", width = width())
		mio.printLines([allHelps[cmd][1]], width = width(), indent1 = indent, indent2 = indent)

commands = {
	"list" : iolist,
	"load" : load,
	"switch" : switch,
	"print" : ioprint,
	"export" : export,
	"solve" : solve,
	"next" : lambda arg: solve(arg, usenext = True),
	"config" : config.edit,
	"help" : iohelp,
	"exit" : lambda _: True
}

mio.title(config["width"])
def main():
	while mio.readCommand(commands, "What do you want to do? ('help' : list the commands)\n", width = width()) != True:
		print("-"*width()+"\n")
		if current != None : printw("Current grid :", currentName, current, width = width(), indent = "    ")
try:
	main()
	printw("Note : Run the function 'main()' to go back in the interpreter")
except Exception as e:
	print("=========================================================================")
	print("=======> Run the function 'main()' to go back in the interpreter <=======")
	print("=========================================================================")
	raise e