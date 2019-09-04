<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0"
	xmlns:ycp="urn:loria:madynes:ensuite:yencap:1.0"
	xmlns:voip="urn:loria:madynes:ensuite:yencap:module:ASTERISK:1.0">

  <xsl:template match="/xc:rpc-reply/xc:data/ycp:netconf/voip:asterisk">
    <div>
	  <p>This module is in charge of the Asterisk software configuration.</p>
      <p>
        <xsl:for-each select="voip:file">
			<h2><xsl:value-of select="@name"/></h2>
			<p>
			<xsl:for-each select="voip:section">
				
				<ul>Section: <xsl:value-of select="@name"/><br/>
					<xsl:for-each select="voip:attribute">
						<li><xsl:value-of select="@name"/>: <xsl:value-of select="text()"/></li>
	        		</xsl:for-each>
				</ul>
	        </xsl:for-each>
			</p>
        </xsl:for-each>
	  </p>
    </div>
  </xsl:template>

  <xsl:template match="/xc:rpc-reply/xc:rpc-error">
    <div>
	  <p>This module is in charge of the Asterisk software configuration.</p>
      <p>
	      <xsl:value-of select="voip:error-message/text()"/>
	  </p>
    </div>
  </xsl:template>

  <xsl:template match="text()"/>

</xsl:stylesheet>
