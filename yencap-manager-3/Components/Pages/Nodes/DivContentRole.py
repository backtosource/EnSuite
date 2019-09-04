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

from Div import Div

class DivContentRole(Div):
	"""
		
	"""

	def __init__(self):
		self.content = """<form>
<table border="1" CELLSPACING=0 width="50%">
<tr>
  <td VALIGN="top">
    Choose Role
  </td>
  <td>
    <input type="text" name="role" value="startup"/><br/>
  </td>
</tr>
<tr>
  <td  ALIGN=center bgcolor="orange" colspan="2">
    <input type="submit" value="activate" />
    <input type="submit" value="deactivate"/>
  </td>
</tr>
</table>
</form>"""
		self.id = "content"
	
