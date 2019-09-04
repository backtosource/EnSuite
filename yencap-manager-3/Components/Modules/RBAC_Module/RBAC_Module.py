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
from Ft.Xml.Domlette import NonvalidatingReader

class RBAC_Module(Module):

	#def __init__(self, httpSession):
	#	Module.__init__(self, httpSession)
	#	self.xsldocuri = "//%s/Components/Modules/RBAC/RBAC.xsl"%(C.YENCAP_MAN_HOME)
	#	self.path = '/ycp:netconf/ycp:security/ac:rbac'
	#	self.title = "Device's RBAC policy"


	def doPost(self, args):
		baseop = args['rbacoperation']
		start = "<netconf xmlns='urn:loria:madynes:ensuite:yencap:1.0' xmlns:xc='urn:ietf:params:xml:ns:netconf:base:1.0'><security>"
		end = "</security></netconf>"
		if args['object'] == 'Role':
			if baseop == 'Delete':
				config = "%s<rbac xmlns='urn:loria:madynes:ensuite:yencap:module:RBAC:1.0'><roles><role id='%s' xc:operation='delete'><name>%s</name></role></roles></rbac>%s" % (start, args['roleId'], args['name'], end)
			elif baseop == 'Create':
				config = "%s<rbac xmlns='urn:loria:madynes:ensuite:yencap:module:RBAC:1.0'><roles><role xc:operation='create'><name>%s</name></role></roles></rbac>%s" % (start, args['name'], end)
			elif baseop == 'Update':
				config = "%s<rbac xmlns='urn:loria:madynes:ensuite:yencap:module:RBAC:1.0'><roles><role id='%s'><name xc:operation='replace'>%s</name></role></roles></rbac>%s" % (start, args['roleId'], args['name'], end)

		elif args['object'] == 'User':
			if baseop == 'Delete':
				config = "%s<rbac xmlns='urn:loria:madynes:ensuite:yencap:module:RBAC:1.0'><users><user id='%s' xc:operation='delete'><login>%s</login></user></users></rbac>%s" % (start, args['userId'],args['login'], end)
			elif baseop == 'Create':
				config = "%s<rbac xmlns='urn:loria:madynes:ensuite:yencap:module:RBAC:1.0'><users><user xc:operation='create'><login>%s</login></user></users></rbac>%s" % (start, args['login'], end)
			elif baseop == 'Update':
				config = "%s<rbac xmlns='urn:loria:madynes:ensuite:yencap:module:RBAC:1.0'><users><user id='%s'><login xc:operation='replace'>%s</login></user></users></rbac>%s" % (start, args['userId'],args['login'], end)

		elif args['object'] == 'URA':
			if baseop == 'Delete':
				config = "%s<rbac xmlns='urn:loria:madynes:ensuite:yencap:module:RBAC:1.0'><user-assignements><user-assignement id='%s' xc:operation='delete' userRef='%s' roleRef='%s'/></user-assignements></rbac>%s" % (start, args['uraId'], args['userRef'],args['roleRef'], end)
			elif baseop == 'Create':
				config = "%s<rbac xmlns='urn:loria:madynes:ensuite:yencap:module:RBAC:1.0'><user-assignements><user-assignement xc:operation='create' userRef='%s' roleRef='%s'></user-assignement></user-assignements></rbac>%s" % (start, args['userRef'], args['roleRef'], end)
			elif baseop == 'Update':
				config = "%s<rbac xmlns='urn:loria:madynes:ensuite:yencap:module:RBAC:1.0'><user-assignements><user-assignement xc:operation='replace' id='%s' userRef='%s' roleRef='%s'></user-assignement></user-assignements></rbac>%s" % (start, args['uraId'], args['userRef'],args['roleRef'], end)
			#print config

		cNode = NonvalidatingReader.parseString(config, 'http://madynes.loria.fr').documentElement

		attr = {'target' : 'running' , 'config' : cNode}
		tstart = time.time()
		netconfReply = self.netconfSession.sendRequest('edit-config',attr)
		tend = time.time()
		tdiff = tend-tstart
		return netconfReply, tdiff



