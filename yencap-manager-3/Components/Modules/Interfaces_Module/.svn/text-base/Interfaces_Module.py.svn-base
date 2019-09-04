###############################################################################
#                                                                             #
# YencaP software, LORIA-INRIA LORRAINE, MADYNES RESEARCH TEAM                #
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

from Components.Modules.Module import Module
import time
from Constants import C

class Interfaces_Module(Module):


	def doPost(self, args):
		config = "<netconf xmlns='urn:loria:madynes:ensuite:yencap:1.0' xmlns:xc='urn:ietf:params:xml:ns:netconf:base:1.0'><network><interfaces xmlns='urn:loria:madynes:ensuite:yencap:module:Interfaces:1.0'><interface xc:operation='merge'><name>%s</name><mtu>%s</mtu><ipv4><broadcast>%s</broadcast><netmask>%s</netmask><address-v4>%s</address-v4></ipv4></interface></interfaces></network></netconf>" % (args['ifname'], args['mtu'], args['broadcast'], args['netmask'], args['address-v4'])
				
		attr = {'target' : 'running' , 'config' : config}
		tstart = time.time()
		netconfReply = self.netconfSession.sendRequest('edit-config',attr)
		tend = time.time()
		tdiff = tend-tstart
		return netconfReply, tdiff




