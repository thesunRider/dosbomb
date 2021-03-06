import sys,glob,configparser,importlib,os
sys.path.append('./modules/general/')


class plugin_dosbomb:
	plugin_data = {"plugin_name" : "Simple Plugin inside","plugin_version" :"1.00",
					"plugin_author" : "Suryasaradhi","plugin_date" : "18/08/2020" ,
					"plugin_linked_cnf" : False,"plugin_tree" : ''}
	run = False

	def suspend(self):
		print("Suspend current process")

	def start(self):
		print("Process start")

	def gui(self,guihandl):
		print("GUI plugins call")




class loader_plugin:
	def __init__(self, plugins = []):
		self.internal_modules = [plugin_dosbomb()]
		self._plugins = plugins

	def run(self):
		modules_to_execute = self.internal_modules + self._plugins
		for module in modules_to_execute:
			module.process()

	def load_plugin(self,file_cnf):
		config = configparser.RawConfigParser()
		config.read(file_cnf)
		details_dict = dict(config.items('plugin'))
		plugin_filename = details_dict['plugin_file']
		plugin_class = details_dict['plugin_class']
		path, file = os.path.split(file_cnf)
		spec = importlib.util.spec_from_file_location("Plugin."+plugin_class,path + "/" + plugin_filename)
		module = importlib.util.module_from_spec(spec)
		sys.modules[spec.name] = module
		spec.loader.exec_module(module)		
		plg1 = module.plugin_dosbomb()
		self._plugins.append(plg1)
		self._plugins = list(dict.fromkeys(self._plugins))
		return plg1


	def list_plugin(self):
		return self.internal_modules + self._plugins

	def getdetail_plugin(self,loc='./modules/'):
		files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(loc) for f in filenames if os.path.splitext(f)[1] == '.cnf']
		print(files)
		config = configparser.RawConfigParser()
		return_ary = []
		for x in files:
			config.read(x)
			fle = ('plugin_dir',x)
			ktms = config.items('plugin')
			ktms.append(fle)
			details_dict = dict(ktms)
			return_ary.append(details_dict)
		return return_ary 

	def loadall_plugin(self,loc='./modules/'):
		lst_plugs = self.getdetail_plugin(loc)
		for x in lst_plugs:
			plugin_filename = x['plugin_file']
			plugin_class = x['plugin_class']
			path, file = os.path.split(x['plugin_dir'])
			spec = importlib.util.spec_from_file_location("Plugin."+plugin_class, path + "/" + plugin_filename)
			#print(spec)
			module = importlib.util.module_from_spec(spec)
			sys.modules[spec.name] = module
			spec.loader.exec_module(module)		
			plg1 = module.plugin_dosbomb()
			if x['plugin_internal']:
				self.internal_modules.append(plg1)
			else :
				self._plugins.append(module)
		
		self.internal_modules = list(dict.fromkeys(self.internal_modules))
		self._plugins = list(dict.fromkeys(self._plugins))
		return self._plugins + self.internal_modules

#tst = loader_plugin()
#x = tst.getdetail_plugin()
#print(x)
#k = tst.loadall_plugin()
#print(k[1].plugin_name)





