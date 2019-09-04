<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0"
	xmlns:ycp="urn:loria:madynes:ensuite:yencap:1.0"
	xmlns:ac="urn:loria:madynes:ensuite:yencap:module:RBAC:1.0">


  <xsl:template match="/xc:rpc-reply/xc:data/ycp:netconf/ycp:security/ac:rbac">
    <div>

	<p>This module is in charge of the access control (AC) policy. You can manage roles, users, permissions and their repective assignements. Each time a button is clicked, a Netconf message is sent to the agent to update its AC policy. Roles are the central concept of this policy and therefore should in an ideal world be defined first. Then permissions and users can be linked to these roles. After creating roles, the users (managers) will be able to activate them through <i>Role (de)activation</i> item in the left menu. Internally, the RBAC policy is stored in an XML file, so if you prefer to make it manually and deploy it on many agents, you may prefer to build a low-level edit-config request.</p>


	<h2>Roles</h2>
    <p>
    <xsl:for-each select="ac:roles/ac:role">
	  <form method="POST" class="operation" enctype="multipart/form-data">
		Name: <xsl:element name="input">
               <xsl:attribute name="type">text</xsl:attribute>
               <xsl:attribute name="name">name</xsl:attribute>
               <xsl:attribute name="value"><xsl:value-of select="ac:name"/></xsl:attribute>
             </xsl:element>
          <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="name">roleId</xsl:attribute>
            <xsl:attribute name="value"><xsl:value-of select="@id"/></xsl:attribute>
          </xsl:element>
		  <input type="hidden" name="module" value="RBAC_Module"/>
	      <input type="hidden" name="operation" value="Apply"/>
	      <input type="hidden" name="object" value="Role"/>
	      <input type="submit" name="rbacoperation" value="Update"/>
	      <input type="submit" name="rbacoperation" value="Delete"/>
	  </form>
    </xsl:for-each>
	<form method="POST" class="operation" enctype="multipart/form-data">
	  <font color="red">Name:</font>
		<xsl:element name="input">
          <xsl:attribute name="type">text</xsl:attribute>
          <xsl:attribute name="name">name</xsl:attribute>
          <xsl:attribute name="value"></xsl:attribute>
        </xsl:element>
	  <input type="hidden" name="module" value="RBAC_Module"/>
	  <input type="hidden" name="operation" value="Apply"/>
	  <input type="hidden" name="object" value="Role"/>
	  <input type="submit" name="rbacoperation" value="Create"/>
	</form>
	</p>


	<h2>Users</h2>
	<p>
    <xsl:for-each select="ac:users/ac:user">
	  <form method="POST" class="operation" enctype="multipart/form-data">
	  Login: <xsl:element name="input">
               <xsl:attribute name="type">text</xsl:attribute>
               <xsl:attribute name="name">login</xsl:attribute>
               <xsl:attribute name="value"><xsl:value-of select="ac:login"/></xsl:attribute>
             </xsl:element>
          <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="name">userId</xsl:attribute>
            <xsl:attribute name="value"><xsl:value-of select="@id"/></xsl:attribute>
          </xsl:element>
		  <input type="hidden" name="module" value="RBAC_Module"/>
	      <input type="hidden" name="operation" value="Apply"/>
	      <input type="hidden" name="object" value="User"/>
	      <input type="submit" name="rbacoperation" value="Update"/>
	      <input type="submit" name="rbacoperation" value="Delete"/>
	  </form>
    </xsl:for-each>
	<form method="POST" class="operation" enctype="multipart/form-data">
	  <font color="red">Login:</font>
		<xsl:element name="input">
          <xsl:attribute name="type">text</xsl:attribute>
          <xsl:attribute name="name">login</xsl:attribute>
          <xsl:attribute name="value"></xsl:attribute>
        </xsl:element>
	  <input type="hidden" name="module" value="RBAC_Module"/>
	  <input type="hidden" name="operation" value="Apply"/>
	  <input type="hidden" name="object" value="User"/>
	  <input type="submit" name="rbacoperation" value="Create"/>
	</form>
	</p>


    <h2>Permissions</h2>
    <p>
	  <xsl:for-each select="ac:permissions/ac:permission">
	  <form method="POST" class="operation" enctype="multipart/form-data">
    Operation: <xsl:element name="input">
				<xsl:attribute name="type">text</xsl:attribute>
				<xsl:attribute name="name">op</xsl:attribute>
              	<xsl:attribute name="maxlength">2</xsl:attribute>
				<xsl:attribute name="size">2</xsl:attribute>
               <xsl:attribute name="value"><xsl:value-of select="@op"/></xsl:attribute>
             </xsl:element>
	  Scope: <xsl:element name="input">
               <xsl:attribute name="type">text</xsl:attribute>
               <xsl:attribute name="name">scope</xsl:attribute>
              	<xsl:attribute name="maxlength">50</xsl:attribute>
				<xsl:attribute name="size">50</xsl:attribute>
               <xsl:attribute name="value"><xsl:value-of select="ac:scope"/></xsl:attribute>
             </xsl:element><br/>
	</form>
    </xsl:for-each>
	</p>


	<h2>User Assignements</h2>
    <xsl:for-each select="ac:user-assignements/ac:user-assignement">
	  <form method="POST" class="operation" enctype="multipart/form-data">
		User Id: 
             <xsl:element name="input">
               <xsl:attribute name="type">text</xsl:attribute>
               <xsl:attribute name="name">userRef</xsl:attribute>
              	<xsl:attribute name="maxlength">4</xsl:attribute>
				<xsl:attribute name="size">4</xsl:attribute>
               <xsl:attribute name="value"><xsl:value-of select="@userRef"/></xsl:attribute>
             </xsl:element>
    	Role Id: 
             <xsl:element name="input">
               <xsl:attribute name="type">text</xsl:attribute>
               <xsl:attribute name="name">roleRef</xsl:attribute>
              	<xsl:attribute name="maxlength">4</xsl:attribute>
				<xsl:attribute name="size">4</xsl:attribute>
               <xsl:attribute name="value"><xsl:value-of select="@roleRef"/></xsl:attribute>
             </xsl:element>
		
          <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="name">uraId</xsl:attribute>
            <xsl:attribute name="value"><xsl:value-of select="@id"/></xsl:attribute>
          </xsl:element>

		  <input type="hidden" name="module" value="RBAC_Module"/>
	      <input type="hidden" name="operation" value="Apply"/>
	      <input type="hidden" name="object" value="URA"/>
	      <input type="submit" name="rbacoperation" value="Update"/>
	      <input type="submit" name="rbacoperation" value="Delete"/>
			<br/>
		</form>
    </xsl:for-each>
	<form method="POST" class="operation" enctype="multipart/form-data">
		<font color="red">UserRef:</font><input type="text" name="userRef" value=""/>
		<font color="red">RoleRef:</font><input type="text" name="roleRef" value=""/>
		<input type="hidden" name="module" value="RBAC_Module"/>
		<input type="hidden" name="operation" value="Apply"/>
		<input type="hidden" name="object" value="URA"/>
		<input type="submit" name="rbacoperation" value="Create"/>
	</form>


	<h2>Permission Assignements</h2>
    <p>
	<xsl:for-each select="ac:permission-assignements/ac:permission-assignement">
		Permission Id: 
             <xsl:element name="input">
               <xsl:attribute name="type">text</xsl:attribute>
               <xsl:attribute name="name">permRef</xsl:attribute>
               <xsl:attribute name="value"><xsl:value-of select="@permRef"/></xsl:attribute>
             </xsl:element>
    	Role Id: 
             <xsl:element name="input">
               <xsl:attribute name="type">text</xsl:attribute>
               <xsl:attribute name="name">roleRef</xsl:attribute>
               <xsl:attribute name="value"><xsl:value-of select="@roleRef"/></xsl:attribute>
             </xsl:element><br/>
    </xsl:for-each>
	</p>


  </div>
</xsl:template>




  <xsl:template match="text()">	
  </xsl:template>

</xsl:stylesheet>
