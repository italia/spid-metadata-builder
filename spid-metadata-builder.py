import os
import os.path
import xml.etree.ElementTree as et
import uuid
import json

# Configuration file
with open('spid-metadata.conf') as spidMetadataConf:
    data = json.load(spidMetadataConf)

# Namespace
et.register_namespace("md", "urn:oasis:names:tc:SAML:2.0:metadata")
et.register_namespace("ds", "http://www.w3.org/2000/09/xmldsig#")
et.register_namespace("protocolSupportEnumeration", "urn:oasis:names:tc:SAML:2.0:protocol")

# EntityDescriptor ID
uniqueID = uuid.uuid4().hex

# AssertionConsumerServices
def assertionConsumerServices(i,isDefault):
    if isDefault:
        et.SubElement(SPSSODescriptor,"{urn:oasis:names:tc:SAML:2.0:metadata}AssertionConsumerService",Binding=data["AssertionConsumerService"][i]["binding"],Location=data["AssertionConsumerService"][i]["location"],index=str(i),isDefault="true")
    else:
        et.SubElement(SPSSODescriptor,"{urn:oasis:names:tc:SAML:2.0:metadata}AssertionConsumerService",Binding=data["AssertionConsumerService"][i]["binding"],Location=data["AssertionConsumerService"][i]["location"],index=str(i))

# Attributes
def requestedAttribute(attributes):
    for i, attribute in enumerate(attributes):
        et.SubElement(AttributeConsumingService,"{urn:oasis:names:tc:SAML:2.0:metadata}RequestedAttribute",Name=attribute)

# EntityDescriptor
EntityDescriptor = et.Element("{urn:oasis:names:tc:SAML:2.0:metadata}EntityDescriptor",entityID=data["entityID"],ID='_'+uniqueID)

# SPSSODescriptor
SPSSODescriptor = et.SubElement(EntityDescriptor,"{urn:oasis:names:tc:SAML:2.0:metadata}SPSSODescriptor",AuthnRequestsSigned="true",protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol")

# KeyDescriptor use=signing (n)
for i, item in enumerate(data["keyDescriptorSigning"]):
    KeyDescriptor = et.SubElement(SPSSODescriptor,"{urn:oasis:names:tc:SAML:2.0:metadata}KeyDescriptor",use="signing")
    KeyInfo = et.SubElement(KeyDescriptor,"{http://www.w3.org/2000/09/xmldsig#}KeyInfo")
    X509Data = et.SubElement(KeyInfo,"{http://www.w3.org/2000/09/xmldsig#}X509Data")
    et.SubElement(X509Data,"{http://www.w3.org/2000/09/xmldsig#}X509Certificate").text = data["keyDescriptorSigning"][i]["x509"]

# SingleLogoutService (n)
for i, item in enumerate(data["SingleLogoutService"]):
    SingleLogoutService = et.SubElement(SPSSODescriptor,"{urn:oasis:names:tc:SAML:2.0:metadata}SingleLogoutService",Binding=data["SingleLogoutService"][i]["binding"],Location=data["SingleLogoutService"][i]["location"])

# AssertionConsumerService (n)
for i, item in enumerate(data["AssertionConsumerService"]):
    assertionConsumerServices(i,data["AssertionConsumerService"][i]["isDefault"])

# AttributeConsumingService (n)
for i, item in enumerate(data["AttributeConsumingService"]):
    AttributeConsumingService = et.SubElement(SPSSODescriptor,"{urn:oasis:names:tc:SAML:2.0:metadata}AttributeConsumingService",index=str(i))
    et.SubElement(AttributeConsumingService,"{urn:oasis:names:tc:SAML:2.0:metadata}ServiceName",attrib={"xml:lang": "it"}).text = data["AttributeConsumingService"][i]["serviceName"]
    # Attributes
    requestedAttribute(data["AttributeConsumingService"][i]["attributes"])

# Organization
Organization = et.SubElement(EntityDescriptor,"{urn:oasis:names:tc:SAML:2.0:metadata}Organization")
OrganizationName = et.SubElement(Organization,"{urn:oasis:names:tc:SAML:2.0:metadata}OrganizationName",attrib={"xml:lang": "it"}).text = data["Organization"]["organizationName"]
OrganizationDisplayName = et.SubElement(Organization,"{urn:oasis:names:tc:SAML:2.0:metadata}OrganizationDisplayName",attrib={"xml:lang": "it"}).text = data["Organization"]["organizationDisplayName"]
OrganizationURL = et.SubElement(Organization,"{urn:oasis:names:tc:SAML:2.0:metadata}OrganizationURL",attrib={"xml:lang": "it"}).text = data["Organization"]["organizationUrl"]

tree = et.ElementTree(EntityDescriptor)
tree.write("metadata/metadata-" + uniqueID + ".xml")
