###############################################################################
#                                                                             #
# YencaP software, LORIA-INRIA LORRAINE, MADYNES RESEARCH TEAM                #
# Copyright (C) 2005  Vincent CRIDLIG                                         #
#                                                                             #
# This program is free software; you can redistribute it and/or               #
# modify it under the terms of the GNU General Public License                 #
# as published by the Free Software Foundation; either version 2              #
# of the License, or (at your option) any later version.                      #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program; if not, write to the Free Software                 #
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #
#                                                                             #
# Author Info:                                                                #
#   Name : Cristian POPI                                                      #
#   Email: Cristian.Popi@loria.fr                                             #
#                                                                             #
###############################################################################


import os, util

from Ft.Xml.Domlette import NonvalidatingReader, implementation
from Ft.Xml import XPath, EMPTY_NAMESPACE, InputSource
from Ft.Xml.Domlette import NonvalidatingReader, PrettyPrint

from Ft.Xml.Xslt import Processor, DomWriter

from Ft.Xml.XPath.Context import Context
from Ft.Xml import XPath, EMPTY_NAMESPACE
from xml.dom import Node
from Ft.Xml.XPath import Evaluate


from Modules.modulereply import ModuleReply 
from Modules.module import Module 
import OLSR_Parser
from generator import Generator
from OLSR_system import OLSR_System
from constants import C



metaFile = "//%s/Modules/meta.xsl"%(C.YENCAP_HOME)

class OLSR_Module(Module):
    """
        It is the main class of local system state data for the NetConf Agent.
    """
    
 
#   def __init__(self, namespace):
    def __init__(self, name, path, namespace, cacheLifetime, parameters):
        """
        Create an instance and initialize the structure needed by it.
        @type  parameters: dictionary
        @param parameters : should be a dictionary containning the follow keys
        """
        
        Module.__init__(self, name, path, namespace, cacheLifetime, parameters)
        
    
        
    

    def getConfig(self, configName):
        
        """
            the getConfig operation retrieves configuration data only
        """
        
        if configName in [C.STARTUP, C.RUNNING]:
            configFileParser = OLSR_Parser.Parser(self.namespace)
            get_config = configFileParser.parse()
            
#            print "[debug] =========parsed config==========="
#            PrettyPrint(get_config)
        
            if ( get_config != None):
                xmlreply = ModuleReply ( replynode = get_config.documentElement)
            else:
                xmlreply = ModuleReply(
                error_type=ModuleReply.APPLICATION,
                error_tag=ModuleReply.OPERATION_NOT_SUPPORTED,
                error_severity=ModuleReply.ERROR,
                error_message="Parser from Module %s replied with None." % self.name)    
        else:
            print "in getConfig: configuration is %s" %configName
            xmlreply = ModuleReply(
            error_type=ModuleReply.APPLICATION,
            error_tag=ModuleReply.OPERATION_NOT_SUPPORTED,
            error_severity=ModuleReply.ERROR,
            error_message="OPERATION-NOT-SUPPORTED: Module %s only supports startup configuration." % self.name)
        
        return xmlreply
    

#    def get(self, configName):
#        
#        """
#            the get operation retrieves both configuration and state data
#        """
#        
#        doc = implementation.createDocument(self.namespace, None, None)
#        olsr = doc.createElementNS(self.namespace,"olsr")
#        doc.appendChild(olsr)
#        
#        configFileParser = OLSR_Parser.Parser()
#        configFileParser.parseConfigFile(doc, olsr, self.namespace)
#        
#        modulereply = ModuleReply(replynode=doc.documentElement)
#        return modulereply


#    def copyConfig(self, sourceName, targetName, sourceNode = None):
#        """
#            Momentarily, the operation is not supported
#        """
#
#        xmlReply = ModuleReply(
#            error_type = ModuleReply.APPLICATION,
#            error_tag = ModuleReply.OPERATION_NOT_SUPPORTED,
#            error_severity = ModuleReply.ERROR,
#            error_message="OPERATION-NOT-SUPPORTED: Module %s only supports startup configuration." % self.name)
#        return xmlReply


    

    def editConfig(self, defaultoperation, testoption, erroroption, target, confignode, targetnode=None):
        """
        Apply a edit-config request from the confignode to the targetnode.
        @type defaultoperation: MERGE_OPERATION | REPLACE_OPERATION | NONE_OPERATION 
        @param defaultoperation : as specified in NETCONF protocol
        @type testoption : SET | TEST_AND_SET 
        @param testoption : as specified in NETCONF protocol
        @type erroroption : STOP_ON_ERROR | IGNORE_ERROR | ROLL_BACK_ON_ERROR 
        @param erroroption : as specified in NETCONF protocol
        @type target : RUNNING_TARGET | CANDIDATE_TARGET | STARTUP_TARGET
        @param target : as specified in NETCONF protocol
        @type targetnode : string
        @param targetnode : if the target is RUNNING_TARGET or STARTUP_TARGET it will be ignored otherwise should be the node of the CANDIDATE_TARGET that this module should procees
        @rtype: ModuleReply
        @return: It returns a success or error message.
        ** Relates to the netconf edit-config operation
        """

        try:
            # Generate a stylesheet equivalent to the edit-config
            df = InputSource.DefaultFactory
            editXMLRequest = df.fromString(util.convertNodeToString(confignode), 'urn:dummy')
            stylesheet = df.fromUri("file:"+metaFile, 'urn:sty')
            p = Processor.Processor()
            p.appendStylesheet(stylesheet)
            wr = DomWriter.DomWriter()
            p.run(editXMLRequest, writer=wr)
            generatedStyleSheet = wr.getResult()

            # Apply the generated stylesheet to the source document
            inputStyleSheet = df.fromString(util.convertNodeToString(generatedStyleSheet), 'urn:sty')
            oldXMLDocument = self.getConfig(target).getXMLNodeReply()
            inputDocument = df.fromString(util.convertNodeToString(oldXMLDocument), 'urn:dummy')
            p = Processor.Processor()
            p.appendStylesheet(inputStyleSheet)
            wr = DomWriter.DomWriter()
            p.run(inputDocument, writer=wr)
            newXMLDoc = wr.getResult()
            newOLSRRootNode = newXMLDoc.childNodes[0]
            
            # Copy the data to the olsr config file
            file_generator = Generator(self.namespace)
            file_generator.transform(newOLSRRootNode)

            print "new OLSR config is \n"
            PrettyPrint(newXMLDoc.childNodes[0])
            
            if ( newOLSRRootNode != None):
                xmlreply = ModuleReply ( replynode = newOLSRRootNode)
                
            else:
                xmlreply = ModuleReply(
                error_type=ModuleReply.APPLICATION,
                error_tag=ModuleReply.OPERATION_NOT_SUPPORTED,
                error_severity=ModuleReply.ERROR,
                error_message="Config generator from Module %s replied with None." % self.name)
                
            return xmlreply
            
            
            # (Re)start the olsr process on the device, if it is running
#            p = OLSR_System()
#            p.start_new_olsr_instance()
            
#            xmlReply = self.copyConfig("config", target, sourceNode = newXMLDoc)
#            return xmlReply

        except Exception,exp:
            print str(exp)
            moduleReply = ModuleReply(
            error_type=ModuleReply.APPLICATION,
            error_tag=ModuleReply.OPERATION_FAILED,
            error_severity=ModuleReply.ERROR,
            error_message=str(exp))
            return moduleReply
