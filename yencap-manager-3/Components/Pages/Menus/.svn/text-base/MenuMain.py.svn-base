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

class MenuMain(Node):
	"""
		
	"""

	def __init__(self, filter_ip = "Not filtered", filter_function = "Not filtered", filter_status = "Not filtered", filter_capabilities = "Not filtered"):
		Node.__init__(self)

		self.addContent("<form method='POST' class='operation' enctype='multipart/form-data'><ul>")

		self.addContent(self.getIPPart(filter_ip))
		self.addContent(self.getFunctionPart(filter_function))
		self.addContent(self.getStatusPart(filter_status))
		self.addContent(self.getCapabilitiesPart(filter_capabilities))

		self.addContent("""
		<li><br/><center><input type="image" src="/Images/system-searchL.png" name="operation" value="filter" title="filter"/></center></li>
		<li><p><strong>HELP</strong><br/>Apply filters to choose the Netconf devices that fit your management requirements. (Ex: 192.*.0.*)</p></li>
		</ul>
		<input type="hidden" name="page" value="1">
		</form>""")


	def getIPPart(self, filter_ip):

		res = "<li><a href=\"#\">Device name or IP</a></li><li><input type=\"text\" name=\"filter_ip\" value=\"" + filter_ip + "\"/></li>"
		return res


	def getFunctionPart(self, filter_function):

		res = "<li><a href=\"#\">Function</a></li><li><SELECT name=\"filter_function\">"

		# Should be fetched from the parser instead... To Be Done...
		functions = ["Not filtered", "router", "server", "workstation"]

		for function in functions:
			if function == filter_function:
				res = "%s<OPTION value=\"%s\" selected>%s</OPTION>" % (res, function, function)
			else:
				res = "%s<OPTION value=\"%s\">%s</OPTION>" % (res, function, function)

		res = "%s</SELECT></li>" % (res)

		return res


	def getStatusPart(self, filter_status):

		res = "<li><a href=\"#\">Status</a></li><li><SELECT name=\"filter_status\">"

		# Should be fetched from the parser instead... To Be Done...
		statuss = ["Not filtered", "unreachable", "reachable", "connected"]
		
		for status in statuss:
			if status == filter_status:
				res = "%s<OPTION value=\"%s\" selected>%s</OPTION>" % (res, status, status)
			else:
				res = "%s<OPTION value=\"%s\">%s</OPTION>" % (res, status, status)
			
		res = "%s</SELECT></li>" % (res)

		return res


	def getCapabilitiesPart(self, filter_capabilities):
		
		res = "<li><a href='#'>Capabilities</a></li><li><SELECT name='filter_capabilities'>"
		
		capabilitiess = ["Not filtered", "urn:ietf:params:netconf:base:1.0", "urn:ietf:params:netconf:capability:writable-running:1.0", "urn:ietf:params:netconf:capability:candidate:1.0", "urn:ietf:params:netconf:capability:startup:1.0", "urn:ietf:params:netconf:capability:url:1.0?protocol=ftp", "urn:ietf:params:netconf:capability:xpath:1.0", "urn:madynes:params:xml:ns:netconf:capability:rbac:1.0"]
		
		for capability in capabilitiess:
			if capability == filter_capabilities:
				res = "%s<OPTION value='%s' selected>%s</OPTION>" % (res, capability, capability)
			else:
				res = "%s<OPTION value='%s'>%s</OPTION>" % (res, capability, capability)
			
		res = "%s</SELECT></li>" % (res)

		return res

		
	
