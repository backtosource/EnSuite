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

class FormModuleManagement(Node):
	"""
		
	"""

	def __init__(self):
		Node.__init__(self)

		self.addContent("""
		
		<h2>Deploy/Undeploy module</h2>
		<p>
			<ul>
				<li><i>Deploy</i> installs the module in the Netconf agent.</li>
				<li><i>Undeploy</i> uninstalls the module in the Netconf agent.</li>
			</ul>
		<form method="POST" class="operation" enctype="multipart/form-data">
		Please set the module parameters:<br/>
		<table>
    	<tr><td align="right">Name:</td><td align="left"><input type="text" name="name" value="Foo"/></td></tr>
		<tr><td align="right">Xpath:</td><td><input type="text" name="xpath" value="/ycp:netconf/fp:foo"/></td></tr>
		<tr><td align="right">Namespace:</td><td><input type="text" name="namespace" value="urn:loria:madynes:ensuite:yencap:module:Foo:1.0"/></td></tr>
		<tr><td align="right">Prefered prefix:</td><td><input type="text" name="pref" value="fp"/></td></tr>
		<tr><td align="right">Cache lifetime</td><td><input type="text" name="cachelifetime" value="100"/></td></tr>
		<tr><td align="right">Upload module file (tar.gz):</td><td><input type="file" name="file"/></td></tr>
		</table>
		<input type="hidden" name="operation" value="manage-mib-modules">
		<input type="submit" name="mmOp" value="deploy"/>
		<input type="submit" name="mmOp" value="undeploy"/>
		</form>
		</p>

		<h2>Load/Unload module</h2>
		<p>
			<ul>
				<li><i>Load</i> will load the module in the Netconf agent. The module must exist in the agent.</li>
				<li><i>Unload</i> will unload the module from the Netconf agent. But the module still exist.</li>
			</ul>
		Please set the module parameters:<br/>
		<form method="POST" class="operation" enctype="multipart/form-data">
    	<input type="text" name="name" value="Foo"/><br/>
		<input type="hidden" name="operation" value="manage-mib-modules">
		<input type="image" src="/Images/edit-redoL.png" name="mmOp" value="load" title="load"/>
		<input type="image" src="/Images/edit-undoL.png" name="mmOp" value="unload" title="unload"/>
		</form>
		</p>
		""")

