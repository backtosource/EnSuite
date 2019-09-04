###############################################################################
#                                                                             #
# YencaP software, LORIA-INRIA LORRAINE, MADYNES RESEARCH TEAM                #
# Copyright (C) 2005  Vincent CRIDLIG                                         #
#                                                                             #
# This library is free software; you can redistribute it and/or               #
# modify it under the terms of the GNU Lesser General Public                  #
# License as published by the Free Software Foundation; either                #
# version 2.1 of the License, or (at your option) any later version.          #
#                                                                             #
# This library is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU           #
# Lesser General Public License for more details.                             #
#                                                                             #
# You should have received a copy of the GNU Lesser General Public            #
# License along with this library; if not, write to the Free Software         #
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA   #
#                                                                             #
# Author Info:                                                                #
#   Name : Humberto ABDELNUR and Vincent CRIDLIG                              #
#   Email: Humberto.Abdelnur@loria.fr, Vincent.Cridlig@loria.fr               #
#                                                                             #
###############################################################################


import string, os, time, array, syslog
from Ft.Xml.Domlette import NonvalidatingReader, implementation, PrettyPrint
from Ft.Xml import XPath, EMPTY_NAMESPACE
from xml.dom import Node
from Constants import C
from Ft.Xml.XPath import Evaluate
from Ft.Xml.XPath.Context import Context
import traceback
import LogManager
import amara


class ModuleManager:
	"""
		ModuleManager is responsible for:
			- parsing the modules.xml file,
			- storing the info of modules
	"""

	instance = None

	def __init__(self):

		# Instantiate the module list
		self.modules = {}
		self.prefixes = {"ycp":C.YENCAP_XMLNS}

		# Parse the modules info from the modules.xml file
		self.parseModules()
		
	
	def parseModules(self):
		try:

			doc = amara.parse('file:%s/modules.xml'%(C.YENCAP_MAN_CONF_HOME))

			for elem in doc.modules.module:
				name = str(elem.name)+"_Module"
				xpath = str(elem.xpath)
				namespace = str(elem.namespace)
				pref = str(elem.namespace.pref)
				self.prefixes[pref] = namespace
				self.modules[name] = {"xpath" : xpath , "namespace" : namespace}

		except Exception, exp:
			print 'Error while reading %s/modules.xml : %s' %(C.YENCAP_MAN_CONF_HOME, str(exp))


	def getModuleInstance(self, name, httpSession):
		
		# Now trying to load the module:
		newModule = None

		try:
			# Build an instance of the module (like BGP module for instance) 
			# with a dictionnary containing the parameters defined in modules.xml (__init__)
			mod = self.modules[name]
			modz = self.importName("Components.Modules." + name +"."+name, name)
			newModule = modz(name, mod["xpath"], mod["namespace"], httpSession.session_id)
			
			LogManager.getInstance().logInfo("module %s has been loaded successfully." % (name))

		except Exception, exp:
			traceback.print_exc()
			LogManager.getInstance().logInfo("module %s couldn't be loaded. Error:%s" % (name, str(exp)))
			return None

		return newModule


	def getPrefixes(self):
		return self.prefixes


	def importName(self, modulename, name):
		""" Import a named object from a module in the context of this function,
			which means you should use fully qualified module paths.
			
			Return None on failure.
		"""
		try:
			module = __import__(modulename, globals(), locals(), [name])
		except ImportError:
			return None

   		return vars(module)[name]


def getInstance():
	"""
	ModuleManager is a Singleton
	Use getInstance method to get the unique ModuleManager
	
	@rtype: ModuleManager
	@return: The ModuleManager instance itself (which is unique).
	"""
	
	if ModuleManager.instance == None:
		ModuleManager.instance = ModuleManager()
	return ModuleManager.instance
