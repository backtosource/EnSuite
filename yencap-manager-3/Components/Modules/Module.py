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

from Ft.Xml.Domlette import NonvalidatingReader, PrettyPrint
from Ft.Xml import XPath, InputSource
from Ft.Xml.Xslt import Processor, DomWriter
from Components.Pages.Nodes.Node import Node
import util
from Constants import C
import SessionManager

class Module(Node):

	def __init__(self, name, path, namespace, httpSessionId):
		Node.__init__(self)
		self.name = name
		self.path = path
		self.namespace = namespace
		self.httpSession = SessionManager.getInstance().getSessionHTTP(httpSessionId)
		self.netconfSession = self.httpSession.getCurrentNetconfSession()
		self.xsldocuri = "//%s/Components/Modules/%s/%s.xsl"%(C.YENCAP_MAN_HOME,self.name,self.name)
		self.title = "Module %s"%(self.name)


	def doGet(self):
		operation = 'get-config'
		attr = {'type' : 'xpath', 'filter' : self.path, 'source' : 'running'}

		netconfReply = self.netconfSession.sendRequest(operation,attr)
		tmp = self.applyXSLT(netconfReply)
		self.content = "<h2>%s</h2>%s" % (self.title, tmp)

	def doPost(self, args):
		pass

	def applyXSLT(self, netconfReply):
		try:
			# Generate a stylesheet equivalent to the edit-config
			df = InputSource.DefaultFactory
			xmldoc = df.fromString(netconfReply, 'urn:dummy')
			xsldoc = df.fromUri("file:"+self.xsldocuri, 'urn:sty')
			p = Processor.Processor()
			p.appendStylesheet(xsldoc)
			wr = DomWriter.DomWriter()
			p.run(xmldoc, writer=wr)
			newHTMLDoc = wr.getResult()
			
			# Copy the new document over the old one
			return util.convertNodeToString(newHTMLDoc.documentElement)

		except Exception,exp:
			import traceback
			traceback.print_exc()
			return "Exception while applying XSLT of module %s: \n%s" % (self.name, str(exp))
			

