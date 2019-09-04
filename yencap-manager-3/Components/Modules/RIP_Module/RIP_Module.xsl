<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0"
	xmlns:ycp="urn:loria:madynes:ensuite:yencap:1.0"
	xmlns:rip="urn:loria:madynes:ensuite:yencap:module:RIP:1.0">

	<xsl:template match="/xc:rpc-reply/xc:data/ycp:netconf/ycp:routing/rip:rip">
		<div>
			<p>The RIP module communicates with zebra by doing a local telnet on port 2602. To make this module working, you have to setup the zebra and rip daemons configuration.</p>
			<h2>Redistribute</h2>
			
			<p>Here you can define what sources can be redistributed to the RIP route database. For example, you can specify that OSPF learned routes are redistributed to RIP known routes.
				<xsl:for-each select="rip:redistribute/rip:*">
					<form method="POST" class="operation" enctype="multipart/form-data">
						Source: 
								<xsl:element name="input">
               						<xsl:attribute name="type">text</xsl:attribute>
              						 <xsl:attribute name="name">blabla</xsl:attribute>
              						 <xsl:attribute name="maxlength">16</xsl:attribute>
              						 <xsl:attribute name="size">16</xsl:attribute>
			   						 <xsl:attribute name="readonly">readonly</xsl:attribute>
              						 <xsl:attribute name="value"><xsl:value-of select="name()"/></xsl:attribute>
             					</xsl:element>
						Metric:
								<xsl:element name="input">
               						<xsl:attribute name="type">text</xsl:attribute>
              						 <xsl:attribute name="name">metric</xsl:attribute>
              						 <xsl:attribute name="maxlength">2</xsl:attribute>
              						 <xsl:attribute name="size">2</xsl:attribute>
              						 <xsl:attribute name="value"><xsl:value-of select="@metric"/></xsl:attribute>
             					</xsl:element>
						Route-map:
								<xsl:element name="input">
               						<xsl:attribute name="type">text</xsl:attribute>
              						<xsl:attribute name="name">route-map</xsl:attribute>
              						<xsl:attribute name="size">16</xsl:attribute>
              						<xsl:attribute name="value"><xsl:value-of select="@route-map"/></xsl:attribute>
             					</xsl:element>
						
         					<xsl:element name="input">
								<xsl:attribute name="type">hidden</xsl:attribute>
								<xsl:attribute name="name">redistribute</xsl:attribute>
								<xsl:attribute name="value"><xsl:value-of select="name()"/></xsl:attribute>
							</xsl:element>
							<input type="hidden" name="object" value="redistribute"/>
							
								<input type="submit" name="ripoperation" value="replace"/>
								<input type="submit" name="ripoperation" value="delete"/>
						
						<input type="hidden" name="operation" value="Apply"/>
						<input type="hidden" name="module" value="RIP_Module"/>
					</form>
				</xsl:for-each>
				
					<form method="POST" class="operation" enctype="multipart/form-data">
						Source: 
							<select name="redistribute">
								<option>kernel</option>
								<option>ospf</option>
								<option>static</option>
								<option>bgp</option>
								<option>connected</option>
							</select>
						Metric:
							<select name="metric">
								<option>1</option>
								<option>2</option>
								<option>3</option>
								<option>4</option>
								<option>5</option>
								<option>6</option>
								<option>7</option>
								<option>8</option>
								<option>9</option>
								<option>10</option>
								<option>11</option>
								<option>12</option>
								<option>13</option>
								<option>14</option>
								<option>15</option>
								<option>16</option>
							</select>
						Route-map:
							<input type='text' name='route-map' maxlength="16" size="16"/>
							<input type="submit" name="ripoperation" value="create"/>
							<input type="hidden" name="object" value="redistribute"/>
							<input type="hidden" name="operation" value="Apply"/>
							<input type="hidden" name="module" value="RIP_Module"/>
						
					</form>

			</p>

			<h2>Networks</h2>
				<p>The syntax is "w.x.y.z/prefix".
  				<xsl:for-each select="rip:networks/rip:network">
					<form method="POST" class="operation" enctype="multipart/form-data">
						network:
         					<xsl:element name="input">
								<xsl:attribute name="type">text</xsl:attribute>
								<xsl:attribute name="name">network</xsl:attribute>
              						 <xsl:attribute name="maxlength">16</xsl:attribute>
              						 <xsl:attribute name="size">16</xsl:attribute>
								<xsl:attribute name="value"><xsl:value-of select="text()"/></xsl:attribute>
							</xsl:element>
							<input type="hidden" name="object" value="networks"/>
							<input type="submit" name="ripoperation" value="replace"/>
							<input type="submit" name="ripoperation" value="delete"/>
							<input type="hidden" name="operation" value="Apply"/>
							<input type="hidden" name="module" value="RIP_Module"/>
					</form>
				</xsl:for-each>
					<form method="POST" class="operation" enctype="multipart/form-data">
						<input type='text' name='network' maxlength="16" size="16"/>
						<input type="submit" name="ripoperation" value="create"/>
						<input type="hidden" name="object" value="networks"/>
						<input type="hidden" name="operation" value="Apply"/>
						<input type="hidden" name="module" value="RIP_Module"/>
					</form>

			</p>

			<h2>Neighbors</h2>
			<p>Here you can define RIP neighbors as IP addresses. 
  				<xsl:for-each select="rip:neighbors/rip:neighbor">
					<form method="POST" class="operation" enctype="multipart/form-data">
						Neighbor:
         					<xsl:element name="input">
								<xsl:attribute name="type">text</xsl:attribute>
								<xsl:attribute name="name">neighbor</xsl:attribute>
              					<xsl:attribute name="maxlength">16</xsl:attribute>
              					<xsl:attribute name="size">16</xsl:attribute>
								<xsl:attribute name="value"><xsl:value-of select="text()"/></xsl:attribute>
							</xsl:element>
							<input type="hidden" name="object" value="neighbors"/>
							<input type="submit" name="ripoperation" value="replace"/>
							<input type="submit" name="ripoperation" value="delete"/>
							<input type="hidden" name="operation" value="Apply"/>
							<input type="hidden" name="module" value="RIP_Module"/>
					</form>
				</xsl:for-each>
				
					<form method="POST" class="operation" enctype="multipart/form-data">
						<input type='text' name='neighbor' maxlength="16" size="16"/>
						<input type="submit" name="ripoperation" value="create"/>
						<input type="hidden" name="object" value="neighbors"/>
						<input type="hidden" name="operation" value="Apply"/>
						<input type="hidden" name="module" value="RIP_Module"/>
					</form>

			</p>

			<h2>Passive interfaces</h2>
  				Passive-interface
				<xsl:for-each select="rip:passive-interfaces/rip:passive-interface">
					<form method="POST" class="operation" enctype="multipart/form-data">
						<xsl:element name="input">
							<xsl:attribute name="type">text</xsl:attribute>
							<xsl:attribute name="name">passive-interface</xsl:attribute>
              				<xsl:attribute name="maxlength">16</xsl:attribute>
              				<xsl:attribute name="size">16</xsl:attribute>
							<xsl:attribute name="value"><xsl:value-of select="text()"/></xsl:attribute>
						</xsl:element>
						<input type="hidden" name="object" value="passive-interfaces"/>
						<input type="submit" name="ripoperation" value="replace"/>
						<input type="submit" name="ripoperation" value="delete"/>
						<input type="hidden" name="operation" value="Apply"/>
						<input type="hidden" name="module" value="RIP_Module"/>
					</form>
				</xsl:for-each>
				<form method="POST" class="operation" enctype="multipart/form-data">
					<input type='text' name='passive-interface' maxlength="16" size="16"/>
					<input type="submit" name="ripoperation" value="create"/>
					<input type="hidden" name="object" value="passive-interfaces"/>
					<input type="hidden" name="operation" value="Apply"/>
					<input type="hidden" name="module" value="RIP_Module"/>
				</form>

			<br/>

			<h2>Distribute lists</h2>
				<xsl:for-each select="rip:distribute-lists/rip:distribute-list">
					<form method="POST" class="operation" enctype="multipart/form-data">
						distribute-list:
         					<xsl:element name="input">
								<xsl:attribute name="type">text</xsl:attribute>
								<xsl:attribute name="name">distribute-list</xsl:attribute>
              					<xsl:attribute name="maxlength">16</xsl:attribute>
              					<xsl:attribute name="size">16</xsl:attribute>
								<xsl:attribute name="value"><xsl:value-of select="text()"/></xsl:attribute>
							</xsl:element>
						direct:
								<xsl:element name="input">
               						<xsl:attribute name="type">text</xsl:attribute>
              						 <xsl:attribute name="name">direct</xsl:attribute>
              						 <xsl:attribute name="maxlength">3</xsl:attribute>
              						 <xsl:attribute name="size">3</xsl:attribute>
              						 <xsl:attribute name="value"><xsl:value-of select="@direct"/></xsl:attribute>
             					</xsl:element>
						name:
								<xsl:element name="input">
               						<xsl:attribute name="type">text</xsl:attribute>
              						<xsl:attribute name="name">name</xsl:attribute>
              						<xsl:attribute name="maxlength">16</xsl:attribute>
              						<xsl:attribute name="size">16</xsl:attribute>
              						<xsl:attribute name="value"><xsl:value-of select="@name"/></xsl:attribute>
             					</xsl:element>
							<input type="hidden" name="object" value="distribute-lists"/>
							<input type="submit" name="ripoperation" value="replace"/>
							<input type="submit" name="ripoperation" value="delete"/>
							<input type="hidden" name="operation" value="Apply"/>
							<input type="hidden" name="module" value="RIP_Module"/>
					</form>
				</xsl:for-each>
				<form method="POST" class="operation" enctype="multipart/form-data">
					distribute-list:
						<input type='text' name='distribute-list' maxlength="16" size="16"/>
					direct:
					<select name="direct">
								<option>in</option>
								<option>out</option>
					</select>
					name:
						<input type='text' name='name' maxlength="16" size="16"/>
					<input type="submit" name="ripoperation" value="create"/>
					<input type="hidden" name="object" value="distribute-lists"/>
					<input type="hidden" name="operation" value="Apply"/>
					<input type="hidden" name="module" value="RIP_Module"/>
				</form>

		</div>
	</xsl:template>

	<xsl:template match="text()">	
	</xsl:template>

</xsl:stylesheet>
