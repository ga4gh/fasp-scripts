import json
import requests
import pprint

from Gen3DRSClient import crdcDRSClient, bdcDRSClient
from sdlDRSClient import sdlDRSClient
from SBDRSClient import sbcgcDRSClient, cavaticaDRSClient
from DRSClient import DRSClient



class DRSMetaResolver:
# simulate identifiers.ord and n2t.net metaresolver capability
  
	# Initialize a DRS Client for the service at the specified url base
	# and with the REST resource to provide an access key 
	def __init__(self, debug=False):
		self.mysdl = sdlDRSClient('~/.keys/prj_11218_D17199.ngc')
		self.drsClients = { 
			"crdc": crdcDRSClient('~/.keys/CRDCAPIKey.json','s3'),
			"bdc": bdcDRSClient('~/.keys/BDCcredentials.json','gs'),
			"insdc": sdlDRSClient('~/.keys/prj_11218_D17199.ngc'),
			"sbcgc": sbcgcDRSClient('~/.keys/sevenbridges_keys.json','s3'),
			"sbcav": cavaticaDRSClient('~/.keys/sevenbridges_keys.json','s3')
		}
		self.registeredClients = []
		self.hostNameIndex = {}
		self.debug = debug

	def getObject(self, colonPrefixedID):
		idParts = colonPrefixedID.split(":", 1)
		if idParts[0] in self.drsClients.keys():
			print ('Prefix:{}'.format(idParts[0]))
			print ('id:{}'.format(idParts[1]))
			client = self.drsClients[idParts[0]]
			print('sending to: {}'.format(client.__class__.__name__))
			return client.getObject(idParts[1])
		else:
			return "prefix unrecognized"
			
	def getObject2(self, hostURID):
		idParts = hostURID.split("/",3)
		hostName = idParts[2]
		id = idParts[3]
		
		if hostName in self.hostNameIndex.keys():
			print ('Prefix:{}'.format(hostName))
			print ('id:{}'.format(id))
			client = self.hostNameIndex[hostName]
			print('sending to: {}'.format(client.__class__.__name__))
			return client.getObject(id)
		else:
			return "host unrecognized"
			
	# Look for registered DRS services
	def getRegisteredDRSServices(self):
		print('Searching the GA4GH registry for DRS services')
		registryURL = 'https://registry.ga4gh.org/v1/services'
		response = requests.get(registryURL)
		services = response.json()
		for service in services:
			serviceType=service['type']
			if serviceType['artifact'] == 'drs':
				print('__________________________')
				print("id:{}".format(service['id']))
				if self.debug:
					pprint.pprint(service)
				serviceURL = service['url']
				drsClient = DRSClient.fromRegistryEntry(service)
				print (drsClient.id, drsClient.name)
				print("url:{}".format(serviceURL))
				hostname = serviceURL.split("/")[2]
				self.registeredClients.append(drsClient)
				self.hostNameIndex[hostname] = drsClient
		return None
	
	def checkResolution(self):
		mixedIDs = ['insdc:SRR5368359.sra',
				'bdc:dg.4503/66eeec21-aad0-4a77-8de5-621f05e2d301',
				'crdc:f360253c-d7d7-47cb-947a-b26e0b41b800',
				'sbcgc:5baa9d00e4b0abc1388b8ce0',
				'sbcav:5772b6ed507c1752674486fc',
				'dg.ANV0/895c5a81-b985-4559-bc8e-cecece550756']
	
		for id in mixedIDs:
			print('-------------------------------')
			print(id)
			res = mr.getObject(id)
			print(json.dumps(res, indent=2))	
			
	def checkHostURIResolution(self):
		mixedIDs = ['drs://gen3.theanvil.io/dg.ANV0/737247da-f5da-49a7-86ec-737978eb8293',
				'drs://gen3.biodatacatalyst.nhlbi.nih.gov/dg.4503/65f34e96-230a-4e20-b15d-8510d688cbf0',
				'drs://nci-crdc.datacommons.io/dg.4DFC/ff59c94b-8124-48a8-8b78-72e71f5d71f0',
				]
	
		for id in mixedIDs:
			print('-------------------------------')
			print(id)
			res = mr.getObject2(id)
			print(json.dumps(res, indent=2))	

if __name__ == "__main__":
	mr = DRSMetaResolver(debug=False)
	#mr.checkResolution()
	mr.getRegisteredDRSServices()
	mr.checkHostURIResolution()
