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

class FormLogin(Node):
	"""
		
	"""

	def __init__(self):
		Node.__init__(self)

		self.addContent("""
		<h2>Welcome to YencaPManager.</h2>
		<p><br/>Please fill the login information.<br/><br/>
		<form method="POST" class="operation" enctype="multipart/form-data">
		<table border="0">
		<tr><td align="right" width="30%">Login</td><td align="left"><input type="text" name="login" value=""/></td><tr/>
		<tr><td align="right" width="30%">Password</td><td align="left"><input type="password" name="password" value=""/></td><tr/>
		<tr><td align="right" width="30%">&nbsp;</td><td align="left"><input type="hidden" name="operation" value="login">
		<input type="reset" value="reset"/>
		<input type="submit" value="login"/></td><tr/>
		</table>
		</form>
		</p>
		""")
