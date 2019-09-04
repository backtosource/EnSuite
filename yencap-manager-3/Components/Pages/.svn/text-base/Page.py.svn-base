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

from Nodes.DivWrap import DivWrap
from Nodes.DivHeader import DivHeader
from Nodes.DivContent import DivContent
from Nodes.DivColumn1 import DivColumn1
from Nodes.DivColumn2 import DivColumn2
from Nodes.DivFooter import DivFooter
from Nodes.DivNav import DivNav
from Nodes.DivSidebar import DivSidebar
from Nodes.Error import Error


class Page:

	def __init__(self, httpSession, agent, error, netconfReply, info):
		self.httpSession = httpSession
		self.agent = agent
		
		self.divWrap = DivWrap()

		self.divHeader = DivHeader()
		self.divColumn1 = DivColumn1()
		self.divSidebar = DivSidebar()
		self.divContent = DivContent()
		self.divFooter = DivFooter()

		# divNav contains the menu node
		self.divNav = DivNav()
		self.divColumn1.add(self.divNav)

		# Add div HTML nodes to the main div composite (wrapper)
		self.divWrap.add(self.divHeader)
		self.divWrap.add(self.divColumn1)
		self.divWrap.add(self.divSidebar)
		self.divWrap.add(self.divContent)
		self.divWrap.add(self.divFooter)

		self.netconfReply = netconfReply
		self.info = info

		if error != "":
			self.addContent(Error(error))


	def addMenu(self, node):
		self.divNav.add(node)

	def addContent(self, node):
		self.divContent.add(node)

	def toString(self):
		start =  """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>YencaPManager</title>
<link rel="stylesheet" type="text/css" href="/style.css" media="all" />
</head>
<body>
		"""

		end = "</body>\n</html>"
		
		return "%s\n%s\n%s" % (start, self.divWrap.toString(), end)


