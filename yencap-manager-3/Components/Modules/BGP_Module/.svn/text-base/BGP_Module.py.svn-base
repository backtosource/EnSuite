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


class BGP_Module(Module):

	def doPost(self, args):

		if args["object"] == "as-number":
			config = "<netconf xmlns='urn:loria:madynes:ensuite:yencap:1.0' xmlns:xc='urn:ietf:params:xml:ns:netconf:base:1.0'><routing><bgp xmlns='urn:loria:madynes:ensuite:yencap:module:BGP:1.0'><bgprouter><%s xc:operation='%s'>%s</%s></bgprouter></bgp></routing></netconf>" % (args['object'], args['bgpoperation'], args['ASnumber'], args['object'])

		elif args["object"] == "neighbors":
			config = "<netconf xmlns='urn:loria:madynes:ensuite:yencap:1.0' xmlns:xc='urn:ietf:params:xml:ns:netconf:base:1.0'><routing><bgp xmlns='urn:loria:madynes:ensuite:yencap:module:BGP:1.0'><bgprouter><%s><%s xc:operation='%s'><ip-address>%s</ip-address><remote-as>%s</remote-as></%s></%s></bgprouter></bgp></routing></netconf>" % (args['object'], 'neighbor', args['bgpoperation'], args['neighborIpAddress'], args['neighborRemoteAs'], 'neighbor', args['object'])

		elif args["object"] == "route-maps":
			config = "<netconf xmlns='urn:loria:madynes:ensuite:yencap:1.0' xmlns:xc='urn:ietf:params:xml:ns:netconf:base:1.0'><routing><bgp xmlns='urn:loria:madynes:ensuite:yencap:module:BGP:1.0'><filters> <route-map xc:operation='%s'><map-tag>%s</map-tag><sequences><seq-number>%s</seq-number><state>%s</state><match><as-path><as-path-name>%s</as-path-name></as-path></match></sequences></route-map></filters></bgp></routing></netconf>" % (args['bgpoperation'], args['maptag'], args['seqnumber'], args['state'], args['aspathname'])

		elif args["object"] == "afneighbors":
			config = "<netconf xmlns='urn:loria:madynes:ensuite:yencap:1.0' xmlns:xc='urn:ietf:params:xml:ns:netconf:base:1.0'><routing><bgp xmlns='urn:loria:madynes:ensuite:yencap:module:BGP:1.0'><bgprouter><address-families><ipv4-address-family><neighbors><neighbor><ip-address>%s</ip-address><bind-filters xc:operation='%s'><route-map><name>%s</name><direct>%s</direct></route-map></bind-filters></neighbor></neighbors></ipv4-address-family></address-families></bgprouter></bgp></routing></netconf>" % (args['neighborIpAddress'], args['bgpoperation'], args['name'], args['direct'])
		else:
			return None, 0
			
		cNode = NonvalidatingReader.parseString(config, 'http://madynes.loria.fr').documentElement
		
		attr = {'target' : 'running' , 'config' : cNode}
		tstart = time.time()
		netconfReply = self.netconfSession.sendRequest('edit-config',attr)
		tend = time.time()
		tdiff = tend-tstart
		return netconfReply, tdiff





