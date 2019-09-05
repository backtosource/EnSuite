###############################################################################
#                                                                             #
# YencaP software, LORIA-INRIA LORRAINE, MADYNES RESEARCH TEAM                #
# Copyright (C) 2005  Vincent CRIDLIG					                      #
#									                                          #
# YencaP Module, University of Tuebingen, Wilhelm Schickard Institut	      #
# Computer Networks and Internet, Prof. Dr. Georg Carle    		              #
# http://www-ri.informatik.uni-tuebingen.de				                      #
# 									                                          #	
# Copyright (C) 2006  Maximilian Huetter                                      #
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
#   Name : Maximilian Huetter                                                 #
#   Email: maxhuetter@web.de			                                      #
#                                                                             #
###############################################################################
import os, string

from Ft.Xml.Domlette import NonvalidatingReader, implementation, PrettyPrint
from Ft.Xml import XPath, EMPTY_NAMESPACE, InputSource
from xml.dom import Node
from Ft.Xml.XPath import Evaluate, Compile
from Ft.Xml.XPath.Context import Context
from Ft.Xml.Xslt import Processor, DomWriter

from constants import C
from modulereply import ModuleReply 
from module import Module 

import popen2, select

class VERMONT_Module(Module):	
	"""
		Module to ENSuite with configuration data following the IPFIX Configuration Data Model 
		(see draft-muenz-ipfix-configuration-00).
		
		The implementation of a IPFIX device it is intended to be used with is the Versatile Monitoring Toolkit (VERMONT).
		See http://vermont.berlios.de/

		Due to the nature of VERMONT, that reads a configuration at startup you can get the running configuration (as there is always a running
		configuration in Netconf, but you can not edit it or copy anything into it. The running configuration just mirrors the startup.
	"""

	# CONFIGURATION DATASTORES
	RUNNING_TARGET = "running"
	CANDIDATE_TARGET = "candidate"
	STARTUP_TARGET = "startup"

	def __init__(self, name, path, namespace, cacheLifetime, parameters):
		Module.__init__(self, name, path, namespace, cacheLifetime)	

	def get(self, configDatastore):		
		dataFile = C.YENCAP_HOME + '/Modules/VERMONT_Module/' + configDatastore + '.xml'
		doc = NonvalidatingReader.parseUri("file:" + dataFile)
		
		modulereply = ModuleReply(replynode=doc.documentElement)
		
		return modulereply
	
	def getConfig(self, configDatastore):		
		return get(configDatastore)

	def copyConfig(self, sourceNode, targetName, urlValue=None):
		"""
			Copy the sourceNode's XML configuration of the current module to the targenName.
			@type targetName: string
			@param targetName: the target datastore (running, candidate, startup)
			@rtype: ModuleReply
			@return: It should return a success or error message.
			** Relates to the netconf copy-config operation
		"""
		
		if (targetName in [C.URL, C.RUNNING]):
			xmlreply = ModuleReply(
			error_type=ModuleReply.APPLICATION,
			error_tag=ModuleReply.OPERATION_NOT_SUPPORTED, 
			error_severity=ModuleReply.ERROR,
			error_message="OPERATION-NOT-SUPPORTED")
			return xmlreply
		
		#candidate or startup configurations are not supported.
		if (targetName in [C.CANDIDATE, C.STARTUP]):
			return self.editConfig(C.REPLACE, C.SET, C.STOP_ON_ERROR, targetName, sourceNode)

	def deleteConfig(self, targetName):
		
		if (targetName in [C.URL, C.RUNNING]):
			xmlreply = ModuleReply(
			error_type=ModuleReply.APPLICATION,
			error_tag=ModuleReply.OPERATION_NOT_SUPPORTED, 
			error_severity=ModuleReply.ERROR,
			error_message="OPERATION-NOT-SUPPORTED")
			return xmlreply

		if os.path.exists(C.YENCAP_HOME + '/Modules/VERMONT_Module/' + targetName + '.xml'):
			os.remove(C.YENCAP_HOME + '/Modules/VERMONT_Module/' + targetName + '.xml')
			xmlreply = ModuleReply()
			return xmlreply
		else:
			xmlreply = ModuleReply(
			error_type=ModuleReply.APPLICATION,
			error_tag=ModuleReply.OPERATION_FAILED, 
			error_severity=ModuleReply.ERROR,
			error_message="Datastore is empty.")
			return xmlreply
		

	def editConfig(self, defaultoperation, testoption, erroroption, target, confignode, targetnode=None):
		"""
			Apply the request specified in confignode to the targetnode.
			@type defaultoperation: MERGE_OPERATION | REPLACE_OPERATION | NONE_OPERATION 
			@param defaultoperation : as specified in NETCONF protocol
			@type testoption : SET | TEST_AND_SET 
			@param testoption : as specified in NETCONF protocol
			@type erroroption : STOP_ON_ERROR | IGNORE_ERROR | ROLL_BACK_ON_ERROR 
			@param erroroption : as specified in NETCONF protocol
			@type target : RUNNING_TARGET | CANDIDATE_TARGET | STARTUP_TARGET
			@param target : as specified in NETCONF protocol
			@type targetnode : string
			@param targetnode : if the target is RUNNING_TARGET or STARTUP_TARGET it will be ignored otherwise should be the node of the 				CANDIDATE_TARGET that this module should process
			@rtype: ModuleReply
			@return: It should return a success or error message.
			** Relates to the netconf edit-config operation
		"""
		
		error = None

		if (target in [C.URL, C.RUNNING]):
			xmlreply = ModuleReply(
			error_type=ModuleReply.APPLICATION,
			error_tag=ModuleReply.OPERATION_NOT_SUPPORTED, 
			error_severity=ModuleReply.ERROR,
			error_message="OPERATION-NOT-SUPPORTED")
			return xmlreply	
			
		
		if defaultoperation == "replace":
			f = open(C.YENCAP_HOME + '/Modules/VERMONT_Module/' + target + '.xml','w')
			PrettyPrint(confignode, f)
			f.close()
			return ModuleReply()		

		# draft-ietf-netconf-prot-11 says: "the default value for the default-operation is merge"
		# in this datamodel merge will replace all nodes with the same type and id it finds in configNodeRoot
		# and adds all it can't find
		elif defaultoperation == "merge":

			if not os.path.exists(C.YENCAP_HOME + '/Modules/VERMONT_Module/' + target + '.xml'):
				ipfixConfigBase = '<ipfixConfig xmlns="urn:ietf:params:xml:ns:ipfix-config"></ipfixConfig>'
				xmlfile = file(C.YENCAP_HOME + '/Modules/VERMONT_Module/' + target + '.xml','w')
				xmlfile.write(ipfixConfigBase)
				xmlfile.close()
			
			dataFile = C.YENCAP_HOME + '/Modules/VERMONT_Module/' + target + '.xml'
			configDoc = NonvalidatingReader.parseUri("file:" + dataFile)

			configNodeRoot = configDoc.documentElement

			for newProcess in confignode.documentElement.childNodes:
				if newProcess.nodeType == Node.ELEMENT_NODE:
					processName = newProcess.localName
					processId = newProcess.getAttributeNS(EMPTY_NAMESPACE, "id")
					
					isNew = True
													
					for oldProcess in configDoc.documentElement.childNodes:

						if oldProcess.nodeType == Node.ELEMENT_NODE:
							
							if oldProcess.tagName == processName:
								#oldProcessId = oldProcess.attributes[(None, u'id')].value
								oldProcessId = oldProcess.getAttributeNS(EMPTY_NAMESPACE, "id")
								print "Old ProcessId:" + oldProcessId
								if oldProcessId == processId:
									isNew = False
									configNodeRoot.replaceChild(newProcess, oldProcess)
									
					if isNew:
						print "appending"
						configNodeRoot.appendChild(newProcess)

		#otherwise, every node has its own operation, create, delete, replace or merge 
		#the data model ipfix-config-data-model has to treat merge just as replace, as detailed
		#editing of some parts of the data are impossible, due to possible ambiguities. 				
		else:
			if not os.path.exists(C.YENCAP_HOME + '/Modules/VERMONT_Module/' + target + '.xml'):
				ipfixConfigBase = '<ipfixConfig xmlns="urn:ietf:params:xml:ns:ipfix-config"></ipfixConfig>'
				xmlfile = file(C.YENCAP_HOME + '/Modules/VERMONT_Module/' + target + '.xml','w')
				xmlfile.write(ipfixConfigBase)
				xmlfile.close()

			dataFile = C.YENCAP_HOME + '/Modules/VERMONT_Module/' + target + '.xml'
			configDoc = NonvalidatingReader.parseUri("file:" + dataFile)

			for newProcess in confignode.documentElement.childNodes:
				if newProcess.nodeType == Node.ELEMENT_NODE:
					processName = newProcess.localName
					operation = newProcess.getAttributeNS('ietf:params:xml:ns:netconf:base:1.0', "operation")
					processId = newProcess.getAttributeNS(EMPTY_NAMESPACE, "id")
											
					print processName
					print operation
					print processId

					if processName == "ipfixConfig":
						continue
					if processId == None:
						error = "Config data to add has errors!"
						moduleReply = ModuleReply(
							error_type = ModuleReply.APPLICATION,
							error_tag = ModuleReply.OPERATION_FAILED,
							error_severity = ModuleReply.ERROR,
							error_message = error)
						return moduleReply
						
					
					if operation == None:	
						error == "If no defaultoperation is chosen, every process has to have its own operation!"
						moduleReply = ModuleReply(
							error_type = ModuleReply.APPLICATION,
							error_tag = ModuleReply.OPERATION_FAILED,
							error_severity = ModuleReply.ERROR,
							error_message = error)
						return moduleReply
					
					if operation == "create":
						configDoc.documentElement.appendChild(newProcess)
					else:
						error = processName + " " +  "not found!"

						for oldProcess in configDoc.documentElement.childNodes:

							if oldProcess.nodeType == Node.ELEMENT_NODE:
								if oldProcess.tagName == processName:
									#oldProcessId = oldProcess.attributes[(None, u'id')].value
									oldProcessId = oldProcess.getAttributeNS(EMPTY_NAMESPACE, "id")
									if oldProcessId == processId:
								
										if operation == "delete":
											configDoc.documentElement.removeChild(oldProcess)
											error = None
										elif operation == "replace" or operation == "merge":
											configDoc.documentElement.replaceChild(newProcess, oldProcess)
											error = None
										if error != None:
											if erroroption == "stop-on-error":
												modulereply = ModuleReply(error_type=ModuleReply.APPLICATION, error_tag=ModuleReply.OPERATION_FAILED, error_severity=ModuleReply.ERROR, error_message=error)
												return modulereply
		
		xmlFile = open(C.YENCAP_HOME + '/Modules/VERMONT_Module/' + target + '.xml','w')
		PrettyPrint(configDoc, xmlFile)
		xmlFile.close()
		
		if error == None:
			modulereply = ModuleReply()
		else:
			modulereply = ModuleReply(error_type=ModuleReply.APPLICATION, error_tag=ModuleReply.OPERATION_FAILED, error_severity=ModuleReply.ERROR, error_message=error)
			return modulereply
		return modulereply


	def validate(self, targetName, moduleNode = None):
		"""
			Validates the configuration of the targetnode by first calling xmllint to valdidate against the VERMONT-Config-Schema.xsd
			and then check the datapath of the configuration.
			@rtype: ModuleReply
			@return: It should return an error if the configuration does not validate 
		"""
		outdata = ""

		if (targetName in [C.URL, C.RUNNING]):
			xmlreply = ModuleReply(
			error_type=ModuleReply.APPLICATION,
			error_tag=ModuleReply.OPERATION_NOT_SUPPORTED, 
			error_severity=ModuleReply.ERROR,
			error_message="OPERATION-NOT-SUPPORTED")
			return xmlreply

		# call xmllint to validate against the schema

		cmd = "xmllint --schema " + C.YENCAP_HOME + "/Modules/VERMONT_Module/VERMONT-Config-Schema.xsd " + C.YENCAP_HOME + '/Modules/VERMONT_Module/' + targetName + '.xml'
		xmllintcmd = popen2.Popen3(cmd,1)
		xmllintcmd.tochild.close()
		outfile = xmllintcmd.fromchild
		outfd = outfile.fileno()
		
		errfile = xmllintcmd.childerr
		errfd = errfile.fileno()

		errdata = ""
		outeof = erreof = 0

		while 1:
			ready = select.select([outfd, errfd],[],[])
			if outfd in ready[0]:
				outchunk = outfile.read()
				if outchunk == "":
					outeof = 1
				outdata = outdata + outchunk

			if errfd in ready[0]:
				errchunk = errfile.read()
				if errchunk == "":
					erreof = 1
				errdata = errdata + errchunk
			if outeof and erreof: 
				break
			select.select([],[],[],.1)
			
		err = xmllintcmd.wait()
		if err != 0:
			modulereply = ModuleReply(
			error_type=ModuleReply.APPLICATION,
			error_tag=ModuleReply.OPERATION_FAILED, 
			error_severity=ModuleReply.ERROR,
			error_message="Validation error: " + errdata)
			return modulereply	
										
		
		#Data is valid according to the schema VERMONT-Config-Schema.xsd
		#Now check for the correct order of the processes 
		if moduleNode == None:
			dataFile = C.YENCAP_HOME + '/Modules/VERMONT_Module/' + targetName + '.xml'
			configDoc = NonvalidatingReader.parseUri("file:" + dataFile)
			moduleNode = configDoc.documentElement
		
		#first check the observationPoints process order, if a observationPoint is followed by packetSelection
		#there has to be a MeteringProcess with packetReporting as well.

		#first get all meteringProcesses following the observationPoint: 
		nextMeteringProcesses = []
		for node in moduleNode.childNodes:
			if node.nodeType == Node.ELEMENT_NODE:
				if node.tagName == "observationPoint":					
					for childnode in node.childNodes:						
						if childnode.nodeType == Node.ELEMENT_NODE:
							if childnode.tagName == "next":
								for nextChild in childnode.childNodes:
									if nextChild.nodeType == Node.ELEMENT_NODE:
										if nextChild.tagName == "meteringProcessId":
											for textChild in nextChild.childNodes:
												if textChild.nodeType == Node.TEXT_NODE:
													nextMeteringProcesses.append(textChild.nodeValue)
				
		#Check if the meteringProcess follows a observationPoint and if it has packetSelection. If it does, it may have packetReporting as well.
		#If not it has to have a following meteringProcess which does.
		SearchPR = "false"
		for node in moduleNode.childNodes:
			if node.nodeType == Node.ELEMENT_NODE:
				if node.tagName == "meteringProcess":
					meteringProcessId = node.getAttributeNS(EMPTY_NAMESPACE, "id")
					if meteringProcessId in nextMeteringProcesses:
						for childnode in node.childNodes:
							if childnode.nodeType == Node.ELEMENT_NODE:
								if childnode.tagName == "packetSelection":
									SearchPR = "true"
						if SearchPR == "true":
							for childnode in node.childNodes:
								if childnode.nodeType == Node.ELEMENT_NODE:
									if childnode.tagName == "packetReporting":
										SearchPR = "false"
						#if there is not packetReporting in the same meteringProcess, check the next process. Therefore get the processId.
						if SearchPR == "true":
							for childnode in node.childNodes:
								if childnode.nodeType == Node.ELEMENT_NODE:
									if childnode.tagName == "next":
										for nextChild in childnode.childNodes:
											if nextChild.nodeType == Node.ELEMENT_NODE:
												if nextChild.tagName == "meteringProcessId":
													for textChild in nextChild.childNodes:
														if textChild.nodeType == Node.TEXT_NODE:
															followUpMeteringProcessId = textChild.nodeValue
															print "followUpMeteringProcessId: " 
															print followUpMeteringProcessId
		#Is there such a meteringProcess with packetReporting:
		for node in moduleNode.childNodes:
			if node.nodeType == Node.ELEMENT_NODE:
				if node.tagName == "meteringProcess":
					meteringProcessId = node.getAttributeNS(EMPTY_NAMESPACE, "id")
					
					if meteringProcessId == followUpMeteringProcessId:
						for childnode in node.childNodes:
							if childnode.nodeType == Node.ELEMENT_NODE:
								if childnode.tagName == "packetReporting":
									SearchPR = "false"
		#If there is no packetReporting, that is an error.
		if SearchPR == "true":
			modulereply = ModuleReply(
			error_type=ModuleReply.APPLICATION,
			error_tag=ModuleReply.OPERATION_FAILED, 
			error_severity=ModuleReply.ERROR,
			error_message="Validation error: No packetReporting following a packetSelection.")
			return modulereply

		#A collectingProcess can only be followed by a MeteringProcess with flowMetering, so get the following meteringProcesses to check.
		nextMeteringProcesses = []
		for node in moduleNode.childNodes:
			if node.nodeType == Node.ELEMENT_NODE:
				if node.tagName == "collectingProcess":
					for childnode in node.childNodes:
						if childnode.nodeType == Node.ELEMENT_NODE:
							if childnode.tagName == "next":
								for nextChild in childnode.childNodes:
									if nextChild.nodeType == Node.ELEMENT_NODE:
										if nextChild.tagName == "meteringProcessId":
											for textChild in nextChild.childNodes:
												if textChild.nodeType == Node.TEXT_NODE:
													nextMeteringProcesses.append(textChild.nodeValue)

		#Check all following meteringProcess, if they have packetSelection or packetReporting, which will raise an error.
		for node in moduleNode.childNodes:
			if node.nodeType == Node.ELEMENT_NODE:
				if node.tagName == "meteringProcess":
					meteringProcessId = node.getAttributeNS(EMPTY_NAMESPACE, "id")
					if meteringProcessId in nextMeteringProcesses:
						for childnode in node.childNodes:
							if childnode.nodeType == Node.ELEMENT_NODE:
								if node.tagName in ["packetSelection","packetReporting"]:
									modulereply = ModuleReply(
									error_type=ModuleReply.APPLICATION,
									error_tag=ModuleReply.OPERATION_FAILED, 
									error_severity=ModuleReply.ERROR,
									error_message="Validation error: packetSelection or packetReporting follows collectingProcess")
									return modulereply

		#If everything is correct, just return a ok.
		modulereply = ModuleReply()
		return modulereply
		

	def restart(self):
		""" 
		Restart VERMONT
		Forks a new process with VERMONT in parallel.
 
		"""
		newpid = os.fork()
		
		if newpid == 0:
			os.execlp('vermont', 'vermont', '-fstartup.xml')
		
		else: 
			modulereply = ModuleReply()
			return modulereply

	
		
		

		
		
