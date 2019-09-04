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
#   Name : Cristian POPI                                                      #
#   Email: Cristian.Popi@loria.fr                                             #
#                                                                             #
###############################################################################

from Ft.Xml.Domlette import implementation,PrettyPrint
from Ft.Xml import EMPTY_NAMESPACE
#import Grammar 
import os
import sys
import string
from constants import C

#OLSR_CONFIG_FILE_NAME = "/home/popicris/workspace/Yencap_Mesh/src/yencap/Modules/OLSR_Module/test_olsrd.conf"
#OLSR_CONFIG_FILE_NAME = "/etc/olsrd.conf"

# important seperator/comment variables
comment_characters = ['#', ';']  # items must be 1 char long
config_seperator = '\n'
individual_seperator = '='


class Parser:
    
    def __init__(self, namespace):
        #list of keys that identify (key, value) type of parameters
        self.general_command_list = ["DebugLevel",
                             "IpVersion",
                             "AllowNoInt",
                             "TosValue",
                             "Willingness",
                             "UseHysteresis",
                             "HystScaling",
                             "HystThrHigh",
                             "HystThrLow",
                             "Pollrate",
                             "TcRedundancy",
                             "MprCoverage",
                             "LinkQualityLevel",
                             "ClearScreen",
                             "LinkQualityFishEye",
                             "LinkQualityWinSize"
                             ]
        
        #list of keys that identify (key, value, value, ...) type of parameters
        self.general_command_list_special = ["LinkQualityDijkstraLimit"]
        
        #list of commands that identify a block of parameters
        self.block_command_list = ["IpcConnect",
                                   "Hna4",
                                   "Hna6",
                                   "Interface",
                                   "LoadPlugin"
                                   ]
        
        #list of parameters for a specific interface
        self.interface_parameter_list = ["Ip4Broadcast",
                                         "Ip6AddrType",
                                         "Ip6MulticastSite",
                                         "Ip6MulticastGlobal",
                                         "HelloInterval",
                                         "HelloValidityTime",
                                         "TcInterval",
                                         "TcValidityTime",
                                         "MidInterval",
                                         "MidValidityTime",
                                         "HnaInterval",
                                         "HnaValidityTime",
                                         "Weight"
                                         ]
        
        #list of special parameters for a specific interface
        self.interface_parameter_list_special = ["LinkQualityMult"]
        
        #list of parameters for an IpcConnect block
        self.ipcConnect_parameter_list = ["MaxConnections",
                                          "Host",
                                          "Net"]
        self.interface_name = []
        
        self.namespace = namespace
        
        
        
    def parse(self):
        doc = implementation.createDocument(self.namespace, None, None)
        olsr = doc.createElementNS(self.namespace,"olsr")
        doc.appendChild(olsr)
        self.parseConfigFile(doc, olsr, self.namespace)
        return doc
    
    def parseConfigFile(self, doc, olsr, namespace):
        """
            Parse an OLSR configuration file
            @type  name : string
            @param name : Configuration file to use
            @rtype: XML Node
            @return: Corresponding XML node for the file
        """
        
        #doc = implementation.createDocument(namespace, None, None)
        #olsr = doc.createElementNS(namespace,"OLSR")
        #doc.appendChild(olsr)
            
        f = open(C.OLSR_CONFIG_FILE_NAME, 'r')
        lines = f.readlines()
        f.close()
        #strip lines of white spaces at the beginning and end,
        #and drop lines that begin with a comment symbol or are empty
        lines = filter(lambda x: x != '' and not(x.startswith('#')), map(lambda x: x.strip(), lines))
        no_of_lines = len(lines)
        i = 0
        while i < no_of_lines:
            clean_line = lines[i]
            try:
                    #build a list of all words in the line (split by white characters; ie. white space or tabs)
                    words = clean_line.split()
                    #interpret the meaning of the first word
                    if words[0] in self.general_command_list:
                        #add a regular (key, value) parameter to the xml doc
                        xml_element = self.transform_case(words[0])
                        element = doc.createElementNS(namespace, xml_element)
                        olsr.appendChild(element)
                        
                        text = doc.createTextNode(words[1])
                        element.appendChild(text)
                        i+=1
                        
                    elif words[0] in self.general_command_list_special:
                        #add a parameter which takes two values - the maximum number of hops away from the node, and the update period
                        xml_element = self.transform_case(words[0])
                        element = doc.createElementNS(namespace, xml_element)
                        olsr.appendChild(element)
                        
                        hops_element = doc.createElementNS(namespace, "maxHops")
                        element.appendChild(hops_element)
                        
                        text = doc.createTextNode(words[1])
                        hops_element.appendChild(text)
                        
                        update_element = doc.createElementNS(namespace, "updatePeriod")
                        element.appendChild(update_element)
                        
                        text = doc.createTextNode(words[2])
                        update_element.appendChild(text)
                        i+=1
                     
                    elif words[0] in self.block_command_list:
                        #for the case of interface block parameters, store the interface name
                        #first check that this interface has not already been configured
                        if words[0] == "Interface":
                            if words[1] in self.interface_name:
                                print "Configuration file error: Interface %s is declared more than once in the configuration file " %words[1]
                                sys.exit()
                            self.interface_name.append(words[1])
                        #treat block configuration parameters
                        block_start_index, block_end_index = self.verify_block_syntax(lines, i)
                        #send the block content for parsing and addition to the xml tree
                        self.treat_BlockParameters(doc, olsr, namespace, words[0], lines[block_start_index+1:block_end_index])
                        #advance index after the end of the block to parse the following configuration parameter
                        i = block_end_index + 1
                    else:
                        i+=1
                            
                        
                        
            except:
                raise
            
