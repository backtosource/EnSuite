<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0"
	xmlns:ycp="urn:loria:madynes:ensuite:yencap:1.0"
	xmlns:bgp="urn:loria:madynes:ensuite:yencap:module:BGP:1.0">

	<xsl:template match="/xc:rpc-reply/xc:data/ycp:netconf/ycp:routing/bgp:bgp/bgp:bgprouter">
		<div>
			AS number:
			<form method="POST" class="operation" enctype="multipart/form-data">
				<xsl:element name="input">
					<xsl:attribute name="type">text</xsl:attribute>
           			<xsl:attribute name="name">ASnumber</xsl:attribute>
           			<xsl:attribute name="maxlength">8</xsl:attribute>
			   		<xsl:attribute name="size">8</xsl:attribute>
					<xsl:attribute name="value"><xsl:value-of select="bgp:as-number/text()"/></xsl:attribute>
   				</xsl:element>
				<input type="submit" name="bgpoperation" value="replace"/>
				<input type="submit" name="bgpoperation" value="delete"/>
				<input type="hidden" name="object" value="as-number"/>
				<input type="hidden" name="operation" value="Apply"/>
				<input type="hidden" name="module" value="BGP_Module"/>
			</form>
			<br/>

			<h2>Neighbors</h2>
			<table>
  				<tr align='left'><th width="20%">ip-address</th><th width="10%">remote-as</th></tr>
				<xsl:for-each select="bgp:neighbors/bgp:neighbor">
					<form method="POST" class="operation" enctype="multipart/form-data">
						<tr align='left'>
							<td>
								<xsl:element name="input">
									<xsl:attribute name="type">text</xsl:attribute>
           							<xsl:attribute name="name">neighborIpAddress</xsl:attribute>
           							<xsl:attribute name="maxlength">16</xsl:attribute>
			   						<xsl:attribute name="size">16</xsl:attribute>
			   						<xsl:attribute name="readonly">readonly</xsl:attribute>
									<xsl:attribute name="value"><xsl:value-of select="bgp:ip-address/text()"/></xsl:attribute>
   								</xsl:element>
							</td>
							<td>
								<xsl:element name="input">
	       							<xsl:attribute name="type">text</xsl:attribute>
	       							<xsl:attribute name="name">neighborRemoteAs</xsl:attribute>
            	  					<xsl:attribute name="maxlength">8</xsl:attribute>
          	    					<xsl:attribute name="size">8</xsl:attribute>
              						<xsl:attribute name="value"><xsl:value-of select="bgp:remote-as/text()"/></xsl:attribute>
             					</xsl:element>
							</td>
							<td>
								<input type="submit" name="bgpoperation" value="replace"/>
								<input type="submit" name="bgpoperation" value="delete"/>
							</td>
						</tr>
						<input type="hidden" name="object" value="neighbors"/>
						<input type="hidden" name="operation" value="Apply"/>
						<input type="hidden" name="module" value="BGP_Module"/>
					</form>
				</xsl:for-each>
				
				<form method="POST" class="operation" enctype="multipart/form-data">
					<tr>
						<td>
							<input type="text" name="neighborIpAddress" maxlength="16" size="16"/>
						</td>
						<td>
							<input type='text' name='neighborRemoteAs' maxlength="8" size="8"/>
						</td>
						<td>
							<input type="submit" name="bgpoperation" value="create"/>
							<input type="hidden" name="object" value="neighbors"/>
							<input type="hidden" name="operation" value="Apply"/>
							<input type="hidden" name="module" value="BGP_Module"/>
						</td>
					</tr>
				</form>
			</table>
			<br/>


			<h2>Route maps</h2>
			<table>
				<tr align='left'><th width="20%">map tag</th><th width="20%">Sequence number</th><th width="10%">State</th><th width="20%">as-path-name</th></tr>
				<xsl:for-each select="/xc:rpc-reply/xc:data/ycp:netconf/ycp:routing/bgp:bgp/bgp:filters/bgp:route-map">
					<form method="POST" class="operation" enctype="multipart/form-data">
						<tr>
							<td>
								<xsl:element name="input">
									<xsl:attribute name="type">text</xsl:attribute>
           							<xsl:attribute name="name">maptag</xsl:attribute>
           							<xsl:attribute name="maxlength">16</xsl:attribute>
			   						<xsl:attribute name="size">12</xsl:attribute>
			   						<xsl:attribute name="readonly">readonly</xsl:attribute>
									<xsl:attribute name="value"><xsl:value-of select="bgp:map-tag/text()"/></xsl:attribute>
   								</xsl:element>
							</td>
							<td>
								<xsl:element name="input">
									<xsl:attribute name="type">text</xsl:attribute>
           							<xsl:attribute name="name">seqnumber</xsl:attribute>
           							<xsl:attribute name="maxlength">8</xsl:attribute>
			   						<xsl:attribute name="size">8</xsl:attribute>
									<xsl:attribute name="value"><xsl:value-of select="bgp:sequences/bgp:seq-number/text()"/></xsl:attribute>
   								</xsl:element>
							</td>
							<td>
								<xsl:element name="input">
									<xsl:attribute name="type">select</xsl:attribute>
           							<xsl:attribute name="name">state</xsl:attribute>
           							<xsl:attribute name="maxlength">8</xsl:attribute>
			   						<xsl:attribute name="size">8</xsl:attribute>
									<xsl:attribute name="value"><xsl:value-of select="bgp:sequences/bgp:state/text()"/></xsl:attribute>
   								</xsl:element>
							</td>
							<td>
								<xsl:element name="input">
									<xsl:attribute name="type">text</xsl:attribute>
           							<xsl:attribute name="name">aspathname</xsl:attribute>
           							<xsl:attribute name="maxlength">16</xsl:attribute>
			   						<xsl:attribute name="size">12</xsl:attribute>
									<xsl:attribute name="value"><xsl:value-of select="bgp:sequences/bgp:match/bgp:as-path/bgp:as-path-name/text()"/></xsl:attribute>
   								</xsl:element>
							</td>
							<td>
								<input type="submit" name="bgpoperation" value="replace"/>
								<input type="submit" name="bgpoperation" value="delete"/>
							</td>
						</tr>
						<input type="hidden" name="object" value="route-maps"/>
						<input type="hidden" name="operation" value="Apply"/>
						<input type="hidden" name="module" value="BGP_Module"/>
					</form>
				</xsl:for-each>

				
				<form method="POST" class="operation" enctype="multipart/form-data">
					<tr>
						<td>
							<input type="text" name="maptag" maxlength="16" size="12"/>
						</td>
						<td>
							<input type='text' name='seqnumber' maxlength="8" size="8"/>
						</td>
						<td>
							<select name="state">
								<option>permit</option>
								<option>deny</option>
							</select>
						</td>
						<td>
							<input type='text' name='aspathname' maxlength="16" size="12"/>
						</td>
						<td>
							<input type="submit" name="bgpoperation" value="create"/>
							<input type="hidden" name="object" value="route-maps"/>
							<input type="hidden" name="operation" value="Apply"/>
							<input type="hidden" name="module" value="BGP_Module"/>
						</td>
					</tr>
				</form>
			</table>
			<br/>



			<h2>Address families</h2>
			<table>
				<tr align='left'><th width="15%">Neighbor</th><th width="15%">Route map</th><th width="10%">Direct</th><th></th></tr>
				<xsl:for-each select="/xc:rpc-reply/xc:data/ycp:netconf/ycp:routing/bgp:bgp/bgp:bgprouter/bgp:address-families/bgp:ipv4-address-family/bgp:neighbors/bgp:neighbor">
					<form method="POST" class="operation" enctype="multipart/form-data">
						<tr>
							<td>
								<xsl:element name="input">
									<xsl:attribute name="type">text</xsl:attribute>
           							<xsl:attribute name="name">neighborIpAddress</xsl:attribute>
           							<xsl:attribute name="maxlength">16</xsl:attribute>
			   						<xsl:attribute name="size">16</xsl:attribute>
			   						<xsl:attribute name="readonly">readonly</xsl:attribute>
									<xsl:attribute name="value"><xsl:value-of select="bgp:ip-address/text()"/></xsl:attribute>
   								</xsl:element>
							</td><td></td><td></td><td></td>
						</tr>
						
							<xsl:for-each select="bgp:bind-filters/bgp:route-map">
								<tr><td></td><td>
									<xsl:element name="input">
               							<xsl:attribute name="type">text</xsl:attribute>
              							<xsl:attribute name="name">name</xsl:attribute>
              							<xsl:attribute name="maxlength">16</xsl:attribute>
              							<xsl:attribute name="size">16</xsl:attribute>
              							<xsl:attribute name="value"><xsl:value-of select="bgp:name/text()"/></xsl:attribute>
             						</xsl:element>
								</td>
								<td>
									<xsl:element name="input">
               							<xsl:attribute name="type">text</xsl:attribute>
              							<xsl:attribute name="name">direct</xsl:attribute>
              							<xsl:attribute name="maxlength">3</xsl:attribute>
              							<xsl:attribute name="size">3</xsl:attribute>
              							<xsl:attribute name="value"><xsl:value-of select="bgp:direct/text()"/></xsl:attribute>
             						</xsl:element>
								</td>
								<td>
									<input type="submit" name="bgpoperation" value="replace"/>
									<input type="submit" name="bgpoperation" value="delete"/>
								</td></tr>
							</xsl:for-each>
						
						<input type="hidden" name="object" value="afneighbors"/>
						<input type="hidden" name="operation" value="Apply"/>
						<input type="hidden" name="module" value="BGP_Module"/>
					</form>
				</xsl:for-each>

				<form method="POST" class="operation" enctype="multipart/form-data">
					<tr>
						<td><input type="text" name="neighborIpAddress" maxlength="16" size="16"/></td>
						<td><input type="text" name="name" maxlength="16" size="16"/></td>
						<td>
							<select name="direct">
								<option>in</option>
								<option>out</option>
							</select>
						</td>
						<td>
							<input type="submit" name="bgpoperation" value="create"/>
							<input type="hidden" name="object" value="afneighbors"/>
							<input type="hidden" name="operation" value="Apply"/>
							<input type="hidden" name="module" value="BGP_Module"/>
						</td>
					</tr>
				</form>
			</table>
			<br/>

		</div>
	</xsl:template>

	<xsl:template match="text()">	
	</xsl:template>

</xsl:stylesheet>
