###############################################################################
#                                                                             #
# YencaPManager software, LORIA-INRIA LORRAINE, MADYNES RESEARCH TEAM         #
# Copyright (C) 2005                                       #
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
#   Name : Frederic BECK                                                      #
#   Email: Frederic.Beck@loria.fr                                             #
#                                                                             #
###############################################################################


import os
from socket import *
import struct
import select
import time
import sys

ICMP_ECHO_REQUEST=128
ICMP_ECHO_REPLY=129
myID=os.getpid() & 0xFFFF

class Pinger6:
	pass

	def __init__(self):
		self.results={}
		self.destDict={}
		self.soc=socket(AF_INET6,SOCK_RAW, IPPROTO_ICMPV6)
	
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
			icmpHeader=recPacket[0:8]
			
			type,code,checksum,packetID,sequence=struct.unpack("BbHHh",icmpHeader)
			if type == ICMP_ECHO_REPLY:
				if self.destDict.has_key(sequence):
					bytesInDouble=struct.calcsize("d")
				
					timeSent=struct.unpack("d",recPacket[8:8+bytesInDouble])[0]
					dT = timeReceived-timeSent
					self.results[self.destDict[sequence]]=dT
					del self.destDict[sequence]
					if len(self.destDict)==0:
						return
				
			timeLeft=timeLeft-howLongInSelect
			if timeLeft<=0:
				return 
	
	def sendPings(self):
		for seq,dest in self.destDict.items():
			myChecksum=0
			header=struct.pack("BbHHh",ICMP_ECHO_REQUEST,0,htons(myChecksum), myID,seq)
			bytesInDouble=struct.calcsize("d")
			data=(192-bytesInDouble) * "Q"
			data=struct.pack("d",time.time())+data
			myChecksum=self.checksum(header+data)
			header=struct.pack("BbHHh",ICMP_ECHO_REQUEST,0,htons(myChecksum), myID,seq)
			packet=header+data
			self.soc.sendto(packet,(dest,0)) # Don't know about the 1
	
	def ping6(self, destAddr,timeout=1):
		dest=[]
		for n in destAddr:
			dest.append(n)

		cnt=1
		for d in destAddr:
			self.destDict[cnt]=d
			cnt=cnt+1
			
		self.sendPings()
		self.receivePings(timeout)
		self.soc.close()
		return self

