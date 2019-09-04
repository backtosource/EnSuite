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
###############################################################################

from SessionNetconf import *
import Parser
from threading import Thread

class SessionHTTP(Thread):
	
	# Parser
	parser = Parser.getInstance()
	
	def __init__(self,session_id, user):
		Thread.__init__(self)
		
		self.session_id = session_id
		self.user = user
		self.idNetconf = 0
		self.stop = 0
		self.sessionsNetconf = []
		# The session that is currently seen by the manager.
		self.currentNetconfSession = None
		
# SessionHTTP Management  #
		
	"""
			Close an HTTP session
	"""
	def closeHTTP(self):
		
		# get all sessions NetConf for this session HTTP
		
		for session in self.sessionsNetconf:
			# close them
			session.close()
			self.sessionsNetconf.remove(session)

		self.stop = 1	
		

	def setCurrentNetconfSession(self, agent):
		self.currentNetconfSession = self.getNetconf(agent)

	def getCurrentNetconfSession(self):
		return self.currentNetconfSession
		

# SessionNetconf Management  #
	
	def openNetconf(self,agent):
		"""
			Open a new NetConf session for this user
			@type  adr : string
			@param adr : The IP address to use
			@type  port : int
			@param port : The port to use
			@rtype: SessionNetconf
			@return: The newly created NetConf Session
		"""	
		# if no session NetConf opened with this agent 
		netconfSession = self.getNetconf(agent)
		
		if ( netconfSession == None ):
			
			self.idNetconf+=1

			try:
				# create it
				session = SessionNetconf(agent, self.user)
			
				# start it ( send capabilities )
				session.start()

				# add it to the sessions NetConf list
				self.sessionsNetconf.append(session)
				
				# return the new session
				return session

			except Exception, exp:
				print str(exp)
				return None

		else:
			# return the existing session
			return netconfSession
	
	
	def getNetconf(self,agent):
		"""
			Return the requested NetConf session.
			@type  adr : string
			@param adr : The IP address to use
			@type  port : int
			@param port : The port to use
			@rtype: SessionNetconf
			@return: The requested Session
		"""
		# return the NetConf session for this agent if exists or None
		for sessionNetconf in self.sessionsNetconf:
			if sessionNetconf.getAgent() == agent:
				return sessionNetconf
		return None
		
			
				
	def closeCurrentNetconfSession(self):
		"""
			Close the requested Netconf session
			@type  adr : string
			@param adr : The IP address to use
			@type  port : int
			@param port : The port to use
		"""
		self.closeNetconfSession(self.currentNetconfSession)
		#self.currentNetconfSession.close()
		#self.sessionsNetconf.remove(self.currentNetconfSession)
				
	def closeNetconfSession(self, ns):
		ns.close()
		self.sessionsNetconf.remove(ns)


	def getAgents(self):
		"""
			Return the agent list managed by this user.
			@rtype: Agents list
			@return: The list of managed agent.
		"""
		agents=[]
		
		for session in self.sessionsNetconf:
			agents.append(session.getAgent())
		return agents
