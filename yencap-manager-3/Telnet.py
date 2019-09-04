###############################################################################
#                                                                             #
# YencaPManager software, LORIA-INRIA LORRAINE, MADYNES RESEARCH TEAM          #
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

import telnetlib

class Telnet:
	def __init__(self,host,login,password):
		self.tn = telnetlib.Telnet(host)
		self.tn.read_until('login: ')
		self.tn.write(login +'\n')
		self.tn.read_until('Password: ')
		self.tn.write(password +'\n')
		
		
	def ping(self,dest):
		"""
			Send a ping request to the specific host.
			@type  dest : String
			@param dest : The destination address for the ping command
			@rtype: String
			@return: The ping response
		"""
		self.tn.write('ping -c 4 %s\n'%(dest))
		self.tn.write('exit\n')
		resp = self.tn.read_all()
		return resp 
	
		
	def traceroute(self,dest):
		"""
			Send a traceroute request to the specific host.
			@type  dest : String
			@param dest : The destination address for the traceroute command
			@rtype: String
			@return: The traceroute response
		"""
		self.tn.write('traceroute %s\n'%(dest))
		self.tn.write('exit\n')
		resp = self.tn.read_all()
		return resp
	
