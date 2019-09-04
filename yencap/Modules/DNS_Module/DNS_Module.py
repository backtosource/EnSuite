#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os

from Modules.module import Module
from Modules.modulereply import ModuleReply 

from Ft.Xml.Domlette import NonvalidatingReader, implementation, PrettyPrint
from Ft.Xml.XPath.Context import Context
from Ft.Xml import XPath, EMPTY_NAMESPACE
from xml.dom import Node
from Ft.Xml.XPath import Evaluate

class DNS_Module(Module):
    

    def __init__(self, name, path, namespace, cacheLifetime, parameters):
        """
        Create an instance and initialize the structure needed by it.
        @type  parameters: dictionary
        @param parameters : should be a dictionary containning the follow keys
        """
        Module.__init__(self, name, path, namespace, cacheLifetime, parameters)
        
        
        
    def getConfig(self, configName):
        """
            Generate the interfaces XML configuration.
            @rtype: ModuleReply
            @return: the main node of the network interfaces.
            ** Relates to the netconf get-config operation
        """
        
        self.doc = implementation.createDocument(self.namespace, None, None)
        dnsnode = self.doc.createElementNS(self.namespace,"dns")
        self.doc.appendChild(dnsnode)
        
        listNs = self.getNameServers()
        if listNs != []:
            for dns in listNs:
                node = self.doc.createElementNS(self.namespace, "server")
                self.doc.documentElement.appendChild(node)
                server = self.doc.createTextNode(dns)
                node.appendChild(server)

        modulereply = ModuleReply(replynode=self.doc.documentElement)
        return modulereply




    def getNameServers(self, filename = "/etc/resolv.conf"):
        """ Get previously set nameservers """
        list = []

        try:
            f = file(filename, "r")
            for line in f.readlines():
                if line.strip().startswith("nameserver"):
                    list.append(line[line.find("nameserver") + 10:].rstrip('\n').strip())
            f.close()
        except IOError:
            return "Could not open file to read" # FIXME: return an error message here

        return list

    def setNameServers(self, *args):
        """ Set nameservers """
        try:
            f = file("/etc/resolv.conf", "w")
            for arg in args:
                data = "nameserver " + arg.strip() + '\n' 
                f.write(data)
            f.close()
        except IOError:
            return "Could not open file to write" # FIXME: return an error message here

        return 0
#
#if __name__ == "__main__":
#    n = nameserver()
#    print n.getNameServers()


