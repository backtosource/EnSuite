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

from Operations.base.get_config_operation import Get_config_operation
from Operations.operationReply import OperationReply
from Modules.modulereply import ModuleReply
from constants import C
from xml.dom import Node
import string
from Ft.Xml.Domlette import PrettyPrint, implementation


class Get_operation(Get_config_operation):
			
	
	def getConfig(self, sourceName):

		doc = self.datastoreManager.getConfig(sourceName, "state")
		if doc == None:
			moduleReply = ModuleReply(
			error_type = ModuleReply.PROTOCOL,
			error_tag = ModuleReply.UNKNOWN_ELEMENT,
			error_severity = ModuleReply.ERROR,
			error_message = "%s configuration does not exist." % sourceName)
			self.operationReply.setError()
			self.operationReply.setNode(moduleReply.getXMLNodeReply())
			return
		else:
			self.operationReply.setNode(doc)


	def setParameters(self, operation, NSS = None):
		"""
		Set the source and filter parameters

		@type  operation: Node
		@param operation: The operation node of the current Netconf request.
		"""
		
		self.prefixes = NSS

		for child in operation.childNodes:
			if child.nodeType==Node.ELEMENT_NODE:
							
				if child.tagName == C.FILTER:
					self.filter = child
					for att in self.filter.attributes.values():
						if att.name == "type":
							if att.value == C.SUBTREE:
								self.filterType = C.SUBTREE
							elif att.value == C.XPATH:
								self.filterType = C.XPATH
							else:
								moduleReply = ModuleReply(
								error_type = ModuleReply.PROTOCOL,
								error_tag = ModuleReply.BAD_ATTRIBUTE,
								error_severity = ModuleReply.ERROR,
								error_message = "An attribute value is not correct")
								moduleReply.addErrorInfo("bad-attribute",att.name)
								moduleReply.addErrorInfo("bad-element",child.tagName)
								self.operationReply.setError()
								self.operationReply.setNode(moduleReply.getXMLNodeReply())
								return
						elif  att.name == "select":
							self.xpathrequest = att.value
						else:
							moduleReply = ModuleReply(
							error_type = ModuleReply.PROTOCOL,
							error_tag = ModuleReply.UNKNOWN_ATTRIBUTE,
							error_severity = ModuleReply.ERROR,
							error_message = "An unexpected attribute is present")
							moduleReply.addErrorInfo("bad-attribute",att.name)
							moduleReply.addErrorInfo("bad-element",child.tagName)
							self.operationReply.setError()
							self.operationReply.setNode(moduleReply.getXMLNodeReply())
							return

#					if self.filterType == C.XPATH:
#						tmpval = self.filter.childNodes[0].nodeValue
#						self.xpathrequest = string.strip(str(tmpval))


					
					if (self.xpathrequest != None and self.filterType != C.XPATH):
						moduleReply = ModuleReply(
						error_type = ModuleReply.PROTOCOL,
						error_tag = ModuleReply.UNKNOWN_ATTRIBUTE,
						error_severity = ModuleReply.ERROR,
						error_message = "select without xpath type")
						moduleReply.addErrorInfo("bad-attribute",att.name)
						moduleReply.addErrorInfo("bad-element",child.tagName)
						self.operationReply.setError()
						self.operationReply.setNode(moduleReply.getXMLNodeReply())
						return
					elif self.filterType == C.SUBTREE:
						for node in self.filter.childNodes:
							if (node.nodeType==Node.ELEMENT_NODE):
								self.subtree = node
						# Add by manu 03/09
						# to deal with the special case <get><filter></filter>
						if self.subtree == None:
						  self.subtree = implementation.createDocument(C.YENCAP_XMLNS, 'data', None).documentElement

				else:
					moduleReply = ModuleReply(
					error_type = ModuleReply.PROTOCOL,
					error_tag = ModuleReply.UNKNOWN_ELEMENT,
					error_severity = ModuleReply.ERROR,
					error_message = "An element is not known.")
					moduleReply.addErrorInfo("bad-element",child.tagName)
					self.operationReply.setError()
					self.operationReply.setNode(moduleReply.getXMLNodeReply())
					return
				
				# Add by manu 03/09
				# to deal with the special case <get/>
								
		if self.filter == None:
			self.subtree = implementation.createDocument(C.YENCAP_XMLNS, 'netconf', None).documentElement

