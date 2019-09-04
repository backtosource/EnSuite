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

class FormEditConfig(Node):
	"""
		
	"""

	def __init__(self):
		Node.__init__(self)
		
		
		# Prepare textarea content to help people doing a subtree filtering request:
		attlist = ""
		tmp = ModuleManager.getInstance().prefixes
		for key, value in tmp.items():
			attlist = attlist + " xmlns:%s=\"%s\"" %  (key, value)

		attlist = attlist + " xmlns:xc=\"urn:ietf:params:xml:ns:netconf:base:1.0\""
		
		self.addContent("""
		<h2>Edit the configuration</h2>
		<p>This form allows to build a customized edit-config operation with all possible options.
		<form method="POST" class="operation" enctype="multipart/form-data">
		Target:<br/>
		<input type="radio" name="target" value="running" checked/>running
		<input type="radio" name="target" value="candidate"/>candidate
		<input type="radio" name="target" value="startup"/>startup<br/>
		Default operation:<br/>
		<input type="radio" name="default-operation" value="merge" checked/>merge
		<input type="radio" name="default-operation" value="replace"/>replace
		<input type="radio" name="default-operation" value="none"/>none<br/>
		Error option:<br/>
		<input type="radio" name="error-option" value="stop-on-error" checked/>Stop on error
		<input type="radio" name="error-option" value="continue-on-error"/>Continue on error
		<input type="radio" name="error-option" value="rollback-on-error"/>Rollback on error<br/>
		Error option:<br/>
		<input type="radio" name="test-option" value="test-then-set" checked/>Test then set
		<input type="radio" name="test-option" value="set"/>Set<br/>
		Edit config subtree:<br/>
		<textarea name="subtree" rows="20" cols="70"><ycp:netconf""" + attlist + ">\n\n" + """</ycp:netconf></textarea><br/>
		<input type="hidden" name="operation" value="edit-config">
		<input type="submit" value="edit-config"/>
		</form>
		</p>
		""")
