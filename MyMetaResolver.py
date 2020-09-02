import json
import requests
import pprint

from Gen3DRSClient import crdcDRSClient, bdcDRSClient
from sdlDRSClient import sdlDRSClient
from SBDRSClient import sbcgcDRSClient, cavaticaDRSClient
from DRSClient import DRSClient



class MyMetaResolver:
# simulate identifiers.ord and n2t.net metaresolver capability
  
	# Initialize a DRS Client for the service at the specified url base
	# and with the REST resource to provide an access key 
	def __init__(self):
		self.mysdl = sdlDRSClient('~/.keys/prj_11218_D17199.ngc')
		self.drsClients = { 
			"crdc": crdcDRSClient('~/.keys/CRDCAPIKey.json','s3'),
			"bdc": bdcDRSClient('~/.keys/BDCcredentials.json','gs'),
			"insdc": sdlDRSClient('~/.keys/prj_11218_D17199.ngc'),
			"sbcgc": sbcgcDRSClient('~/.keys/sevenbridges_keys.json','s3'),
			"sbcav": cavaticaDRSClient('~/.keys/sevenbridges_keys.json','s3')
		}
		self.registeredClients = []

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
				#pprint.pprint(service)
				serviceURL = service['url']
				drsClient = DRSClient(serviceURL)
				print("url:{}".format(serviceURL))
				self.registeredClients.append(drsClient)
		return None
	
	def checkResolution(self):
		mixedIDs = ['insdc:SRR5368359.sra',
				'bdc:dg.4503/66eeec21-aad0-4a77-8de5-621f05e2d301',
				'crdc:f360253c-d7d7-47cb-947a-b26e0b41b800',
				'sbcgc:5baa9d00e4b0abc1388b8ce0',
				'sbcav:5772b6ed507c1752674486fc']
	
		for id in mixedIDs:
			print('-------------------------------')
			res = mr.getObject(id)
			print(json.dumps(res, indent=2))	

if __name__ == "__main__":
	mr = MyMetaResolver()
	#mr.checkResolution()
	mr.getRegisteredDRSServices()
	
