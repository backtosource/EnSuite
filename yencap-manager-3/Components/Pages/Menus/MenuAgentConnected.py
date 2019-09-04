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

### Cyrille CORNU - 26/08/2009
# Add "Yang Browsing" in the menu.

from Components.Pages.Nodes.Node import Node
from Components.Modules import ModuleManager

class MenuAgentConnected(Node):
	"""
		
	"""

	def __init__(self, agent):
		Node.__init__(self)
		self.addContent("<ul><li><a href='/main'>Back to main menu</a></li><li><a href='/agent'>%s</a></li><li><a href='/role'>Role (de)activation</a></li><li><a href='/modules'>Modules</a></li><li><ul>" % agent.getIp())

		# Setup Module Menu
		mManager = ModuleManager.getInstance()
		dictio = mManager.modules
		for capability in agent.getCapabilities():
			for moduleName in dictio.keys():
				namespace = dictio[moduleName]["namespace"]
				if namespace == capability:
					self.addContent("<li><a href='/modules/%s'>%s</a></li>\n" % (moduleName,moduleName))

		self.addContent("""</ul>
          </li>
          <li><a href='#'>Standard operations</a></li>
          <li>
            <ul>""")
		
		# add manu 16/9/9
		
		if agent.isYangEnabled():
			self.addContent("""
              <li><a href='/yang'>Yang Browsing</a></li>
              """)
		
		# add manu 16/9/9
		
		self.addContent("""
              <li><a href='/lock'>Lock/Unlock</a></li>
              <li><a href='/copy'>Copy Configuration</a></li>
              <li><a href='/delete'>Delete Configuration</a></li>
              <li><a href='/kill'>Kill Session</a></li>
              <li><a href='/xpath'>XPath Filtering</a></li>
              <li><a href='/subtree'>Subtree Filtering</a></li>
              <li><a href='/edit'>Edit Configuration</a></li>
            </ul>
          </li>
          <li><a href='#'>Capabilities</a></li>
          <li>
            <ul>
              <li><a href='/candidate'>Candidate</a></li>
              <li><a href='/validate'>Validate</a></li>
            </ul>
          </li>
          <li><a href='/close'>Close Session</a></li>
        </ul>
		""")
