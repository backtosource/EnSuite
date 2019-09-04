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

from Components.Modules.Module import Module
import time
from Constants import C

class ASTERISK_Module(Module):


	def doGet(self):
		operation = 'get-config'
		# ASTERISK module only supports startup.
		attr = {'type' : 'xpath', 'filter' : self.path, 'source' : 'startup'}
		
		netconfReply = self.netconfSession.sendRequest(operation,attr)
		tmp = self.applyXSLT(netconfReply)
		self.content = "<h2>%s</h2>%s" % (self.title, tmp)


	def doPost(self, args):
		print "NOT YET IMPLEMENTED"



