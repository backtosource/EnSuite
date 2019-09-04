###############################################################################
#                                                                             #
# YencaPManager software, LORIA-INRIA LORRAINE, MADYNES RESEARCH TEAM         #
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
# Modified by:                                                                #
#   Name : Frederic Beck                                                      #
#   Email : Frederic.Beck@loria.fr                                            #
#                                                                             #
###############################################################################

from Ft.Xml.Domlette import NonvalidatingReader, PrettyPrint
from Ft.Xml.XPath import Evaluate
from Ft.Xml import EMPTY_NAMESPACE
from Agent import Agent
from Constants import *
from User import User
import string
import amara

class Parser:

	instance = None	
	
	def __init__(self):
		self.agents = []
		self.users = []

		self.parseAgents()
		self.parseUsers()
		self.parseServer()


	def getAgents(self):
		return self.agents

	def getUsers(self):
		return self.users

	def getServer(self):
		return self.host, self.port


	def parseAgents(self):
		try:
			doc = amara.parse("file:" + C.YENCAP_MAN_CONF_HOME + "/agents.xml") 

			for elem in doc.agents.agent:
				protocol = str(string.strip(elem.type))
				version = int(elem.ipaddress.type)
				adr = str(elem.ipaddress)
				publicKeyType = str(string.strip(elem.publickey.type))
				publicKey = str(elem.publickey)
				groups = []
				for item in elem.groups.group:
					groups.append(item.ref)
				capabilities = []
				for item in elem.capabilities.capability:
					capabilities.append(item.ref)

				agent = Agent(adr , protocol, publicKey, publicKeyType, version, groups, capabilities)
				self.agents.append(agent)

		except Exception, exp:
			print 'Check configuration file of the server : agents.xml'
			print str(exp)


	def parseUsers(self):
		try:
			doc = amara.parse('file:%s/users.xml'%(C.YENCAP_MAN_CONF_HOME))
			for elem in doc.users.user:
				privateKeyFile = None
				privateKeyType = None
				login = str(elem.login)
				password = str(elem.password)
				pref_nb_devices_per_page = int(str(elem.devicesperpage))
				try:
					privateKeyFile = str(elem.privatekeyfile)
					privateKeyType = str(elem.privatekeyfile.type)
				except Exception, exp:
					pass
				user = User(login , password, privateKeyFile, privateKeyType, pref_nb_devices_per_page)
				self.users.append(user)
		except Exception, exp:
			print 'Check configuration file of the server : users.xml'
			print str(exp)
			

	def parseServer(self):
		try:
			doc = amara.parse('file:%s/config.xml'%(C.YENCAP_MAN_CONF_HOME))
			self.host = ''
			self.port = int(str(doc.server.port))
			self.ip_version = str(doc.server.ip_version)
		except Exception, exp:
			print 'Check configuration file of the server : config.xml'
			print str(exp)
		
	
	
	def saveDoc(self):
		"""
			Save the XML configuration file to disk.
		"""
		f = open(C.CONFIG_FILE,'w')
		PrettyPrint(self.agents,f)
		f.close()
		
# Singleton : only one instance of the Parser
def getInstance():
	if Parser.instance == None:
		Parser.instance = Parser()
	return Parser.instance

