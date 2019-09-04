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


from Ft.Xml.Domlette import PrettyPrint, implementation
from Ft.Xml import EMPTY_NAMESPACE
from xml.dom import Node
import string, util
from Modules.modulereply import ModuleReply
from abstractFilter import AbstractFilter


class SubtreeFilter(AbstractFilter):
	
	def __init__(self, configDocument, filterDocument):
		self.configDocument = configDocument
		self.filterDocument = filterDocument
		self.resultDocument = implementation.createDocument(EMPTY_NAMESPACE, None, None)
		
		
	def applyFilter(self):
		for configElement in self.configDocument.childNodes:
			self.netconfFilter(configElement, self.filterDocument, self.resultDocument)
			moduleReply = ModuleReply(self.resultDocument.documentElement)
		return moduleReply
	
	"""	
	def createNode(self, doc, parent, tag, value=None):
		element = doc.createElementNS(EMPTY_NAMESPACE,tag)
		parent.appendChild(element)
		if (value != None):
			text = doc.createTextNode(value)
			element.appendChild(text)
		return element
	"""
	
	# return names of ELEMENT nodes that contains ELEMENT nodes 
	#  under the filterNode
	def getContainementNodeList(self, filterNode):
		res =[]
		for node in filterNode.childNodes:
			if node.nodeType == Node.ELEMENT_NODE:
				for n in node.childNodes:
					if n.nodeType == Node.ELEMENT_NODE:
						sname = node.namespaceURI + ":" + node.tagName.split(":")[-1]
						#sname = node.namespaceURI + ":" + node.tagName
						res.append(sname)
		return res
	
	# returns names of TEXT element that are childs of childs of the 
	# filter node
	#
	def getContentMatchNodeDictionnary(self, filterNode):
		# Content Match Nodes Dictionnary
		cmnd = {}
		for node in filterNode.childNodes:									
			for n in node.childNodes:
				if n.nodeType == Node.TEXT_NODE and n.nodeValue != None:
					#key = node.namespaceURI + ":" + node.tagName
					value = string.strip(n.nodeValue)
					if value != "":
						key = node.namespaceURI + ":" + node.tagName.split(":")[-1]
						cmnd[key] = value
		return cmnd
	
	
	
	def checkContentMatchNodes(self, configNode, filterNode):
		# Content Match Nodes Dictionnary
		filtercmnd = self.getContentMatchNodeDictionnary(filterNode)
		configcmnd = self.getContentMatchNodeDictionnary(configNode)
	
		for a in filtercmnd:
			if (not configcmnd.has_key(a))  or (not configcmnd[a] == filtercmnd[a]):
				return 0,[]
	
		return 1,filtercmnd
	
	# return names of children nodes that are Element nodes
	# with no children
	# under the filterNode given in parameter
	def getSelectionNodeList(self, filterNode):
		res =[]
		for node in filterNode.childNodes:
			if (node.nodeType == Node.ELEMENT_NODE and node.childNodes == []):
				res.append(node.namespaceURI + ":" + node.tagName.split(":")[-1])
		return res
	
	# check if all attributes in fnode are in node attributes
	# the value is compared
	# add by manu 03/09
	def checkAttributesValue(self, node, fnode):
		fatts = fnode.attributes
		natts = node.attributes
		onemore = 0
		for fatt in fatts:
			for att in natts:
				if fnode.attributes[fatt].value == node.attributes[att].value:
					onemore += 1
#				else:
#					return False
		if onemore == fatts.length:
			return True
		else:
			return False
		
	# return names of node elements common between
	# configNode and filterNode and a copy of the config node is 
	# added under the resultNode 
	
	def fillSelectionNodes(self, configNode, filterNode, resultNode):
		snl = self.getSelectionNodeList(filterNode)
		for node in configNode.childNodes:
			if node.nodeType == Node.ELEMENT_NODE:
				sname = node.namespaceURI + ":" + node.tagName.split(":")[-1]
				#sname = node.namespaceURI + ":" + node.tagName
				if sname in snl:
					# add by manu 03/09
					# in order to select with an attribute
					if node.attributes.length != 0:
						for fnode in filterNode.childNodes:
							if (fnode.nodeType == Node.ELEMENT_NODE):
								fsname = fnode.namespaceURI + ":" + fnode.tagName.split(":")[-1]
								if fsname == sname:
									if fnode.attributes.length != 0:
										if self.checkAttributesValue(node,fnode):
											clone = self.resultDocument.importNode(node, True)
											resultNode.appendChild(clone)
									else:
										clone = self.resultDocument.importNode(node, True)
										resultNode.appendChild(clone)
					else:
						clone = self.resultDocument.importNode(node, True)
						resultNode.appendChild(clone)
		return snl
	
	
	def netconfFilter(self, configNode, filterNode, resultNode):
		
		if (configNode.nodeType == Node.ELEMENT_NODE
		and filterNode.nodeType == Node.ELEMENT_NODE
		and configNode.tagName.split(":")[-1] == filterNode.tagName.split(":")[-1]
		#and configNode.tagName == filterNode.tagName
		and configNode.namespaceURI == filterNode.namespaceURI):

			bool, filtercmnd = self.checkContentMatchNodes(configNode, filterNode)
			
			if  (bool):
				currentNode = self.resultDocument.createElementNS(configNode.namespaceURI, configNode.tagName.split(":")[-1])
				#currentNode = self.resultDocument.createElementNS(configNode.namespaceURI, configNode.tagName)
				resultNode.appendChild(currentNode)
				for att in configNode.attributes:
					ns, name = att
					value = configNode.getAttributeNS(ns, str(name))
					currentNode.setAttributeNS(ns, str(name), value)	

				# Copy Content Match nodes if any to the result document
				if (filtercmnd != {}):
					for node in configNode.childNodes:
						if node.nodeType == Node.ELEMENT_NODE:
							sname = node.namespaceURI + ":" + node.tagName.split(":")[-1]
							#sname = node.namespaceURI + ":" + node.tagName
							if node.nodeType == Node.ELEMENT_NODE and sname in filtercmnd:
								clone = self.resultDocument.importNode(node, True)
								currentNode.appendChild(clone)
	
				# Fill selection nodes to the result document
				snl = self.fillSelectionNodes(configNode, filterNode, currentNode)
				
				# Retrieve containement node list
				cnl = self.getContainementNodeList(filterNode)
				
				# If only Content match nodes, copy all other children of the configuration :
				if (snl==[] and cnl==[]):
					for node in configNode.childNodes:
						if node.nodeType == Node.ELEMENT_NODE:
							sname = node.namespaceURI + ":" + node.tagName.split(":")[-1]
							#sname = node.namespaceURI + ":" + node.tagName
							if sname not in filtercmnd:
								clone = self.resultDocument.importNode(node, True)
								currentNode.appendChild(clone)

					return
				
				# Keep doing recursively with other children
				for f in filterNode.childNodes:
					if f.nodeType == Node.ELEMENT_NODE:
						sname = f.namespaceURI + ":" + f.tagName.split(":")[-1]
						#sname = f.namespaceURI + ":" + f.tagName
						if (not sname in snl) and (not sname in filtercmnd):
							for c in configNode.childNodes:
								if c.nodeType == Node.ELEMENT_NODE:
									# add by manu 03/09
									# to cut nodes that do not match an attribute in the filter
									if f.attributes.length != 0:
										if c.attributes.length != 0:
											if self.checkAttributesValue(c, f):
												self.netconfFilter(c, f, currentNode)
										else:
											self.netconfFilter(c, f, currentNode)
									else:
										self.netconfFilter(c, f, currentNode)
										

