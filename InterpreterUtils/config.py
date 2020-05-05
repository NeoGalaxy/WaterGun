import json

class Config:
	config = {}
	usr = {}
	configPath = "InterpreterUtils/config.json"
	userPath = "InterpreterUtils/config-usr.json"

	def __init__(self):
		if self.config == {} : self.load()

	@staticmethod
	def load():
		f = open(Config.configPath)
		Config.config = json.load(f)
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
	def edit(arg):
		raise NotImplementedError()

	def get(self, arg):
		ret = Config.usr.get(arg)
		return ret if ret != None else Config.config.get(arg)

	def __getitem__(self, arg):
		ret = Config.usr.get(arg)
		return ret if ret != None else Config.config[arg]

	def __setitem__(self, key, value):
		Config.usr[key] = value