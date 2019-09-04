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
# Node used to display an applet.

from Node import Node

class AppletNode(Node):

    def __init__(self,code,param={}):
        Node.__init__(self)
        htmlAppletCode = "<APPLET "+code+">"
        for key in param:
            htmlAppletCode = htmlAppletCode + "<PARAM NAME="+key+" VALUE="+param[key]+">" 
        htmlAppletCode = htmlAppletCode + "</APPLET>"
        self.addContent(htmlAppletCode)
        self.addContent("""<p>If you cannot run this java applet, please <a href="http://www.java.com/download/">download Java Virtual Machine</a>.""")
        