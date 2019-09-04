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

class C:

####### YencaManager variables #######

	# YencaManager directories

	#YENCAP_MAN_HOME='/usr/local/ensuite/yencap-manager'

	YENCAP_MAN_HOME="/root/workspace/yencap-manager"

	#YENCAP_MAN_CONF_HOME = "/etc/ensuite/yencap-manager"

	YENCAP_MAN_CONF_HOME = "/root/workspace/yencap-manager/conf"

	YENCAP_MAN_WWW_FILE='%s/www'%(YENCAP_MAN_HOME)
	
	YENCAP_MAN_YANG_HOME='%s/yang'%(YENCAP_MAN_HOME)
	
	# Namespace

	#MADYNES_NS='netconf:fr:loria:madynes'
	NETCONF_NS='urn:ietf:params:xml:ns:netconf:base:1.0'
	YENCAP_XMLNS = "urn:loria:madynes:ensuite:yencap:1.0"
		
	#NS = { 'netconf' : NETCONF_NS , 'madynes' : MADYNES_NS }
	
	# YencaManager variables used by (at least) sessionSSH:
	SUCCESS = 1
	FAILED = 0
	
	# YencaManager File

	CONFIG_FILE = '%s/config.xml'%(YENCAP_MAN_CONF_HOME)

	HELLO_URI = '%s/capabilities.xml'%(YENCAP_MAN_CONF_HOME)
	
	# Netconf port mapping
	NETCONF_SSH_PORT = 830
	NETCONF_BEEP_PORT = 831
	NETCONF_SOAPHTTP_PORT = 832
	NETCONF_SOAPBEEP_PORT = 833

	NETCONF_SSH_SUBSYSTEM = "netconf"

	# OPERATIONS
	GET = "get"
	GET_CONFIG = "get-config"
	COPY_CONFIG = "copy-config"
	EDIT_CONFIG = "edit-config"
	DELETE_CONFIG = "delete-config"
	LOCK = "lock"
	UNLOCK = "unlock"
	VALIDATE = "validate"
	CLOSE_SESSION = "close-session"
	KILL_SESSION = "kill-session"
	SOURCE = "source"
	TARGET = "target"
	CONFIG = "config"

	RPC = "rpc"
	RPC_REPLY = "rpc-reply"
	CAPABILITY = "capability"
	CAPABILITIES = "capabilities"
	HELLO = "hello"
	URL = "url"
	FILTER = "filter"
	SUBTREE = "subtree"
	XPATH = "xpath"
	TYPE = "type"
	OK = "ok"
	SESSION_ID = "session-id"
	MESSAGE_ID = "message-id"
	DELIMITER = "]]>]]>"

	# Test options
	TEST_OPTION = "test-option"
	TEST_THEN_SET = "test-then-set"
	SET = "set"

	# Error options
	DEFAULT_OPERATION = "default-operation"
	MERGE = "merge"
	REPLACE = "replace"
	NONE = "none"
	ERROR_OPTION = "error-option"
	STOP_ON_ERROR = "stop-on-error"
	CONTINUE_ON_ERROR = "continue-on-error"
	ROLLBACK_ON_ERROR = "rollback-on-error"

	COMMIT = "commit"
	DISCARD_CHANGES = "discard-changes"

	COOKIE = "cookie"
