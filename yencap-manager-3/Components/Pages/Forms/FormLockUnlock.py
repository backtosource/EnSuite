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

class FormLockUnlock(Node):
	"""
		
	"""

	def __init__(self, agent):

		Node.__init__(self)

		self.addContent("""
		<h2>Lock/Unlock configuration</h2>
		<p>Locking a configuration allows to avoid conflicts between different updates from multiple Netconf sessions.
		<form method="POST" class="operation" enctype="multipart/form-data">""")
		
		self.addTargetForm()
		self.addContent("""
		<input type="image" src="/Images/emblem-readonlyL.png" name="operation" value="lock" title="lock"/>
		<input type="image" src="/Images/dialog-passwordL.png" name="operation" value="unlock" title="unlock"/>
		</form>
		</p>
		""")
