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

### Cyrille CORNU - 26/08/2009
# Page where the applet is displayed.

from AgentConnectedPage import AgentConnectedPage
from Nodes.AppletNode import AppletNode
from Nodes.Node import Node

class YangPage(AgentConnectedPage):
   

    def __init__(self, httpSession, agent, error, netconfReply, info):

        AgentConnectedPage.__init__(self, httpSession, agent, error, netconfReply, info)

        title = Node()
        title.addContent("""<h2>Yang Browsing</h2>""")
        self.addContent(title)
        agentIP = httpSession.currentNetconfSession.getAgent().getIp()
        self.addContent(AppletNode(""" CODE="applet.YangApplet.class" ARCHIVE="YangApplet.jar" HEIGHT=600 WIDTH=700 """,{"agentIP":""+agentIP}))
        