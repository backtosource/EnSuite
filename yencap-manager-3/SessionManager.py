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

from SessionHTTP import *

class SessionManager:

	instance = None
	
	# sessions HTTP list
	sessionsHTTP = {}
	
		
 	def stopManager(self):
		"""
			Stop the SessionManager
		"""	
		# Stop all sessionHTTP 
		for sessionID in self.sessionsHTTP.keys():
  			self.sessionsHTTP[sessionID].closeHTTP()
			del self.sessionsHTTP[sessionID]	
	
# SessionHTTP Management  #
	
	
	def openSessionHTTP(self,sessionID, user):
		"""
			Creates a new SessionHTTP and appends it to the sessions list.
			@type sessionID : int
			@param sessionID : The session ID for this Session HTTP
		"""	
		# create a new session HTTP for the session_id only if not exists
		
		if ( self.getSessionHTTP(sessionID) == None ):
			# create HTTP session
			session = SessionHTTP(sessionID, user)
			# open HTTP session
			session.start()
			# add this session to the session list
			self.sessionsHTTP[sessionID] = session
			
		
	def getSessionHTTP(self,sessionID):
		"""
			Return the requested SessionHTTP
			@type  sessionID  : int
			@param sessionID : sessionID of the requested SessionHTTP 
			@rtype: SessionHTTP
			@return: The requested SessionHTTP
		"""	
		# if the user with this session_id has already a session HTTP opened
		if ( self.sessionsHTTP.has_key(int(sessionID))):
			# return his session HTTP
			return self.sessionsHTTP[int(sessionID)]
		else:
			# retrun None
			return None
			
		
	def closeSessionHTTP(self,sessionID):
		"""
			Close requested SessionHTTP.
			@type  sessionID : int
			@param sessionID : The session ID for the requested Sesssion ID
		"""	
		# get the session HTTP for this user
		session = self.getSessionHTTP(sessionID)
		# if exists
		if ( session != None ):
			# close it	
			session.closeHTTP()
			# delete it from the session list
			del self.sessionsHTTP[int(sessionID)] 
		
		
# Singleton : only one instance of the SessionManager		
def getInstance():
	if SessionManager.instance == None:
		SessionManager.instance = SessionManager()
	return SessionManager.instance