#        PrettyPrint(doc)


    def stripQuotations(self, word):
        return word.lstrip('"').rstrip('"')

    def transform_case(self, word):
        """
            transforms the first letter of a word into upper case
            @type name: string
            @param name: word
            @rtype: string
            @return: the input word with the first letter in low case
        """
        
        if word[0] in string.ascii_uppercase:
            leader = word[0]
            tail = string.lstrip(word, word[0])
            leader = string.lower(leader)
            word = [leader, tail]
            word = string.join(word, '')
        return word
    
    def verify_block_syntax(self, lineList, current_line):
        """
            Check the correctedness of the block declaration in the configuration file
            @type  name : List of strings
            @param name : List of lines in the configuration file
            @rtype: Integer
            @return: Line indexes in the list that correspond to the beginning - ending of the block
        """
        
        begin = end = False
        start_index = end_index = current_line
        while not (begin and end):
            current_line += 1
            line = lineList[current_line]
            if line == '{':
                    if begin:
                        print "configuration file syntax error: encountered two { symbols before }"
                        sys.exit()
                    begin = True
                    start_index = current_line
            elif line == '}':
                    if not begin:
                        print "configuration file syntax error: encountered a } symbol before a { symbol"
                        sys.exit()
                    end = True
                    end_index = current_line
            else:
                    if not begin:
                        print "configuration file syntax error: block declared but not opened with a { symbol"
                        sys.exit()
        return start_index, end_index
    
    def treat_BlockParameters(self, doc, olsr, namespace, block_command, ParameterLineList):
        if block_command == "Hna4":
            #this is the case for a Hna4 parameters block
            self.treat_Hna4BlockParameters(doc, olsr, namespace, block_command, ParameterLineList)
        
        elif block_command == "Hna6":
            #this is the case for a Hna6 parameters block
            self.treat_Hna6BlockParameters(doc, olsr, namespace, block_command, ParameterLineList)
            
        elif block_command == "Interface":
            #this is the case for an Interface parameters block
            self.treat_InterfaceBlockParameters(doc, olsr, namespace, block_command, ParameterLineList)
        
        elif block_command == "IpcConnect":
            #this is the case for an Interface parameters block
            self.treat_IpcConnectBlockParameters(doc, olsr, namespace, block_command, ParameterLineList)
            
        elif block_command == "LoadPlugin":
            #this is the case for an Interface parameters block
            self.treat_LoadPlugin(doc, olsr, namespace, block_command, ParameterLineList)
            
                
    
    def treat_Hna4BlockParameters(self, doc, olsr, namespace, block_command, ParameterLineList):
            #first check that an Hna4 element doesn't already exist
            hna4 = self.create_UniqueChildElement(doc, olsr, namespace, "hna4")
            if len(ParameterLineList) > 0:
                networks = self.create_UniqueChildElement(doc, hna4, namespace, "networks")
                for network in ParameterLineList:
                    network_param = network.split()
                    net_addr, net_mask = network_param[0:]
                    
                    #create a network element
                    net_element = doc.createElementNS(namespace, "network")
                    networks.appendChild(net_element)
                        
                    #create a network address element
                    net_addr_element = doc.createElementNS(namespace, "address")
                    net_element.appendChild(net_addr_element)
                    
                    #add the address value to the network address element
                    addr_text = doc.createTextNode(net_addr)
                    net_addr_element.appendChild(addr_text)
                    
                    #create a network mask element
                    net_mask_element = doc.createElementNS(namespace, "mask")
                    net_element.appendChild(net_mask_element)
                    
                    #add the mask value to the network address element
                    mask_text = doc.createTextNode(net_mask)
                    net_mask_element.appendChild(mask_text)
                    
                    
    def treat_Hna6BlockParameters(self, doc, olsr, namespace, block_command, ParameterLineList):
            #first check that an Hna6 element doesn't already exist
            hna6 = self.create_UniqueChildElement(doc, olsr, namespace, "hna6")
            if len(ParameterLineList) > 0:
                networks = self.create_UniqueChildElement(doc, hna6, namespace, "networks")
                for network in ParameterLineList:
                    network_param = network.split()
                    net_addr, net_mask = network_param[0:]
                    
                    #create a network element
                    net_element = doc.createElementNS(namespace, "network")
                    networks.appendChild(net_element)
                        
                    #create a network address element
                    net_addr_element = doc.createElementNS(namespace, "address")
                    net_element.appendChild(net_addr_element)
                    
                    #add the address value to the network address element
                    addr_text = doc.createTextNode(net_addr)
                    net_addr_element.appendChild(addr_text)
                    
                    #create a network mask element
                    net_mask_element = doc.createElementNS(namespace, "mask")
                    net_element.appendChild(net_mask_element)
                    
                    #add the mask value to the network address element
                    mask_text = doc.createTextNode(net_mask)
                    net_mask_element.appendChild(mask_text)
                                    
    
    def treat_InterfaceBlockParameters(self, doc, olsr, namespace, block_command, ParameterLineList):

        interfaces = self.create_UniqueChildElement(doc, olsr, namespace, "interfaces")
        
        interface = doc.createElementNS(namespace, "interface")
        interfaces.appendChild(interface)
        
        iface_name = doc.createElementNS(namespace, "name")
        interface.appendChild(iface_name)
        
        clean_interface_name = self.stripQuotations(self.interface_name[-1])
        
        iface_name_text = doc.createTextNode(clean_interface_name)
        iface_name.appendChild(iface_name_text)
        
        if len(ParameterLineList) > 0:
                for ParamLine in ParameterLineList:
                    interface_param = ParamLine.split()
                    if len(interface_param) == 2:
                        xml_element = self.transform_case(interface_param[0])
                        element = doc.createElementNS(namespace, xml_element)
                        interface.appendChild(element)
                        
                        text = doc.createTextNode(interface_param[1])
                        element.appendChild(text)
                    elif interface_param[0] == "LinkQualityMult":
                        xml_element = self.transform_case(interface_param[0])
                        element = doc.createElementNS(namespace, xml_element)
                        interface.appendChild(element)
                        
                        link = doc.createElementNS(namespace, "linkTo")
                        element.appendChild(link)
                        
                        link_text = doc.createTextNode(interface_param[1])
                        link.appendChild(link_text)
                        
                        multiplier = doc.createElementNS(namespace, "multiplier")
                        element.appendChild(multiplier)
                        
                        multiplier_text = doc.createTextNode(interface_param[2])
                        multiplier.appendChild(multiplier_text)
                    else:
                        print "configuration file error: unrecognized (parameter, value) pair: %s" %interface_param[0]
    
    def treat_IpcConnectBlockParameters(self, doc, olsr, namespace, block_command, ParameterLineList):
        ipcConnect = self.create_UniqueChildElement(doc, olsr, namespace, "ipcConnect")
        if len(ParameterLineList) > 0:
                for ParamLine in ParameterLineList:
                    ipc_param = ParamLine.split()
                    if ipc_param[0] == "MaxConnections":
                        connections_element = doc.createElementNS(namespace, "maxConnections")
                        ipcConnect.appendChild(connections_element)
                        
                        connections_text = doc.createTextNode(ipc_param[1])
                        connections_element.appendChild(connections_text)
                        
                    elif ipc_param[0] == "Host":
                        hosts = self.create_UniqueChildElement(doc, ipcConnect, namespace, "hosts")
        
                        host = doc.createElementNS(namespace, "host")
                        hosts.appendChild(host)
                        
                        address = doc.createElementNS(namespace, "address")
                        host.appendChild(address)
                        
                        address_text = doc.createTextNode(ipc_param[1])
                        address.appendChild(address_text)
                        
                    elif ipc_param[0] == "Net":
                        networks = self.create_UniqueChildElement(doc, ipcConnect, namespace, "networks")
        
                        network = doc.createElementNS(namespace, "network")
                        networks.appendChild(network)
                        
                        address = doc.createElementNS(namespace, "address")
                        network.appendChild(address)
                        
                        address_text = doc.createTextNode(ipc_param[1])
                        address.appendChild(address_text)
                        
                        mask = doc.createElementNS(namespace, "mask")
                        network.appendChild(mask)
                        
                        mask_text = doc.createTextNode(ipc_param[2])
                        mask.appendChild(mask_text)
                        
                    else:
                        print "unknown parameter in IpcConnect block of configuration file: %s !" %ipc_paramm[0]
        
        
    def treat_LoadPluginParameters(self, doc, olsr, namespace, block_command, ParameterLineList):
        print "[LoadPlugin]"
        
    def create_UniqueChildElement(self, doc, parent_node, namespace, element_name):
        """
            checks if element_name is an element in doc
            if it doesn't exist, it creates a new element element_name
            in both cases it returns the elment_name element
            @rtype: Element
            @return: an element with a qualified name of element_name
        """
        
        #get a list containing node names out of the childNodes objects list for the doc node
        #if the element_name is among childNodes return the object corresponding to element_name
        element = filter(lambda x: x.localName == element_name, parent_node.childNodes)
        if len(element) == 1:
            return element[0]
        #if an element_name node does not exist, reate one, link it to its parent and return it
        element = doc.createElementNS(namespace, element_name)
        parent_node.appendChild(element)
        return element
