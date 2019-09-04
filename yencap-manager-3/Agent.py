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

from ping import Pinger
from ping6 import *
import sys, string
from Constants import C
from Ft.Xml.Domlette import NonvalidatingReader, PrettyPrint
from xml.dom import Node

import re


class Agent:

	def __init__(self, ip, protocol, publicKey="", publicKeyType="", version=4, groups = [], capabilities = []):
		self.ip = ip
		self.version = version
		self.protocol = protocol
		self.publicKey = publicKey
		self.publicKeyType = publicKeyType
		#self.subsystem = "netconf"
		# status: "unreachable" (default), "reachable"
		self.status = "unreachable"
		#self.refreshStatus()
		self.groups = groups
		self.capabilities = capabilities
		
		# manu 16/9/9
		
		self.yangcapabilities =[]
		self.yangmodules = []
		self.xpaths = {}
		self.namespaces = {}
		self.globalnamespaces = {}
		self.yangOk = True
		self.yangErrors = ""
		
		# manu 16/9/9
		
	def getIp(self):
		return self.ip
		
	def getVersion(self):
		return self.version

	def getProtocol(self):
		return self.protocol

	def getPublicKeyType(self):
		return self.publicKeyType

	def getPublicKey(self):
		return self.publicKey

	#def getSubsystem(self):
	#	return self.subsystem

	def getStatus(self):
		return self.status

	def setStatus(self, status):
		self.status = status

	def refreshStatus(self):
		self.status = self.ping()

	def ping(self):
		if self.version == 6:
			res = Pinger6().ping6([self.ip]).results
		else:
			res = Pinger().ping([self.ip]).results
		if res == {}:
			return "unreachable"
		else:
			return "reachable"

	def getCapabilities(self):
		return self.capabilities

	def setCapabilities(self, capabilities):
		self.capabilities = []
		doc = NonvalidatingReader.parseString(capabilities.strip(), 'http://madynes.loria.fr')
		helloNode = doc.documentElement
		if helloNode.tagName == C.HELLO:
			for capabilitiesNode in helloNode.childNodes:
				if (capabilitiesNode.nodeType == Node.ELEMENT_NODE and capabilitiesNode.tagName == C.CAPABILITIES):
					for capabilityNode in capabilitiesNode.childNodes:
						if (capabilityNode.nodeType == Node.ELEMENT_NODE and capabilityNode.tagName == C.CAPABILITY):
							txtvalue = string.strip(str(capabilityNode.childNodes[0].nodeValue))
							if not txtvalue in self.capabilities:
								self.capabilities.append(txtvalue)
		
		self.setYangModules()
								
	def setYangModules(self):
		self.yangcapabilities = []
		for cap in self.capabilities:
			modulecapab = re.split('\?', cap)
			if len(modulecapab) == 2:
				modulerefs = re.split('&',modulecapab[1])
				if len(modulerefs) > 0:
					item = re.split('=', modulerefs[0])
					if len(item) > 1:
						if item[0] == "module":
							modulename = item[1]
							self.yangmodules.append(modulename)
							self.yangcapabilities.append(cap)
				    
		
	def isYangOk(self):
		return self.yangOk
						
	def setYangErrMesg(self, errors):
		self.yangErrors = errors
		if errors != "":
			self.yangOk = False
		
	def getYangErrMesg(self):
		return self.yangErrors

	def isYangEnabled(self):
		return self.hasYangModule() and self.yangOk
	
	def hasYangModule(self):
		return len(self.yangcapabilities) != 0 
