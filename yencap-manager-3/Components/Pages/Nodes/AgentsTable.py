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

from Node import Node
import AgentManager


class AgentsTable(Node):
	"""
		
	"""

	def __init__(self, httpSession, filter_ip = "Not filtered", filter_function = "Not filtered", filter_status = "Not filtered", filter_capabilities = "Not filtered", page=1):
		Node.__init__(self)

		self.addContent("""<SCRIPT LANGUAGE="JavaScript">
<!-- Begin
var checkflag = "false";
function check(field) {
if (checkflag == "false") {
  for (i = 0; i < field.length; i++) {
  field[i].checked = true;}
  checkflag = "true";
  return "Unselect all"; }
else {
  for (i = 0; i < field.length; i++) {
  field[i].checked = false; }
  checkflag = "false";
  return "Select all"; }
}
//  End -->
</script>

		<h2>List of all agents</h2>
		<p>This table contains all the Netconf agents that meet the filters.<br/>Display [ """)

		#<a href="">15</a> | <a href="">30</a> | <a href="">100</a> | <a href="">All</a> ] devices on one page.</p>
		self.addContent("<a href=\"/main?page=1&filter_ip="+filter_ip + "&filter_status="+filter_status + "&filter_capabilities="+filter_capabilities + "&filter_function="+filter_function + "&page_pref=15\">15</a> | ")
		self.addContent("<a href=\"/main?page=1&filter_ip="+filter_ip + "&filter_status="+filter_status + "&filter_capabilities="+filter_capabilities + "&filter_function="+filter_function + "&page_pref=30\">30</a> | ")
		self.addContent("<a href=\"/main?page=1&filter_ip="+filter_ip + "&filter_status="+filter_status + "&filter_capabilities="+filter_capabilities + "&filter_function="+filter_function + "&page_pref=100\">100</a> | ")
		self.addContent("<a href=\"/main?page=1&filter_ip="+filter_ip + "&filter_status="+filter_status + "&filter_capabilities="+filter_capabilities + "&filter_function="+filter_function + "&page_pref=All\">All</a> ] devices on one page.")

		self.addContent("""
		<form method="POST" class="operation" enctype="multipart/form-data">
		<table>
			<tr><th width="5%">&nbsp;</th><th width="20%">Device</th><th width="20%"><a href="" title="Last connection to the agent">Last access</a></th><th width="20%"><a href="" title="Sort by function">Function</a></th><th><a href="" title="Sort by status">Status</a></th></tr>""")

		connectedAgents = []
		for Netconfsession in httpSession.sessionsNetconf:
			connectedAgents.append(Netconfsession.getAgent())

		# Filtering parameters
		pref_nb_devices_per_page = httpSession.user.pref_nb_devices_per_page
		
		# Get all agents
		all_agents = AgentManager.getInstance().agents

		# Filter agents according to filter parameters
		agents =[]
		for agent in all_agents:
			#print "filter_ip : " + filter_ip
			#print "filter_status : " + filter_status
			#print filter_capabilities
			#print "filter_capabilities : " + filter_capabilities
			#print "filter_function : " + filter_function
			#print "agent_ip : " + agent.ip
			#print "agent_status : " + agent.getStatus()
			#print "agent_capabilities : " + str(agent.capabilities)
			#print "agent_function : " + str(agent.groups)
			a = self.selectedByIpFilter(filter_ip, agent)
			b = self.selectedByStatusFilter(filter_status, agent, connectedAgents)
			c = self.selectedByCapabilitiesFilter(filter_capabilities, agent)
			d = self.selectedByFunctionFilter(filter_function, agent)

			if (a & b & c & d):
				agents.append(agent)
				
		nb_agents = len(agents)

		if (pref_nb_devices_per_page == "All"):
			nb_pages = 1
		else:
			if nb_agents % pref_nb_devices_per_page != 0:
				nb_pages = nb_agents / pref_nb_devices_per_page + 1
			else:
				nb_pages = nb_agents / pref_nb_devices_per_page

			if nb_agents > pref_nb_devices_per_page:
				agents = agents[((page-1)*pref_nb_devices_per_page):(page*pref_nb_devices_per_page)]

		table = ""
		i = 0
		for agent in agents:

			connected = False
			if agent.getStatus()=="reachable":
				if agent in connectedAgents:
					connected = True

			if ((i % 2) == 0):
				table = table + "<tr bgcolor=\"#d7e5ef\">"
			else:
				table = table + "<tr>"
			i = i + 1

			table = table + "<td><input type=\"checkbox\" name=\"agentip\" value=\"" + str(agent.getIp()) + "\"/></td>"
			
			if agent.getStatus()=="unreachable":
				table = table + "<td><font color=\"red\">" + str(agent.getIp()) + "</td>"
				
			elif agent.getStatus()=="reachable":
				if connected:
					table = table + "<td><font color=\"green\">" + str(agent.getIp()) + "</font></td>"
				else:
					table = table + "<td><font color=\"orange\">" + str(agent.getIp()) + "</font></td>"
				
			table = table + """<td>2006-12-31 : 13h46</td>"""

			table = table + "<td>"
			for group in agent.groups:
				table = table + group + ", "

			table = table + "</td>"

			if agent.getStatus()=="unreachable":
				table = table + "<td>unreachable</td>"
			elif agent.getStatus()=="reachable":
				if agent in connectedAgents:
					table = table + "<td>connected</td>"
				else:
					table = table + "<td>reachable</td>"
			table = table + "</tr>"


		table = table + """<tr>
				<td>&nbsp;</td>
				<td><input type="button" value="Select all" onClick="this.value=check(this.form.agentip)"/></td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
		</table>"""

		self.addContent(table)

		tablecommande = """
		<table>
			<tr>
			<td>
			<input type="image" src="/Images/dialog-okL.png" name="operation" value="connect" title="connect"/>
			<input type="image" src="/Images/dialog-closeL.png" name="operation" value="disconnect" title="disconnect"/>
			<input type="image" src="/Images/document-openL.png" name="operation" value="edit" title="edit"/>
			<input type="image" src="/Images/edit-deleteL.png" name="operation" value="delete" title="delete"/>
			</td>
			<td>
			</tr>
		</table>"""

		pages = "<center>"

		for i in range(1,nb_pages+1):
			pages = pages + "<a href=\"/main?page=" + str(i) + "&filter_ip="+filter_ip + "&filter_status="+filter_status + "&filter_capabilities="+filter_capabilities + "&filter_function="+filter_function+"\">" + str(i) + "</a> "

		pages = pages + """
		</center>
		</form>
		</p>
		"""
		#<input type="hidden" name="operation" value="connect-agent"/>
		
		self.addContent(tablecommande + pages)


	def selectedByIpFilter(self, filter_ip, agent):

		if (filter_ip == "Not filtered"):
			return True

		sp_filter_ip = filter_ip.split(".")
		if len(sp_filter_ip) != 4:
			return False
		else:
			for item in sp_filter_ip:
				if item != "*":
					tmp = int(item)
					if ((tmp > 255) | (tmp < 0)):
						return False

		ip = agent.ip
		sp_ip = ip.split(".")
		res = True
		for i in range(0,4):
			res = res & ((sp_ip[i] == sp_filter_ip[i]) | (sp_filter_ip[i] == "*"))

		return res


	def selectedByStatusFilter(self, filter_status, agent, connectedAgents):

		a = (filter_status == "Not filtered")
		b = (str(agent.getStatus()) == filter_status)
		c = ((filter_status == "connected") & (agent in connectedAgents))

		return ( a | b | c )


	def selectedByCapabilitiesFilter(self, filter_capabilities, agent):

		return ((filter_capabilities in agent.getCapabilities()) | (filter_capabilities == "Not filtered"))


	def selectedByFunctionFilter(self, filter_function, agent):

		return ((filter_function in agent.groups) | (filter_function == "Not filtered"))


