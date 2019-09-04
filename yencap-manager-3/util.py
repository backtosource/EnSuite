###############################################################################
#                                                                             #
# YencaPClient software, LORIA-INRIA LORRAINE, MADYNES RESEARCH TEAM           #
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
#   Email: Vincent.CRIDLIG@loria.fr                                           #
#                                                                             #
###############################################################################

from Ft.Xml.Domlette import PrettyPrint
import cStringIO, zlib, base64

def asciiCompress(data, level=6):
	""" compress data to printable ascii-code """

	code = zlib.compress(data,level)
	csum = zlib.crc32(code)
	code = base64.encodestring(code)
	return code

def asciiDecompress(code):
	""" decompress result of asciiCompress """

	code = base64.decodestring(code)
	csum = zlib.crc32(code)
	data = zlib.decompress(code)
	return data

def convertNodeToString(node):
	""" convert a Domlette tree to a string """

	buf = cStringIO.StringIO()
	PrettyPrint(node, stream=buf, encoding='UTF-8')
	result = buf.getvalue()
	buf.close()
	return result

def printNodeToFile(node, filePath):
	""" print a Domlette tree to a file """

	f = open(filePath,'w')
	PrettyPrint(node, f)
	f.close()

