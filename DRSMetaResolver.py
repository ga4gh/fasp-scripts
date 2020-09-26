import json
import requests
import pprint
import sys, getopt

from Gen3DRSClient import crdcDRSClient, bdcDRSClient, Gen3DRSClient
from sdlDRSClient import sdlDRSClient
from SBDRSClient import sbcgcDRSClient, cavaticaDRSClient
from DRSClient import DRSClient


class GA4GHRegistry:

	def __init__(self):
		self.hostURL = 'https://registry.ga4gh.org/v1'
	
	# Look for registered DRS services
	def getRegisteredServices(self, type=None):
		servicesURL = "{}/services".format(self.hostURL)
		if type == None:
			type = 'all'
		else:
			registryURL = 'https://registry.ga4gh.org/v1/services?type={}:*'.format(type)
		print('Searching the GA4GH registry for {} services'.format(type))
		response = requests.get(registryURL)
		services = response.json()
		return services


class DRSMetaResolver(DRSClient):
# simulate identifiers.ord and n2t.net metaresolver capability
  
	# Initialize a DRS Client for the service at the specified url base
	# and with the REST resource to provide an access key 
	def __init__(self, debug=False):
		self.drsClients = { 
			"insdc": sdlDRSClient('~/.keys/prj_11218_D17199.ngc'),
			"crdc": crdcDRSClient('~/.keys/CRDCAPIKey.json','s3'),
			"bdc": bdcDRSClient('~/.keys/BDCcredentials.json','gs'),
			"anv": Gen3DRSClient('https://gen3.theanvil.io','/user/credentials/api/access_token', '~/.keys/anvil_credentials.json', 'gs'),
			"insdc": sdlDRSClient('~/.keys/prj_11218_D17199.ngc'),
			"sbcgc": sbcgcDRSClient('~/.keys/sevenbridges_keys.json','s3'),
			"sbcav": cavaticaDRSClient('~/.keys/sevenbridges_keys.json','s3')
		}
		self.registeredClients = []
		self.hostNameIndex = {}
		self.debug = debug

	def getObject(self, colonPrefixedID):
		client, id = self.getClient(colonPrefixedID)
		if client != None:
			print ('id:{}'.format(id))
			print('sending to: {}'.format(client.__class__.__name__))
			return client.getObject(id)
		else:
			return "prefix unrecognized"

	def getAccessURL(self, colonPrefixedID, access_id=None):
		client, id = self.getClient(colonPrefixedID)
		if client != None:
			return client.getAccessURL(id, access_id)
		else:
			return "prefix unrecognized"
							
	def getClient(self, colonPrefixedID):
		idParts = colonPrefixedID.split(":", 1)
		prefix = idParts[0]
		
		if prefix in self.drsClients.keys():
			return self.drsClients[prefix] , idParts[1]
		else:
			return None
			
	def getRegisteredClient(self, colonPrefixedID):
		idParts = colonPrefixedID.split(":", 1)
		prefix = idParts[0]
		
		if prefix in self.registeredClients.keys():
			return [self.registeredClients[prefix] , idParts[1]]
		else:
			return None
			
	def getClient2(self, hostURID):
		idParts = hostURID.split("/",3)
		hostName = idParts[2]
		
		if hostName in self.hostNameIndex.keys():
			return self.hostNameIndex[hostName]
		else:
			return None
			
	def getObject2(self, hostURID):
		client = self.getClient2(hostURID)
		idParts = hostURID.split("/",3)
		id = idParts[3]
		
		if client != None:
			print ('Prefix:{}'.format(idParts[2]))
			print ('id:{}'.format(id))
			print('sending to: {}'.format(client.__class__.__name__))
			return client.getObject(id)
		else:
			return "host unrecognized"
	
	def DRSClientFromRegistryEntry(self, service, prefix):
		
			if prefix == "crdc": 
				drsClient = crdcDRSClient('~/.keys/CRDCAPIKey.json','s3')
			elif prefix == "bdc": 
				drsClient = bdcDRSClient('~/.keys/BDCcredentials.json','gs')
			elif prefix == "insdc": 
				drsClient = sdlDRSClient('~/.keys/prj_11218_D17199.ngc')
			elif prefix == "sbcgc": 
				drsClient = sbcgcDRSClient('~/.keys/sevenbridges_keys.json','s3')
			elif prefix == "sbcav": 
				drsClient = cavaticaDRSClient('~/.keys/sevenbridges_keys.json','s3')
			else: 
				drsClient = drsClient = DRSClient.fromRegistryEntry(service)
			return drsClient

			
	# Look for registered DRS services
	def getRegisteredDRSServices(self):
		reg = GA4GHRegistry()
		drsServices = reg.getRegisteredServices('org.ga4gh:drs')
		for service in drsServices:
			if self.debug:
				pprint.pprint(service)
			serviceURL = service['url']
			prefix = service['curiePrefix']
			drsClient = self.DRSClientFromRegistryEntry(service, prefix)
			hostname = serviceURL.split("/")[2]
			self.registeredClients.append(drsClient)
			self.hostNameIndex[hostname] = drsClient
			self.drsClients[prefix] = drsClient
			print('__________________________')
			print("id:{}".format(service['id']))
			print (drsClient.id, drsClient.name)
			print("url:{}".format(serviceURL))
			print("prefix:{}".format(prefix))
		return None
	
	def checkResolution(self):
		mixedIDs = ['insdc:SRR5368359.sra',
				'bdc:dg.4503/66eeec21-aad0-4a77-8de5-621f05e2d301',
				'crdc:f360253c-d7d7-47cb-947a-b26e0b41b800',
				'sbcgc:5baa9d00e4b0abc1388b8ce0',
				'sbcav:5772b6ed507c1752674486fc',
				'anv:dg.ANV0/895c5a81-b985-4559-bc8e-cecece550756']
	
		testResults = {}
		for id in mixedIDs:
			print('-------------------------------')
			print(id)
			res = self.getObject(id)
			idParts = id.split(":", 1)
			if res == 404:
				testResults[idParts[0]] = 'id not found:{}'.format(id)
			elif res == 401:
				testResults[idParts[0]] = 'Unauthorized'
			elif res == 500:
				testResults[idParts[0]] = 'server error - may be unauthorized'
			elif res.__class__.__name__ != int:
				testResults[idParts[0]] = 'Success'
				print(json.dumps(res, indent=2))
			else: 
				testResults[idParts[0]] = 'Failed: response was {}'.format(res)
			
		print('----Test results ---')
		for clientKey in self.drsClients.keys():
			if clientKey in testResults:
				print ("{} Tested: {}".format(clientKey, testResults[clientKey]))
			else:
				print ("{} untested".format(clientKey))
			
	def checkHostURIResolution(self):
		mixedIDs = ['drs://gen3.theanvil.io/dg.ANV0/737247da-f5da-49a7-86ec-737978eb8293',
				'drs://gen3.biodatacatalyst.nhlbi.nih.gov/dg.4503/65f34e96-230a-4e20-b15d-8510d688cbf0',
				'drs://nci-crdc.datacommons.io/dg.4DFC/ff59c94b-8124-48a8-8b78-72e71f5d71f0',
				]
	
		for id in mixedIDs:
			print('-------------------------------')
			print(id)
			res = self.getObject2(id)
			print(json.dumps(res, indent=2))	

def usage():
	print (sys.argv[0] +' -l listTables -c listCatalog -t tableInfo -r registeredServices')

def main(argv):

	mr = DRSMetaResolver()

	try:
		opts, args = getopt.getopt(argv, "hcu", ["help", "checkCompactResolution", "checkURIResolution"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
	    if opt in ("-h", "--help"):
	        usage()
	        sys.exit()
	    elif opt in ("-c", "--checkCompactResolution"):
	        mr.checkResolution()
	    elif opt in ("-u", "--checkURIResolution"):
	        mr.getRegisteredDRSServices()
	        mr.checkHostURIResolution()


			
if __name__ == "__main__":
    main(sys.argv[1:])

