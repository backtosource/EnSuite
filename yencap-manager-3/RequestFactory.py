###############################################################################
#                                                                             #
# YencaPManager software, LORIA-INRIA LORRAINE, MADYNES RESEARCH TEAM         #
# Copyright (C) 2005  Jerome BOURDELLON                                       #
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

from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Domlette import NonvalidatingReader, PrettyPrint, implementation
from Constants import C
from xml.dom import XMLNS_NAMESPACE
from Components.Modules import ModuleManager


class RequestFactory:
	
	instance = None	

	def __init__(self):
		# This builds a dictionnary of known prefixes to help people using XPath via the web interface.
		self.namespace_prefix = ModuleManager.getInstance().prefixes
	

	def createRequest(self, msgID, operation, args={}):
		"""
			Creates a new NetConf request.
			@type  msgID : int
			@param msgID : The message ID for the Netconf request
			@type  operation : String
			@param operation : NetConf operation : get-config, get, copy-config, delete-config, close-session, edit-config
			@type  args : Dictionnary 
			@param args : Dictionnary with the request args
			@rtype: String
			@return: The weel-formed NetConf request
		"""
						
		if (operation == C.GET_CONFIG):
			doc = self.generate_get_config(msgID, args[C.SOURCE], args[C.TYPE], args[C.FILTER])
		elif (operation == C.GET):
			doc = self.generate_get(msgID, args[C.TYPE], args[C.FILTER])
		elif (operation == C.COPY_CONFIG):
			doc = self.generate_copy_config(msgID, args[C.TARGET], args[C.SOURCE], args["inlineconfig"])
		elif (operation == C.VALIDATE):
			doc = self.generate_validate(msgID, args[C.SOURCE], args["inlineconfig"])
		elif (operation == C.LOCK):
			doc = self.generate_lock(msgID, args[C.TARGET])
		elif (operation == C.UNLOCK):
			doc = self.generate_unlock(msgID, args[C.TARGET])
		elif (operation == C.DELETE_CONFIG):
			doc = self.generate_delete(msgID, args[C.TARGET])
		elif (operation == C.EDIT_CONFIG):
			if args.has_key(C.ERROR_OPTION):
				eo = args[C.ERROR_OPTION]
			else:
				eo = None
			if args.has_key(C.DEFAULT_OPERATION):
				do = args[C.DEFAULT_OPERATION]
			else:
				do = None
			if args.has_key(C.TEST_OPTION):
				to = args[C.TEST_OPTION]
			else:
				to = None
			doc = self.generate_edit_config(msgID, args[C.TARGET], args[C.CONFIG], eo, do, to)
		elif (operation == C.KILL_SESSION):
			doc = self.generate_kill_session(msgID, args[C.SESSION_ID])
		elif (operation == C.CLOSE_SESSION):
			doc = self.generate_close_session(msgID)
		elif (operation == C.COMMIT):
			doc = self.generate_commit(msgID)
		elif (operation == C.DISCARD_CHANGES):
			doc = self.generate_discard_changes(msgID)
		elif (operation == 'manage-mib-modules'):
			if args['mmOp'] == "deploy":
				doc = self.generate_manage_mib_modules(msgID,args['mmOp'],args['name'],args['xpath'],args['namespace'],args['cachelifetime'],args['file'],args['pref'])
			else:
				doc = self.generate_manage_mib_modules(msgID,args['mmOp'],args['name'])
		elif (operation == 'rbac'):
			doc = self.generate_rbac(msgID, args['rbacOp'], args['roleName'])
		
		return doc.documentElement
	

	def generate_get_config(self, msgID, sourceName, filtertype, filterdata):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, C.GET_CONFIG)
		self.setSource(doc, operationNode, sourceName)
		if filterdata != '':
			self.setFilter(doc, operationNode, filtertype, filterdata)
		return doc

	def generate_get(self, msgID, filtertype, filterdata):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, C.GET)
		if filterdata != '':
			self.setFilter(doc, operationNode, filtertype, filterdata)
		return doc

	def generate_copy_config(self, msgID, targetName, sourceName, inlineconfig = None):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, C.COPY_CONFIG)
		self.setSource(doc, operationNode, sourceName, inlineconfig)
		self.setTarget(doc, operationNode, targetName)
		return doc

	def generate_validate(self, msgID, sourceName, inlineconfig = None):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, C.VALIDATE)
		self.setSource(doc, operationNode, sourceName, inlineconfig)
		return doc

	def generate_lock(self, msgID, targetName):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, C.LOCK)
		self.setTarget(doc, operationNode, targetName)
		return doc

	def generate_unlock(self, msgID, targetName):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, C.UNLOCK)
		self.setTarget(doc, operationNode, targetName)
		return doc

	def generate_delete(self, msgID, targetName):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, C.DELETE_CONFIG)
		self.setTarget(doc, operationNode, targetName)
		return doc

	def generate_edit_config(self, msgID, targetName, inlineconfig, error_option = None, default_operation = None, test_option = None):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, C.EDIT_CONFIG)
		if error_option != None:
			self.setOption(doc, operationNode, error_option, C.ERROR_OPTION)
		if default_operation != None:
			self.setOption(doc, operationNode, default_operation, C.DEFAULT_OPERATION)
		if test_option != None:
			self.setOption(doc, operationNode, test_option, C.TEST_OPTION)
			
		self.setTarget(doc, operationNode, targetName)

		configNode = doc.createElementNS(C.NETCONF_NS, C.CONFIG)
		operationNode.appendChild(configNode)
		#cNode = NonvalidatingReader.parseString(inlineconfig).documentElement
		cNode = doc.importNode(inlineconfig, True)
		configNode.appendChild(cNode)
		return doc

	def generate_kill_session(self, msgID, session_id):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, C.KILL_SESSION)
		sessionIdNode = doc.createElementNS(C.NETCONF_NS, C.SESSION_ID)
		operationNode.appendChild(sessionIdNode)
		sNode = doc.createTextNode(session_id)
		sessionIdNode.appendChild(sNode)
		return doc

	def generate_close_session(self, msgID):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, C.CLOSE_SESSION)
		return doc
		
	def generate_commit(self, msgID):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, C.COMMIT)
		return doc

	def generate_discard_changes(self, msgID):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, C.DISCARD_CHANGES)
		return doc

	def generate_manage_mib_modules(self, msgID, m_op, m_name, m_xpath = None, m_namespace = None, m_cachelifetime = None, m_file = None, m_pref = None):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, "manage-mib-modules")
		mmopNode = doc.createElementNS(EMPTY_NAMESPACE, m_op)
		operationNode.appendChild(mmopNode)
		nameNode = doc.createElementNS(EMPTY_NAMESPACE,"name")
		mmopNode.appendChild(nameNode)
		nNode = doc.createTextNode(m_name)
		nameNode.appendChild(nNode)

		if m_op == 'deploy':

			tmpNode = doc.createElementNS(EMPTY_NAMESPACE, "xpath")
			mmopNode.appendChild(tmpNode)
			nNode = doc.createTextNode(m_xpath)
			tmpNode.appendChild(nNode)

			tmpNode = doc.createElementNS(EMPTY_NAMESPACE, "namespace")
			mmopNode.appendChild(tmpNode)
			nNode = doc.createTextNode(m_namespace)
			tmpNode.appendChild(nNode)
			tmpNode.setAttributeNS(EMPTY_NAMESPACE, "pref", m_pref)
			
			tmpNode = doc.createElementNS(EMPTY_NAMESPACE, "cachelifetime")
			mmopNode.appendChild(tmpNode)
			nNode = doc.createTextNode(m_cachelifetime)
			tmpNode.appendChild(nNode)

			tmpNode = doc.createElementNS(EMPTY_NAMESPACE, "file")
			mmopNode.appendChild(tmpNode)
			nNode = doc.createTextNode(m_file)
			tmpNode.appendChild(nNode)
			
			tmpNode = doc.createElementNS(EMPTY_NAMESPACE, "parameters")
			mmopNode.appendChild(tmpNode)

		return doc

	def generate_rbac(self, msgID, rbac_op, rbac_rolename):
		doc = implementation.createDocument(C.NETCONF_NS, C.RPC, None)
		operationNode = self.setOperationNode(doc, msgID, "rbac")
		rbacopNode = doc.createElementNS(EMPTY_NAMESPACE,rbac_op)
		operationNode.appendChild(rbacopNode)
		rolesNode = doc.createElementNS(EMPTY_NAMESPACE,"roles")
		rbacopNode.appendChild(rolesNode)
		roleNode = doc.createElementNS(EMPTY_NAMESPACE,"role")
		rolesNode.appendChild(roleNode)
		rNode = doc.createTextNode(rbac_rolename)
		roleNode.appendChild(rNode)
		return doc
	
	def setOperationNode(self, doc, msgID, operation):
		rpcNode = doc.documentElement
		rpcNode.setAttributeNS(None, C.MESSAGE_ID, str(msgID))
		operationNode = doc.createElementNS(C.NETCONF_NS, operation)
		rpcNode.appendChild(operationNode)
		return operationNode

	def setTarget(self, doc, operationNode, target):
		targetNode = doc.createElementNS(C.NETCONF_NS, C.TARGET)
		operationNode.appendChild(targetNode)
		tNode = doc.createElementNS(C.NETCONF_NS, target)
		targetNode.appendChild(tNode)


	def setSource(self, doc, operationNode, sourceName, inlineConfig = None):
		sourceNode = doc.createElementNS(C.NETCONF_NS, C.SOURCE)
		operationNode.appendChild(sourceNode)
		if sourceName == C.CONFIG:
			configNode = doc.createElementNS(C.NETCONF_NS, C.CONFIG)
			sourceNode.appendChild(configNode)
			#sNode = NonvalidatingReader.parseString(inlineConfig).documentElement
			sNode = doc.importNode(inlineConfig, True)
			configNode.appendChild(sNode)
		else:
			sNode = doc.createElementNS(C.NETCONF_NS, sourceName)
			sourceNode.appendChild(sNode)


	def setFilter(self, doc, operationNode, filtertype, filterdata):
		filterNode = doc.createElementNS(C.NETCONF_NS, C.FILTER)
		filterNode.setAttributeNS(C.NETCONF_NS, C.TYPE, filtertype)		
		operationNode.appendChild(filterNode)
		if filtertype == C.SUBTREE:
			#fNode = NonvalidatingReader.parseString(filterdata).documentElement
			fNode = doc.importNode(filterdata, True)
		elif filtertype == C.XPATH:
			for key, value in self.namespace_prefix.items():
				filterNode.setAttributeNS(XMLNS_NAMESPACE, "xmlns:"+key, value)
			fNode = doc.createTextNode(filterdata)
		filterNode.appendChild(fNode)


	def setOption(self, doc, operationNode, optionValue, optionName):
		errorTextNode = doc.createTextNode(optionValue)
		errorNode = doc.createElementNS(C.NETCONF_NS, optionName)
		errorNode.appendChild(errorTextNode)
		operationNode.appendChild(errorNode)


# Singleton : only one instance of the ReqFactory
def getInstance():
	if RequestFactory.instance == None:
		RequestFactory.instance = RequestFactory()
	return RequestFactory.instance

