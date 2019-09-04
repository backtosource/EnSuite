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
from Ft.Xml.Domlette import NonvalidatingReader

class RIP_Module(Module):


	def doPost(self, args):
		
		if args["object"] == "redistribute":
			config = "<netconf xmlns='urn:loria:madynes:ensuite:yencap:1.0' xmlns:xc='urn:ietf:params:xml:ns:netconf:base:1.0'><routing><rip xmlns='urn:loria:madynes:ensuite:yencap:module:RIP:1.0'><redistribute><%s xc:operation='%s' metric='%s' route-map='%s'/></redistribute></rip></routing></netconf>" % (args['redistribute'], args['ripoperation'], args['metric'], args['route-map'])
			
		elif args["object"] == "networks":
			config = "<netconf xmlns='urn:loria:madynes:ensuite:yencap:1.0' xmlns:xc='urn:ietf:params:xml:ns:netconf:base:1.0'><routing><rip xmlns='urn:loria:madynes:ensuite:yencap:module:RIP:1.0'><%s><%s xc:operation='%s'>%s</%s></%s></rip></routing></netconf>" % (args['object'], "network", args['ripoperation'], args['network'], 'network', args['object'])
		elif args["object"] == "neighbors":
			config = "<netconf xmlns='urn:loria:madynes:ensuite:yencap:1.0' xmlns:xc='urn:ietf:params:xml:ns:netconf:base:1.0'><routing><rip xmlns='urn:loria:madynes:ensuite:yencap:module:RIP:1.0'><%s><%s xc:operation='%s'>%s</%s></%s></rip></routing></netconf>" % (args['object'], "neighbor", args['ripoperation'], args['neighbor'], 'neighbor', args['object'])
		elif args["object"] == "passive-interfaces":
			config = "<netconf xmlns='urn:loria:madynes:ensuite:yencap:1.0' xmlns:xc='urn:ietf:params:xml:ns:netconf:base:1.0'><routing><rip xmlns='urn:loria:madynes:ensuite:yencap:module:RIP:1.0'><%s><%s xc:operation='%s'>%s</%s></%s></rip></routing></netconf>" % (args['object'], "passive-interface", args['ripoperation'], args['passive-interface'], 'passive-interface', args['object'])
		elif args["object"] == "distribute-lists":
			config = "<netconf xmlns='urn:loria:madynes:ensuite:yencap:1.0' xmlns:xc='urn:ietf:params:xml:ns:netconf:base:1.0'><routing><rip xmlns='urn:loria:madynes:ensuite:yencap:module:RIP:1.0'><%s><%s xc:operation='%s' direct='%s' name='%s'>%s</%s></%s></rip></routing></netconf>" % (args['object'], "distribute-list", args['ripoperation'], args['direct'], args['name'], args['distribute-list'], 'distribute-list', args['object'])

		cNode = NonvalidatingReader.parseString(config, 'http://madynes.loria.fr').documentElement

		attr = {'target' : 'running' , 'config' : cNode}
		
		tstart = time.time()
		netconfReply = self.netconfSession.sendRequest(C.EDIT_CONFIG, attr)
		tend = time.time()
		tdiff = tend-tstart
		return netconfReply, tdiff




