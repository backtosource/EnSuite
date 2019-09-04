import os

from Ft.Xml.Domlette import NonvalidatingReader, implementation
from Ft.Xml import XPath, EMPTY_NAMESPACE
from Ft.Xml.Domlette import NonvalidatingReader, PrettyPrint

#from Modules.modulereply import ModuleReply 
#from Modules.module import Module 
import OLSR_Parser
from constants import C


HNA_PARAMETER = 1
IPC_PARAMETER = 2

class Generator:
    
 def __init__(self, namespace):
     self.namespace = namespace

 def addQuotes(self, word):
    new_word =  '"' + word + '"'
    return new_word

 def treatInterfaces(self, file, interfaces):
    for interface in interfaces.childNodes:
        if interface.nodeType == interface.ELEMENT_NODE:
            if interface.nodeName == "interface":
                for parameter_name in interface.childNodes:
                    if parameter_name.nodeType == parameter_name.ELEMENT_NODE:
                        if parameter_name.nodeName == "name":
                            name = self.transformCaseUp(interface.nodeName)
                            value = self.addQuotes(parameter_name.childNodes[0].nodeValue)
                            file.write(name + ' ' + value+'\n')
                            file.write('{\n')                            
                        elif parameter_name.nodeName == "linkQualityMult":
                            if len(parameter_name.childNodes) == 2:
                                linkto, multiplier = parameter_name.childNodes[0], parameter_name.childNodes[1]
                                name = self.transformCaseUp(parameter_name.nodeName)
                                file.write(name + ' ' + linkto.childNodes[0].nodeValue + ' ' + multiplier.childNodes[0].nodeValue + '\n')
                        else:
                            name = self.transformCaseUp(parameter_name.nodeName)
                            value = parameter_name.childNodes[0].nodeValue
                            file.write(name + ' ' + value+'\n')
                file.write('}\n\n')
                            
    return



 def treatHostCollector(self, file, hosts):
    """
        writes each individual host specific for IpcConnect into the configuration file
        under the format:    Host     Host_address
        hosts - represents the root node for all IpcConnect, Host related information in the xml tree
    """
    for host in hosts:
        if host.nodeType == host.ELEMENT_NODE:
            if host.nodeName == "host":
                if len(host.childNodes) == 1:
                    address = host.childNodes[0]
                    file.write(self.transformCaseUp(host.nodeName) + ' ' + address.childNodes[0].nodeValue + '\n')
    return


 def treatNetworkCollector(self, file, networks, parameter):
    """
        writes each individual network specific for IpcConnect or Hna4/Hna6 into the configuration file
        under the format:    Net_address Net_mask (for Hna4/6) and Net  Net_address Net_mask (for IpcConnect)
        networks - represents the root node for all IpcConnect/Hna4/Hna6, Network related information in the xml tree
    """
    for network in networks:
        if network.nodeType == network.ELEMENT_NODE:
            if network.nodeName == "network":
                if len(network.childNodes) == 2:
                    address, mask = network.childNodes[0], network.childNodes[1]
                    if parameter == HNA_PARAMETER:
                        file.write(address.childNodes[0].nodeValue + ' ' + mask.childNodes[0].nodeValue + '\n')
                    elif parameter == IPC_PARAMETER:
                        file.write('Net' + ' ' + address.childNodes[0].nodeValue + ' ' + mask.childNodes[0].nodeValue + '\n')
    return

 def treatHna4(self, file, hna4):
    name = self.transformCaseUp(hna4.nodeName)
    file.write(name+'\n'+'{'+'\n')
    if len(hna4.childNodes) == 1:
        networks = hna4.childNodes[0]
        if networks.nodeType == networks.ELEMENT_NODE:
            if networks.nodeName == "networks":
                self.treatNetworkCollector(file, networks, HNA_PARAMETER)
    file.write('}\n\n')

 def treatHna6(self, file, hna6):
    name = self.transformCaseUp(hna6.nodeName)
    file.write(name+'\n'+'{'+'\n')
    if len(hna6.childNodes) == 1:
        networks = hna6.childNodes[0]
        if networks.nodeType == networks.ELEMENT_NODE:
            if networks.nodeName == "networks":
                self.treatNetworkCollector(file, networks, HNA_PARAMETER)
    file.write('}\n\n')


 def treatIpcConnect(self, file, ipcconnect):
    name = self.transformCaseUp(ipcconnect.nodeName)
    file.write(name+ '\n' + '{' + '\n')
    for node in ipcconnect.childNodes:
        if node.nodeType == node.ELEMENT_NODE:
            if node.nodeName == "maxConnections":
                name = self.transformCaseUp(node.nodeName)
                value = node.childNodes[0].nodeValue
                file.write(name + ' ' + value+'\n')
            elif node.nodeName == "networks":
                self.treatNetworkCollector(file, node, IPC_PARAMETER)
            elif node.nodeName == "hosts":
                self.treatHostCollector(file, node)
    file.write('}\n\n')
    

 def treatLinkQualityDijkstraLimit(self, file, link_quality):
    name = self.transformCaseUp(link_quality.nodeName)
    if len(link_quality.childNodes) == 2:
        max_hops, update_period = link_quality.childNodes[0], link_quality.childNodes[1]
        file.write(name + ' ' + max_hops.childNodes[0].nodeValue + ' ' + update_period.childNodes[0].nodeValue + '\n')



 def transform(self, rootNode):
    """
        method that treats the OLSR related xml subtree;
        node values are written in to the configuration file
    """ 
    f = open(C.OLSR_CONFIG_FILE_NAME, 'w')
    for node in rootNode.childNodes:
        if node.nodeType == node.ELEMENT_NODE:
            if node.nodeName == "interfaces":
                self.treatInterfaces(f, node)
            elif node.nodeName == "hna4":
                self.treatHna4(f, node)
            elif node.nodeName == "hna6":
                self.treatHna6(f, node)
            elif node.nodeName == "ipcConnect":
                self.treatIpcConnect(f, node)
            elif node.nodeName == "linkQualityDijkstraLimit":
                self.treatLinkQualityDijkstraLimit(f, node)
            else:
                name = self.transformCaseUp(node.nodeName)
                value = node.childNodes[0].nodeValue
                f.write(name + ' ' + value+'\n')
    f.close()
    


 def transformCaseUp(self, word):
    
    return word[0].capitalize() + word[1:]
