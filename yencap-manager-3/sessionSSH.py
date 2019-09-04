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

from Constants import C
import paramiko, syslog
import string, base64, socket
from paramiko import RSAKey, DSSKey, Transport


class sessionSSH:

	def __init__(self, agent, user):
		
		self.hostname = agent.getIp()
		self.username = user.getLogin()
		self.publicKey = agent.getPublicKey()
		self.publicKeyType = agent.getPublicKeyType()
		self.version = agent.getVersion()

		self.privateKeyFile=user.getPrivateKeyFile()
		self.privateKeyType=user.getPrivateKeyType()
		self.password = user.getPassword()

		self.raw_data = ''

		# Create a socket (IPv4 or IPv6):
		if self.version == 4:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		elif self.version == 6:
			sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

		#sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

		# Connect to the agent (The SSH tunnel is done later)
		sock.connect((self.hostname, C.NETCONF_SSH_PORT))
		
		# Create a new SSH session over an existing socket (here sock).
		self.ssh = Transport(sock)

		self.i = 1
		
						
	def connect(self):
		
		try:
			
			# Build a public key object from the server (agent) key file
			if self.publicKeyType == 'rsa':
				agent_public_key = RSAKey(data=base64.decodestring(self.publicKey))
			elif self.publicKeyType == 'dss':
				agent_public_key = DSSKey(data=base64.decodestring(self.publicKey))
			
			# Build a private key object from the manager key file, and connect to the agent:
			if self.privateKeyFile != None:
				# Using client (manager) private key to authenticate
				if self.privateKeyType == "rsa":
					user_private_key = RSAKey.from_private_key_file(self.privateKeyFile)
				elif self.privateKeyType == "dss":
					user_private_key = DSSKey.from_private_key_file(self.privateKeyFile )
				self.ssh.connect(hostkey=agent_public_key, username=self.username, pkey=user_private_key)
			else:
				# Using client (manager) password to authenticate
				self.ssh.connect(hostkey=agent_public_key, username=self.username, password=self.password)	
			
			# Request a new channel to the server, of type "session".
			self.chan = self.ssh.open_session()
			
			# Request a "netconf" subsystem on the server:
			self.chan.invoke_subsystem(C.NETCONF_SSH_SUBSYSTEM)
			
		except Exception,exp:
			syslog.openlog("YencaP Manager")
			syslog.syslog(syslog.LOG_ERR, str(exp))
			syslog.closelog()
			return C.FAILED
		
		return C.SUCCESS

		
	def send(self,request):
		"""
			Send a request to a Netconf agent and return a Netconf reply as a string.
		"""
	
		try:
			# Send the request and the delimiter over the channel:
			self.chan.sendall(request+C.DELIMITER)

			# Get the Netconf agent response:
			response = self.getRequest()

			# Return the string Netconf reply:
			return response
			
		except Exception, exp:
			print str(exp)
			
	
	def close(self):
		"""
			Close the SSH session.
		"""
		# Close the SSH channel:
		self.chan.close()

		
	def getRequest(self):
		"""
			Get the Netconf agent response. The method name must be changed.
		"""
		
		stringResponse = ''
			
		messages = self.raw_data.split(C.DELIMITER)
			
		if len(messages) > 1:
			stringResponse = messages[0]
			self.raw_data = self.raw_data[len(stringResponse)+6::]

		while (stringResponse == ''):
			self.raw_data = self.raw_data + self.chan.recv(1024)
			
			messages = self.raw_data.split(C.DELIMITER)
			
			if len(messages) > 1:
				stringResponse = messages[0]
				self.raw_data = self.raw_data[len(stringResponse)+6::]
		
		# Maybe this was to check that the Netconf reply is well-formed ?????
		#response = NonvalidatingReader.parseString(stringResponse,C.NETCONF_NS)
		#return util.convertNodeToString(response)
		return stringResponse
		
