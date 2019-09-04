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

import Parser
from DeviceStatusManager import DeviceStatusManager


class AgentManager:

	instance = None
	
	# agents list
	agents = []
	
	def __init__(self):
		self.agents = Parser.getInstance().getAgents()
		dsm = DeviceStatusManager(self.agents)
		dsm.start()
		
		
	def findAgentByIp(self, ip):
		for agent in self.agents:
			if (agent.getIp() == ip):
				return agent
		return None
		

	def refreshAllAgentStatus(self):
		for agent in self.agents:
			agent.refreshStatus()
		
		
# Singleton : only one instance of the SessionManager		
def getInstance():
	if AgentManager.instance == None:
		AgentManager.instance = AgentManager()
	return AgentManager.instance
