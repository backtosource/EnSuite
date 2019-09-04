###############################################################################
#                                                                             #
# YencaPManager software, LORIA-INRIA LORRAINE, MADYNES RESEARCH TEAM         #
# Copyright (C) 2005  Jerome BOURDELLON                                       #
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
#   Name : Jerome Bourdellon, Vincent CRIDLIG                                 #
#   Email: Vincent.Cridlig@loria.fr                                           #
#                                                                             #
###############################################################################

from Authentification import * 
from cStringIO import StringIO
from Components.Pages import pageFactory
import AgentManager, SessionManager, Parser
import cgi, time, socket
from SimpleHTTPServer import SimpleHTTPRequestHandler
from Components.Modules import ModuleManager
from Ft.Xml.Domlette import NonvalidatingReader
from Constants import C
from Ft.Xml.Domlette import  PrettyPrint

	
class SecureHTTPRequestHandler(SimpleHTTPRequestHandler):

	# Authentification class
	auth = Authentification()
	
	# XML Parser instance
	parser = Parser.getInstance()
	
	# HTTP Session Manager instance
	sessionMGR = SessionManager.getInstance()
	
	# AgentManager instance
	agentMGR = AgentManager.getInstance()
	
	# List of operations
	netconfOperations = ['request', C.GET_CONFIG, C.GET, C.COPY_CONFIG, C.DELETE_CONFIG, C.EDIT_CONFIG, C.LOCK                                                                                                                                                                                                                  , C.UNLOCK, C.KILL_SESSION, 'manage-mib-modules', 'rbac', C.COMMIT, C.DISCARD_CHANGES, C.VALIDATE]


	def setup(self):
		self.connection = self.request
		self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
		self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)


	def do_GET(self):
		"""
			Handle HTTP GET request.
		"""
		
		try:
			#print self.headers
			agent = None
			httpSession = None
			sessionID = self.headers.getheader(C.COOKIE)
			
			pf = pageFactory.getInstance()

			if ( sessionID != None):
				sessionID = sessionID[sessionID.index('=')+1:]
				
				httpSession = self.sessionMGR.getSessionHTTP(str(sessionID))
				if httpSession!= None:
					netconfSession = httpSession.getCurrentNetconfSession()
					if netconfSession != None:
						agent = netconfSession.getAgent()

					l = self.path.split("?")
					if len(l) == 2:
						m = l[1].split("&")
						dictio = {"filter_ip" : "Not filtered", "filter_function" : "Not filtered", "filter_status" : "Not filtered", "filter_capabilities" : "Not filtered", "page" : 1}
						for elem in m:
							param = elem.split("=")
							if len(param) == 2:
								name = param[0]
								value = param[1].replace('%20', ' ')
								dictio[name] = value
								
						self.wfile.write(pf.getPage("/main", httpSession, agent, dictio = dictio))
					else:
						self.wfile.write(pf.getPage(self.path, httpSession, agent))
							
				else:
					if self.path in ['/style.css',"/Images/background_big.gif","/Images/selector_sub.gif","/Images/header_big.gif"]:
						self.wfile.write(pf.getPage(self.path, httpSession, agent))
					else:
						self.wfile.write(pf.getPage('/login', httpSession, agent))
			else:
				if self.path in ['/style.css',"/Images/background_big.gif","/Images/selector_sub.gif","/Images/header_big.gif"]:
					# Static pages are allowed even if no session is open
					self.wfile.write(pf.getPage(self.path, httpSession, agent))
				else:
					# Otherwise forward to login page to open a HTTP session
					self.wfile.write(pf.getPage('/login', httpSession, agent))
			
		except IOError,exp:
			self.wfile.write(str(exp))
	
	
	def do_POST(self):
		"""
			 Handle the POST request
		"""
		try:
			
			# get content of Post request
			ctype, pdict = cgi.parse_header(self.headers['content-type'])
			
			# as a dictionnary
			rawData = dict(cgi.parse_multipart(self.rfile, pdict))
			
			args = {}
			# format the header ( delete "['" and "']" )
			for arg in rawData:
				args[arg] = str(rawData[arg])[2:-2]
				# manu 2/10/9 remove '\r \n \t' added by the form
				args[arg] = args[arg].replace('\\n','')
				args[arg] = args[arg].replace('\\r','')
				args[arg] = args[arg].replace('\\t','')
			# get the Session id
			sessionID = self.headers.getheader(C.COOKIE)
			if ( sessionID != None):
				args[C.COOKIE] = sessionID[sessionID.index('=')+1:]
			
			if args.has_key('operation'):
				self.dispatch(args['operation'],args)
			
		except IOError,exp:
			print exp
			self.wfile.write(open('error.html').read())
		
			
	def dispatch(self,operation,args):
		"""
			Dispatch request to the appropriate treatment.
			@type  operation : String
			@param operation: Request operation
			@type args : Dictionnary
			@param args : Dictionnary with the form args
		"""
		attr = {}
		pf = pageFactory.getInstance()
		
		# login operation at startup
		if ( operation == 'login' ):
			login = args['login']
			password = args['password']
			if login=="" or password=="":
				self.wfile.write(pf.getPage("", None, None, error="Login failed"))
				return

			user, session_id = self.auth.getSessionID(login,password)
			
			if ( session_id == None or user==None ):
				# if the couple login/password given is not correct
				# return index page another time
				self.wfile.write(pf.getPage("", None, None, error="Login failed"))
				return
				
			else:
				# if the couple login/password given is correct 
				# create a new Session HTTP for this user ( session_id)
				self.sessionMGR.openSessionHTTP(session_id, user)
				self.send_response(200)
 				self.send_header("Content-type", "text/html")
				# send a cookie with his session_id
				self.send_header("Set-cookie",'session_id=%s;'%(session_id))
 				self.end_headers()
				# return the Manager home page
				self.wfile.write(pf.getPage("/main", self.sessionMGR.getSessionHTTP(session_id)))
			
		elif ( operation == 'logout'):	
			# close HTTP sessions opened by this user
			httpSession = self.sessionMGR.getSessionHTTP(args[C.COOKIE])
			httpSession.closeHTTP()

		elif ( operation == 'filter'):
			# get the current HTTP session
			httpSession = self.sessionMGR.getSessionHTTP(args[C.COOKIE])

			# get the filter parameters	
			self.wfile.write(pf.getPage("/main", httpSession, None, dictio=args))

		elif ( operation == 'Add' ):
			# if the couple login/password given is not correct
			if ( self.auth.isValid(args['login-add'],args['password-add'])):
				self.parser.addAgent(args['adr'],args['port'],args['ssh-login'],args['ssh-password'])
			self.htmlFactory.getPage('Manager/add-agent.html',self.wfile)
			
		elif ( operation == 'Delete' ):
			# if the couple login/password given is not correct
			if ( self.auth.isValid(args['login-del'],args['password-del'])):
				agent = args['agents']
				adr = agent[:agent.index(':')]
				port = agent[agent.index(':')+1:]
				self.parser.removeAgent(adr,port)
			self.htmlFactory.getPage('Manager/delete-agent.html',self.wfile)

					
		elif ( operation == 'connect'):
			# get the Session HTTP for this user
			httpSession = self.sessionMGR.getSessionHTTP(args[C.COOKIE])

			if (not args.has_key('agentip')):
				self.wfile.write(pf.getPage("/main", httpSession, error="Please select at least one device."))
				return
			
			agents = args['agentip'].split("', '")
			
			if len(agents) == 0:
				self.wfile.write(pf.getPage("/main", httpSession))

			elif len(agents) == 1:
				agent = self.agentMGR.findAgentByIp(agents[0])
				
				if agent.getStatus() == "unreachable":
					# Must be replaced by a specific page for unreachable agents with a specific menu
					self.wfile.write(pf.getPage("/main", httpSession, agent=agent, error="Connection failed for Netconf agent " + agent.ip +" : unreachable<br/>"))

				# open a NetConf session to the given agent
				elif ( httpSession.openNetconf(agent) != None ):
					# return the desired agent home page
					httpSession.setCurrentNetconfSession(agent)
					self.wfile.write(pf.getPage("/agent", httpSession, agent=agent))
					
				else:
					# Connection failed
					self.wfile.write(pf.getPage("/agentreachable", httpSession, agent=agent, error="Connection failed"))

			else:
				message = ""
				for a in agents:
					agent = self.agentMGR.findAgentByIp(a)
					
					if agent.getStatus() == "reachable":
						connected = httpSession.openNetconf(agent)
						if connected == None:
							message = message + "Connection failed for Netconf agent " + agent.ip +".<br/>"

					else:
						message = message + "Connection failed for Netconf agent " + agent.ip +" : unreachable<br/>"

				if message != "":
					self.wfile.write(pf.getPage("/main", httpSession, error=message))
				else:
					self.wfile.write(pf.getPage("/main", httpSession))
			

		elif ( operation == 'disconnect'):
			# get the Session HTTP for this user
			httpSession = self.sessionMGR.getSessionHTTP(args[C.COOKIE])

			if (not args.has_key('agentip')):
				#if 'agentip' not in args.keys():
				self.wfile.write(pf.getPage("/main", httpSession, error="Please select at least one device."))
				return

			agents = args['agentip'].split("', '")
			
			if len(agents) == 0:
				self.wfile.write(pf.getPage("/main", httpSession))
			else:
				message = ""
				for a in agents:
					agent = self.agentMGR.findAgentByIp(a)
					netconfSession = httpSession.getNetconf(agent)
					if netconfSession != None:
						httpSession.closeNetconfSession(netconfSession)
					else:
						message = message + "Agent " + agent.ip + " was not connected.<br/>"

				if message != "":
					self.wfile.write(pf.getPage("/main", httpSession, error=message))
				else:
					self.wfile.write(pf.getPage("/main", httpSession))

			
		elif operation in self.netconfOperations:

			# get the current HTTP session
			httpSession = self.sessionMGR.getSessionHTTP(args[C.COOKIE])
			if httpSession == None:
				self.wfile.write(pf.getPage('/login'))
				return

			# get the NetConf session for this agent
			netconfSession = httpSession.getCurrentNetconfSession()
			if netconfSession == None:
				self.wfile.write(pf.getPage('/main', httpSession))
				return

			agent = netconfSession.getAgent()

			# get all args of the http request to create the netconf request
			if operation == C.GET:
				
				attr = {}
				t = args[C.TYPE]
				f = args[C.FILTER]
				if t=='' and f=='':
					self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Please fill all fields."))
					return
				if t == C.SUBTREE:
					# Test if XML subtree is well-formed.
					try:
						if f != '':
							fNode = NonvalidatingReader.parseString(f, 'http://madynes.loria.fr').documentElement
							attr[C.FILTER] = fNode
						else:
							attr[C.FILTER] = ''
					except Exception,exp:
						self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Subtree filter is not well formed : %s"%(str(exp))))
						return
				elif t == C.XPATH:
					f = f.replace('\\r', '').replace('\\n', '')
					attr[C.FILTER] = f

				attr[C.TYPE] = t

			elif operation == C.GET_CONFIG:
				attr = {}
				if args.has_key(C.SOURCE):
					s = args[C.SOURCE]
				else:
					self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Please fill all fields."))
					return
				t = args[C.TYPE]
				f = args[C.FILTER]
				if t=='' and f=='':
					self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Please fill all fields."))
					return
				if t == C.SUBTREE:
					# Test if XML subtree is well-formed.
					try:
						if f != '':
							fNode = NonvalidatingReader.parseString(f, 'http://madynes.loria.fr').documentElement
							attr[C.FILTER] = fNode
						else:
							attr[C.FILTER] = f
					except Exception,exp:
						self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Subtree filter is not well formed : %s"%(str(exp))))
						return
				elif t == C.XPATH:
					f = f.replace('\\r', '').replace('\\n', '')
					attr[C.FILTER] = f

				attr[C.TYPE] = t
				attr[C.SOURCE] = s

			elif operation == C.COPY_CONFIG:
				attr = {}
				if args.has_key(C.TARGET):
					attr[C.TARGET] = args[C.TARGET]
				else:
					self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Please fill all fields."))
					return
				s = args[C.SOURCE]
				if s=='':
					self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Please fill all fields."))
					return
				else:
					attr[C.SOURCE] = args[C.SOURCE]
					
				if args.has_key('inlineconfig'):
					inline = args['inlineconfig']

					# Test if XML inline config is well-formed.
					try:
						inlineNode = NonvalidatingReader.parseString(inline, 'http://madynes.loria.fr').documentElement
						attr["inlineconfig"] = inlineNode
					except Exception,exp:
						self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Inline config is not well formed : %s"%(str(exp))))
						return

			elif operation == C.VALIDATE:
				attr = {}
				s = args[C.SOURCE]
				if s=='':
					self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Please fill all fields."))
					return
				else:
					attr[C.SOURCE] = args[C.SOURCE]
					
				if args.has_key('inlineconfig'):
					inline = args['inlineconfig']

					# Test if XML inline config is well-formed.
					try:
						inlineNode = NonvalidatingReader.parseString(inline, 'http://madynes.loria.fr').documentElement
						attr["inlineconfig"] = inlineNode
					except Exception,exp:
						self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Inline config is not well formed : %s"%(str(exp))))
						return

			elif operation == C.DELETE_CONFIG:
				if args.has_key(C.TARGET):
					t = args[C.TARGET]
					attr = {C.TARGET : t}
				else:
					self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Please fill all fields."))
					return

			elif operation == C.EDIT_CONFIG:

				attr = {}

				if args.has_key(C.TARGET):
					attr[C.TARGET] = args[C.TARGET]
				else:
					self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Please fill all fields."))
					return

				s = args[C.SUBTREE]
				if s == '':
					self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Please fill all fields."))
					return
				else:
					# Test if XML subtree is well-formed.
					try:
						
						s = s.replace('\\r', '').replace('\\n', '').replace('\\t', '')
						print s
						fNode = NonvalidatingReader.parseString(s, 'http://madynes.loria.fr').documentElement
						attr[C.CONFIG] = fNode
					except Exception,exp:
						self.wfile.write(pf.getPage(self.path, httpSession, agent, error="config element is not well formed : %s"%(str(exp))))
						return

				if args.has_key(C.DEFAULT_OPERATION):
					do = args[C.DEFAULT_OPERATION]
					if do in [C.MERGE, C.REPLACE, C.NONE]:
						attr[C.DEFAULT_OPERATION] = do
					else:
						self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Default operation is not set appropriately."))
						return
				
				if args.has_key(C.ERROR_OPTION):
					eo = args[C.ERROR_OPTION]
					if eo in [C.STOP_ON_ERROR, C.CONTINUE_ON_ERROR, C.ROLLBACK_ON_ERROR]:
						attr[C.ERROR_OPTION] = eo
					else:
						self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Error option is not set appropriately."))
						return

				if args.has_key(C.TEST_OPTION):
					to = args[C.TEST_OPTION]
					if to in [C.TEST_THEN_SET, C.SET]:
						attr[C.TEST_OPTION] = to
					else:
						self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Test option is not set appropriately."))
						return

			elif operation in [C.LOCK, C.UNLOCK]:
				if args.has_key(C.TARGET):
					t = args[C.TARGET]
					attr = {C.TARGET : t}
				else:
					self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Please fill all fields."))
					return

			elif operation == C.KILL_SESSION:
				attr = {C.SESSION_ID : args[C.SESSION_ID]}

			elif (operation == 'manage-mib-modules'):
				if args['mmOp'] in ['undeploy','load','unload']:
					attr = {'mmOp' : args['mmOp'], 'name' : args['name']}
				else:
					attr = {'mmOp' : args['mmOp'], 'name' : args['name'], C.XPATH : args[C.XPATH], 'namespace' : args['namespace'], 'pref' : args['pref'], 'cachelifetime' : args['cachelifetime'], 'file' : args['file']}

			elif (operation == 'rbac'):
				attr = {'rbacOp' : args['rbacOp'], 'roleName' : args['roleName']}
				
			elif (operation == 'request'):
				attr=args['request']
			
		
			# Send Netconf request and store Netconf reply
			tstart = time.time()
			
			print operation
			print attr
			
			netconfReply = netconfSession.sendRequest(operation,attr)
			tend = time.time()
			tdiff = tend-tstart
			
			

			# Return the response from the agent or the HTML page containing it
			info = "Netconf request done in %s s." % str(tdiff)

			### CORNU - 25/08/09
			# The manager send only the raw netconf reply and print it if 'noHTML' option is present
			if args.has_key('noHTML'):
				self.wfile.write(netconfReply)
				print "reponse recue:\n"+netconfReply
			else:
				self.wfile.write(pf.getPage("/agent", httpSession, agent=netconfSession.getAgent(), netconfReply=netconfReply, info=info))
			###

		elif ( operation == 'Apply'):
			
			# get the current HTTP session
			httpSession = self.sessionMGR.getSessionHTTP(args[C.COOKIE])

			# get the NetConf session for this agent
			netconfSession = httpSession.getCurrentNetconfSession()

			mManager = ModuleManager.getInstance()
			module = mManager.getModuleInstance(args['module'], httpSession)
			if module != None:
				netconfReply, tdiff = module.doPost(args)

				agent = netconfSession.getAgent()
				info = "Netconf request done in %s s." % str(tdiff)
				# html = pf.getPage("/agent", httpSession, agent=agent, netconfReply=netconfReply, info=info)
				html = pf.getPage("/modules/"+module.name, httpSession, agent=agent, netconfReply=netconfReply, info=info)
				self.wfile.write(html)
			else:
				self.wfile.write(pf.getPage(self.path, httpSession, agent, error="Module could not be loaded."))
				return

		else:
			# get the current HTTP session
			httpSession = self.sessionMGR.getSessionHTTP(args[C.COOKIE])
			# This should never happen
			self.wfile.write(pf.getPage("/main", httpSession, error="Unknown operation."))

