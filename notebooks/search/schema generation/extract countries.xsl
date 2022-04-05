<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:output method="text"/>
    
    <xsl:template match="/">
       [
        <xsl:apply-templates select="//VALUEDOMAIN/PermissibleValues/PermissibleValues_ITEM/VALIDVALUE"/>
        ]
    </xsl:template>
    
    <xsl:template match="VALIDVALUE">
        {"const":"<xsl:value-of select="." />"},
    </xsl:template>
</xsl:stylesheet>