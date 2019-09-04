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

from BaseHTTPServer import HTTPServer
import os, socket
from SocketServer import BaseServer
from OpenSSL import SSL
from Constants import C


class SecureHTTPServer(HTTPServer):

	def __init__(self, server_address, HandlerClass):
		BaseServer.__init__(self, server_address, HandlerClass)
		ctx = SSL.Context(SSL.SSLv23_METHOD)
		#server.pem's location (containing the server private key and
		#the server certificate).
		fpem = C.YENCAP_MAN_CONF_HOME + '/server.pem'
		ctx.use_privatekey_file (fpem)
		ctx.use_certificate_file(fpem)
		self.socket = SSL.Connection(ctx, socket.socket(self.address_family, self.socket_type))
		self.server_bind()
		self.server_activate()
		
		os.chdir(C.YENCAP_MAN_WWW_FILE)

