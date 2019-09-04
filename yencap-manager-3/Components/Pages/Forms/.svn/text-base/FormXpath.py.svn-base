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

from Components.Pages.Nodes.Node import Node
from Components.Modules import ModuleManager

class FormXpath(Node):
	"""
		
	"""

	def __init__(self, agent):

		Node.__init__(self)

		self.addContent("""
		<h2>Get the configuration</h2>
		<p>If you perform a get request, the source will be silently ignored. To write request more easily, you can use the following defined namespace prefixes:<ul>""")

		tmp = ModuleManager.getInstance().prefixes
		for key, value in tmp.items():
			if value in agent.getCapabilities():
				self.addContent("<li>%s: %s</li>" %  (key, value))

		self.addContent("</ul><form method='POST' class='operation' enctype='multipart/form-data'>")
		self.addSourceForm()
		self.addContent("""XPath expression:<br/>
		<input type="text" size="50" name="filter" value="/ycp:netconf"/><br/>
		<input type="hidden" name="type" value="xpath">
		<input type="submit" name="operation" value="get"/>
		<input type="submit" name="operation" value="get-config"/>
		</form>
		</p>""")
