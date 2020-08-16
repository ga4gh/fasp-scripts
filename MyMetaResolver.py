import 


class MyMetaResolver:
# simulate identifiers.ord and n2t.net metaresolver capability
  
    # Initialize a DRS Client for the service at the specified url base
    # and with the REST resource to provide an access key 
    def __init__(self, api_url_base,  access_token_resource):
    	self.resolverData = {
			'crdc':'https://nci-crdc.datacommons.io/', 
			'bdc': 'https://gen3.biodatacatalyst.nhlbi.nih.gov/'
		}


    # Obtain an access_token using the provided Fence API key.
    # The client object will retain the access key for subsequent calls
    def resolve(self, colonPrefixedID):
    	idParts = colonPrefixedID.split(":", 1)
    	if idParts[0] in self.resolverData:
    		return self.resolverData[idParts[1]]+idParts[1]
    	else:
    		return "prefix unrecognized"
