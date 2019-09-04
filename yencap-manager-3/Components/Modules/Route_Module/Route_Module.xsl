<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0"
	xmlns:ycp="urn:loria:madynes:ensuite:yencap:1.0"
	xmlns:rt="urn:loria:madynes:ensuite:yencap:module:Route:1.0">


<xsl:template match="xc:rpc-reply/xc:data/ycp:netconf/ycp:network/rt:routes">
  <div>

	<p>This module is in charge of the network routes. </p>

    <xsl:for-each select="rt:route">
		<h1>Route</h1>
		<p>
	  <form method="POST" class="operation" enctype="multipart/form-data">
			Target:
		  <xsl:element name="input">
            <xsl:attribute name="type">text</xsl:attribute>
            <xsl:attribute name="name">target</xsl:attribute>
            <xsl:attribute name="value"><xsl:value-of select="rt:target"/></xsl:attribute>
          </xsl:element>
			 <br/>

			Next Hop:
          <xsl:element name="input">
            <xsl:attribute name="type">text</xsl:attribute>
            <xsl:attribute name="name">next-hop</xsl:attribute>
            <xsl:attribute name="value"><xsl:value-of select="rt:next-hop"/></xsl:attribute>
          </xsl:element>
			 <br/>

			Flags:
          <xsl:element name="input">
            <xsl:attribute name="type">text</xsl:attribute>
            <xsl:attribute name="name">flags</xsl:attribute>
            <xsl:attribute name="value"><xsl:value-of select="rt:flags"/></xsl:attribute>
          </xsl:element>
			 <br/>

			Metric:
          <xsl:element name="input">
            <xsl:attribute name="type">text</xsl:attribute>
            <xsl:attribute name="name">metric</xsl:attribute>
            <xsl:attribute name="value"><xsl:value-of select="rt:metric"/></xsl:attribute>
          </xsl:element>
			 <br/>

			Ref:
          <xsl:element name="input">
            <xsl:attribute name="type">text</xsl:attribute>
            <xsl:attribute name="name">ref</xsl:attribute>
            <xsl:attribute name="value"><xsl:value-of select="rt:ref"/></xsl:attribute>
          </xsl:element>
			 <br/>

			Use:
          <xsl:element name="input">
            <xsl:attribute name="type">text</xsl:attribute>
            <xsl:attribute name="name">use</xsl:attribute>
            <xsl:attribute name="value"><xsl:value-of select="rt:use"/></xsl:attribute>
          </xsl:element>
			 <br/>

			Interface
          <xsl:element name="input">
            <xsl:attribute name="type">text</xsl:attribute>
            <xsl:attribute name="name">ifname</xsl:attribute>
            <xsl:attribute name="value"><xsl:value-of select="rt:ifname"/></xsl:attribute>
          </xsl:element>
			 <br/>
		  <input type="hidden" name="module" value="Route_Module"/>
	      <input type="hidden" name="operation" value="Apply"/>
	      <input type="submit" name="routeoperation" value="Update"/>
	      <input type="submit" name="routeoperation" value="Delete"/>
	  </form>
		</p>
    </xsl:for-each>

	<h1>Add a route</h1>
	<form method="POST" class="operation" enctype="multipart/form-data">
	  Target:
		<xsl:element name="input">
          <xsl:attribute name="type">text</xsl:attribute>
          <xsl:attribute name="name">target</xsl:attribute>
          <xsl:attribute name="value"></xsl:attribute>
        </xsl:element>
			 <br/>

		Next hop:
		<xsl:element name="input">
          <xsl:attribute name="type">text</xsl:attribute>
          <xsl:attribute name="name">next-hop</xsl:attribute>
          <xsl:attribute name="value"></xsl:attribute>
        </xsl:element>
			 <br/>

		Flags:
		<xsl:element name="input">
          <xsl:attribute name="type">text</xsl:attribute>
          <xsl:attribute name="name">flags</xsl:attribute>
          <xsl:attribute name="value"></xsl:attribute>
        </xsl:element>
			 <br/>

		Interface:
		<xsl:element name="input">
          <xsl:attribute name="type">text</xsl:attribute>
          <xsl:attribute name="name">ifname</xsl:attribute>
          <xsl:attribute name="value"></xsl:attribute>
        </xsl:element>
			 <br/>
	  <input type="hidden" name="module" value="Route_Module"/>
	  <input type="hidden" name="operation" value="Apply"/>
	  <input type="submit" name="routeoperation" value="Create"/>
	</form>


  </div>
</xsl:template>




  <xsl:template match="text()">	
  </xsl:template>

</xsl:stylesheet>
