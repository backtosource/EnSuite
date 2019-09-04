###############################################################################
#                                                                             #
# YencaPManager software, LORIA-INRIA LORRAINE, MADYNES RESEARCH TEAM         #
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

from AgentConnectedPage import AgentConnectedPage
from Forms.FormDeleteConfig import FormDeleteConfig
from Nodes.AgentInfo import AgentInfo
from Nodes.Info import Info
from Nodes.NetconfReply import NetconfReply
from Nodes.AppletNode import AppletNode


class AgentPage(AgentConnectedPage):


	def __init__(self, httpSession, agent, error, netconfReply, info):

		AgentConnectedPage.__init__(self, httpSession, agent, error, netconfReply, info)

		self.addContent(AgentInfo(self.agent))
		if self.info != "":
			self.addContent(Info(self.info))
		if self.netconfReply != "":
				self.addContent(NetconfReply(self.netconfReply))
		else:
			data = "<h2>Agent Capabilities</h2><table>"
			for capa in self.agent.getCapabilities():
				data = data + "<tr><td>" + capa + "</td></tr>"
			data = data + "</table>"
			# YANG 17/6/9
			if not agent.isYangOk():
				data = data + "<h2> Yang errors</h2><table>" + agent.getYangErrMesg() + "</table>"
			elif agent.isYangEnabled():
				data = data + "<h2> Yang modules validated</h2><table>"
				for yang in agent.yangmodules:
					data = data + "<tr><td>" + yang + "</td></tr>"
				data = data + "</table>"
			# YANG 17/6/9
			self.addContent(Info(data))
