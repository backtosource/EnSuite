
import os, string

from Ft.Xml.Domlette import NonvalidatingReader, implementation, PrettyPrint
from Ft.Xml import XPath, EMPTY_NAMESPACE
from xml.dom import Node
from Ft.Xml.XPath import Evaluate, Compile
from Ft.Xml.XPath.Context import Context

from Modules.modulereply import ModuleReply 
from Modules.module import Module 

from constants import C


class VERMONT_Module(Module):	


	def __init__(self, name, path, namespace, cacheLifetime, parameters):
		Module.__init__(self, name, path, namespace, cacheLifetime, parameters)
		
	def getConfig(self):
		self.doc = implementation.createDocument(self.namespace, None, None)
		element = doc.createElementNS(self.namespace,"MonitorConfig")
		self.doc.appendChild(element)
		modulereply = ModuleReply(replynode=self.doc.documentElement)
		return modulereply

	def editConfig(self, defaultoperation, testoption, erroroption, target, confignode, targetnode=None):
		# Apply the request
		# ...

		# No error raised...
		modulereply = ModuleReply()
		return modulereply

		
