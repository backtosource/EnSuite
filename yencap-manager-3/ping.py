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
#   Name : Vincent CRIDLIG                                                    #
#   Email: Vincent.Cridlig@loria.fr                                           #
#                                                                             #
###############################################################################

import os
from socket import *
import struct
import select
import time
import sys

ICMP_ECHO_REQUEST=8
myID=os.getpid() & 0xFFFF


class Pinger:
	"""
		Python implementation of ping
	"""

	def __init__(self, *dest):
		self.results={}
		icmp=getprotobyname("icmp")
		self.soc=socket(AF_INET,SOCK_RAW,icmp)
	
	def checksum(self, str):
		sum=0
		countTo=(len(str)/2)*2
		count=0
		while count<countTo:
			thisVal=ord(str[count+1])*256+ord(str[count])
			sum=sum+thisVal
			sum=sum & 0xffffffff # Necessary?
			count=count+2

		if countTo<len(str):
			sum=sum+ord(str[len(str)-1])
			sum=sum & 0xffffffff # Necessary?

		sum=(sum >> 16) + (sum & 0xffff)
		sum=sum+(sum >> 16)
		answer=~sum
		answer=answer & 0xffff

		# Swap bytes. Bugger me if I know why.
		answer=answer >> 8 | (answer << 8 & 0xff00)
		return answer

	def receivePings(self,timeout):
		timeLeft=timeout
		while 1:
			startedSelect=time.time()
			whatReady=select.select([self.soc],[],[],timeLeft)
			howLongInSelect=(time.time()-startedSelect)
			if whatReady[0]==[]: # Timeout
				return 
			timeReceived=time.time()
			recPacket,addr= self.soc.recvfrom(1024)
			icmpHeader=recPacket[20:28]
			
			type,code,checksum,packetID,sequence=struct.unpack("bbHHh",icmpHeader)
			if self.destDict.has_key(packetID):
				bytesInDouble=struct.calcsize("d")
				
				timeSent=struct.unpack("d",recPacket[28:28+bytesInDouble])[0]
				dT = timeReceived-timeSent
				self.results[self.destDict[packetID]]=dT
				# print self.destDict[packetID], dT
				del self.destDict[packetID]
				if len(self.destDict)==0:
					return
				
			timeLeft=timeLeft-howLongInSelect
			if timeLeft<=0:
				return 
	
	def sendPings(self):
		for ID, dest in self.destDict.items():
			# Header is type (8), code (8), checksum (16), id (16), sequence (16)
			myChecksum=0
			# Make a dummy heder with a 0 checksum.
			header=struct.pack("bbHHh",ICMP_ECHO_REQUEST,0,myChecksum, ID,1)
			bytesInDouble=struct.calcsize("d")
			data=(192-bytesInDouble) * "Q"
			data=struct.pack("d",time.time())+data
			# Calculate the checksum on the data and the dummy header.
			myChecksum=self.checksum(header+data)
			# Now that we have the right checksum, we put that in. It's just easier
			# to make up a new header than to stuff it into the dummy.
			
			header=struct.pack("bbHHh",ICMP_ECHO_REQUEST,0,htons(myChecksum), ID,1)
			packet=header+data
			self.soc.sendto(packet,(dest,1)) # Don't know about the 1
	
	def ping(self, destAddr,timeout=1):
		# Returns either the delay (in seconds) or none on timeout.
		dest=[]
		for n in destAddr:
			dest.append(gethostbyname(n))
		self.destDict={}
		cnt=3 # Started at 3 for no good reason
		for d in destAddr:
			self.destDict[cnt]=d
			cnt+=1
			
		self.sendPings()
		self.receivePings(timeout)
		self.soc.close()
		return self

