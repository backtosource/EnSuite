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


class Node:
	"""
		
	"""

	def __init__(self):
		self.content = []

	def getContent(self):
		return self.content
	
	def addContent(self, data):
		self.content.append(data)

	def toString(self):
		return ''.join(self.getContent())
		#return str(self.content)
		
	def addSourceForm(self):
		self.addContent("""Source:<br/>
		<input type="radio" name="source" value="running" checked/>running
		<input type="radio" name="source" value="candidate"/>candidate
		<input type="radio" name="source" value="startup"/>startup<br/>""")

	def addTargetForm(self):
		self.addContent("""Target:<br/>
		<input type="radio" name="target" value="running" checked/>running
		<input type="radio" name="target" value="candidate"/>candidate
		<input type="radio" name="target" value="startup"/>startup<br/>""")

	def addOperationForm(self, opname):
		self.addContent("<input type='hidden' name='operation' value='%s'>" % opname)
		self.addContent("<input type='submit' value='%s'/>" % opname)


