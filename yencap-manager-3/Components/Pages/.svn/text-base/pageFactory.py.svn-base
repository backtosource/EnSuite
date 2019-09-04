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
#   Name : Vincent CRIDLIG                                                    #
#   Email: Vincent.Cridlig@loria.fr                                           #
#                                                                             #
###############################################################################

### Cyrille CORNU - 26/08/2009
# Add "yang" to the dictionnary.

from Page import Page
import SessionManager
import re
from Components.Modules import ModuleManager

from LoginPage import LoginPage
from MainPage import MainPage
from ModulePage import ModulePage
from AgentPage import AgentPage
#from LockPage import LockPage
#from CopyPage import CopyPage
#from DeletePage import DeletePage
#from KillPage import KillPage
#from RolePage import RolePage
#from ModuleManagementPage import ModuleManagementPage
#from AgentReachablePage import AgentReachablePage
#from SubtreePage import SubtreePage
#from XpathPage import XpathPage
#from EditPage import EditPage
#from ValidatePage import ValidatePage
#from CandidatePage import CandidatePage


class PageFactory:
	"""
	
	"""

	instance = None

	def __init__(self):
		self.dictionary = {
		"/main": "MainPage",
		"/": "MainPage",
		"": "MainPage",
		"/agent": "AgentPage",
		"/modules": "ModuleManagementPage",
		"/agentreachable": "AgentReachablePage",
		"/login": "LoginPage" ,
		"/lock": "LockPage" ,
		"/copy": "CopyPage" ,
		"/delete": "DeletePage" ,
		"/kill": "KillPage" ,
		"/role": "RolePage" ,
		"/subtree": "SubtreePage" ,
		"/xpath": "XpathPage" ,
		"/edit": "EditPage" ,
		"/validate": "ValidatePage" ,
		"/candidate": "CandidatePage",
		"/close": "ClosePage",
		"/logout": "LoginPage",
		"/yang":"YangPage"}


	def importName(self, modulename, name):
		"""
			Import a named object from a module in the context of this function,
			which means you should use fully qualified module paths.
			Return None on failure.
		"""
		module = __import__(modulename, globals(), locals(), [name])
		return vars(module)[name]


	def getPage(self, path, httpSession=None, agent=None, error="", netconfReply="", info="", dictio={"filter_ip" : "Not filtered", "filter_function" : "Not filtered", "filter_status" : "Not filtered", "filter_capabilities" : "Not filtered", "page" : 1}):

		p = re.compile('/modules/')
		m = p.match(path)

		if not self.dictionary.has_key(path) and m == None:
			# for static files...
			return open(path[1:]).read()

		if dictio.has_key("page_pref") and httpSession != None:
			value = dictio["page_pref"]
			if value == "All":
				httpSession.user.pref_nb_devices_per_page = value
			else:
				httpSession.user.pref_nb_devices_per_page = int(value)

		if httpSession == None:

			page = LoginPage(httpSession, agent, error, netconfReply, info)

		else:
			
			if (m != None):
				modulename = path[m.end():]
				mManager = ModuleManager.getInstance()
				module = mManager.getModuleInstance(modulename, httpSession)
				if module != None:
					page = ModulePage(httpSession, agent, error, netconfReply, info, module)
				else:
					page = AgentPage(httpSession, agent, error+"Error while loading module "+modulename+". See /var/log/messages.", netconfReply, info)

			elif self.dictionary.has_key(path):
				className = self.dictionary[path]
				mod = self.importName(className, className)
				if path in ["/main", "/", ""]:
					page = mod(httpSession, agent, error, netconfReply, info, dictio["filter_ip"], dictio["filter_function"], dictio["filter_status"], dictio["filter_capabilities"], int(dictio["page"]))
				else:
					page = mod(httpSession, agent, error, netconfReply, info)

		return page.toString()



def getInstance():
	"""
		PageFactory is a Singleton
		Use getInstance method to get the unique PageFactory
		@rtype: PageFactory
		@return: PageFactory singleton instance
	"""

	if PageFactory.instance == None:
		PageFactory.instance = PageFactory()
	return PageFactory.instance

