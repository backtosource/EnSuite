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

class FormCopyConfig(Node):
	"""
		
	"""

	def __init__(self):
		Node.__init__(self)
		self.addContent("""<h2>Copy configuration</h2><p><ul>""")

		tmp = ModuleManager.getInstance().prefixes
		for key, value in tmp.items():
			self.addContent("<li>%s: %s</li>" %  (key, value))

		self.addContent("</ul><form method='POST' class='operation' enctype='multipart/form-data'>")
		self.addSourceForm()
		self.addContent("""<input type="radio" name="source" value="config"/>config (inline)
		<br/>Inline configuration:<br/> 
		<textarea name="inlineconfig" rows="20" cols="70"><ycp:netconf""")
		
		# Prepare textarea content to help people doing a subtree filtering request:
		attlist = ""
		for key, value in tmp.items():
			attlist = attlist + " xmlns:%s='%s'" %  (key, value)

		self.addContent(attlist)
		self.addContent(">\n\n")
		self.addContent("</ycp:netconf></textarea><br/>")
		self.addTargetForm()
		self.addOperationForm("copy-config")
		self.addContent("</form></p>")

