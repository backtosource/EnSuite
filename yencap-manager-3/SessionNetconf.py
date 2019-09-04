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
#   Name : Jerome BOURDELLON                                                  #
#   Email: Jerome.Bourdellon@loria.fr                                         #
#                                                                             #
# Modified by:                                                                #
#   Name : Frederic Beck                                                      #
#   Email : Frederic.Beck@loria.fr                                            #
#                                                                             #
###############################################################################


from Ft.Xml.Domlette import NonvalidatingReader
from util import *
from threading import Thread
import RequestFactory
from Constants import C
from sessionSSH import *
import time, os
from os import  popen3
from subprocess import  Popen, PIPE, call

class SessionNetconf(Thread):
	
	# instance of RequestFactory
	reqFactory = RequestFactory.getInstance()
	
		
	def __init__(self, agent, user):
		
		Thread.__init__(self)
		
		self.agent = agent
		self.user = user
		
		self.msg_id = 0		

		
		if self.agent.getProtocol() == 'ssh':

			self.client = sessionSSH(self.agent, self.user)
			
		elif self.agent.getProtocol() == 'beep':
			print 'NOT IMPLEMENTED'

		
		connected = C.FAILED
		try:
			# Connect to the Netconf agent:
			connected = self.client.connect()
			
		except Exception, exp:
			print str(exp)

		if connected:

			# Build a Hello node containing capabilities, also checking that it is well-formed.
			doc = NonvalidatingReader.parseUri('file:%s' % (C.HELLO_URI))

			# Serialize the Hello XML document to a string
			req = convertNodeToString(doc.documentElement)

			# Send the string capabilities, and receive agent capabilities
			agentCapabilities = self.client.send(req)

			# Store agent capabilities
			self.agent.setCapabilities(agentCapabilities)
			
			# YANG 17/6/9
			
			if self.agent.hasYangModule():
				yms = ("-p",C.YENCAP_MAN_YANG_HOME)
				for ym in self.agent.yangmodules:
					s = C.YENCAP_MAN_YANG_HOME + "/" + ym + ".yang"
					yms = yms + (s ,)
			
				
				cmdline = ("java",  "-jar",  "YangTreeNodeGenerator.jar", str(agent.ip)) +  yms
				#cmdline = ("java", "-cp", ".:../../Parser/yang:../../yang-manager/bin", "YangSchemaTreeGenerator", str(agent.ip), str(ins))
				#cmdline = cmdline + nsp + (str(iyms),) + yms + yxp
				
				print cmdline
			
				err = Popen(cmdline, stderr=PIPE).stderr
										  
				errors = ""
				for eachline in err.readlines():
					errors = errors + "<tr><td>" + eachline + "</tr></td>"
				self.agent.setYangErrMesg(errors)
			
			# YANG
		else:
			raise Exception('Not Connected')
		

	def close(self):
		"""
			Close a Netconf session.
		"""

		# Send a close-session operation (which has no argument: {}) to the agent.
		netconfReply = self.sendRequest(C.CLOSE_SESSION, {})
		# Close the client socket
		self.client.close()
		
		
	def getAgent(self):
		"""
			Return information about the agent of this SessionNetconf.
		"""	
		
		# return the agent of this session NetConf
		return self.agent

		
	def sendRequest(self, operation, args):
		
		# Increment the message-id attribute of rpc element:
		self.msg_id += 1

		# Create the rpc request from its operation name (like get-config, ...):
		req = self.reqFactory.createRequest(self.msg_id, operation, args)

		# Convert the rpc XML document to a string:
		stringreq = convertNodeToString(req)

		print "envoie requete : \n" + stringreq

		# Send the serialized rpc to the agent:
		return self.client.send(stringreq)

