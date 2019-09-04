<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0"
	xmlns:ycp="urn:loria:madynes:ensuite:yencap:1.0"
	xmlns:ifs="urn:loria:madynes:ensuite:yencap:module:Interfaces:1.0">

	<xsl:template match="/">
		<div>
			<xsl:for-each select="xc:rpc-reply/xc:data/ycp:netconf/ycp:network/ifs:interfaces/ifs:interface">
				<form method="POST" class="operation" enctype="multipart/form-data">
					<h2><xsl:value-of select="ifs:name"/></h2>

          mac-address:
            <xsl:value-of select="ifs:mac-address"/><br/>

          mtu:
			<xsl:element name="input">
              <xsl:attribute name="type">text</xsl:attribute>
              <xsl:attribute name="name">mtu</xsl:attribute>
              <xsl:attribute name="value"><xsl:value-of select="ifs:mtu"/></xsl:attribute>
            </xsl:element>
			<br/>

         <xsl:for-each select="ifs:ipv4">

      	   netmask:
			 <xsl:element name="input">
               <xsl:attribute name="type">text</xsl:attribute>
               <xsl:attribute name="name">netmask</xsl:attribute>
               <xsl:attribute name="value"><xsl:value-of select="ifs:netmask"/></xsl:attribute>
             </xsl:element>
			 <br/>

           broadcast:
             <xsl:element name="input">
               <xsl:attribute name="type">text</xsl:attribute>
               <xsl:attribute name="name">broadcast</xsl:attribute>
               <xsl:attribute name="value"><xsl:value-of select="ifs:broadcast"/></xsl:attribute>
             </xsl:element>
             <br/>

           address-v4:
			<xsl:element name="input">
              <xsl:attribute name="type">text</xsl:attribute>
              <xsl:attribute name="name">address-v4</xsl:attribute>
              <xsl:attribute name="value"><xsl:value-of select="ifs:address-v4"/></xsl:attribute>
            </xsl:element>
    		<br/>
      	  </xsl:for-each>

          <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="name">ifname</xsl:attribute>
            <xsl:attribute name="value"><xsl:value-of select="ifs:name"/></xsl:attribute>
          </xsl:element>

<input type="hidden" name="module" value="Interfaces_Module"/>
<input type="submit" name="operation" value="Apply"/>
</form>
</xsl:for-each>
</div>
</xsl:template>

  <xsl:template match="text()">	
  </xsl:template>

</xsl:stylesheet>
