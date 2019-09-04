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
###############################################################################


import UserManager

class Authentification:

	userManager = UserManager.getInstance()
	
	# Session id
	session_id = 0
	
	
	def getSessionID(self,login,password):
		"""
			Return a session ID if the user is valid
			@type  login : String
			@param login : Login  for the user
			@type  password : String
			@param password : Password for the user
			@rtype: Int
			@return: The new Session ID
		"""
		
		# only if this user is valid
		valid, user = self.isValid(login,password)
		print valid
		if valid:
			# return a new session_id
			self.session_id+=1
			return user, self.session_id
		else:
			return False, None
			
	
	# Authentification method
	def isValid(self,login,password):
		"""
			Test is the user is valid
			@type  login : String
			@param login : Login  for the user
			@type  password : String
			@param password : Password for the user
			@rtype: int
			@return: The result if the test
		"""
		user = self.userManager.findUserByLogin(login)

		if user != None:
			if user.getPassword() == password:
				return True, user
		return False, None
