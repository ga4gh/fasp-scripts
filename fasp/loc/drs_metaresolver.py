import json
import requests
import sys, getopt

from fasp.loc import crdcDRSClient, bdcDRSClient, Gen3DRSClient, anvilDRSClient
from fasp.loc import kfDRSClient
from fasp.loc import sdlDRSClient, SRADRSClient
from fasp.loc import sbcgcDRSClient, cavaticaDRSClient, sbbdcDRSClient
from fasp.loc import DRSClient
from fasp.loc import GA4GHRegistryClient



class DRSMetaResolver(DRSClient):
	'''simulate identifiers.org and n2t.net metaresolver capability.
	Prefixes used are not official. For demonstration purpposes only'''
	# Initialize a DRS Client for the service at the specified url base
	# and with the REST resource to provide an access key 
	def __init__(self, debug=False, getReg=True, meta_resolver=None):
		crdcDRS = crdcDRSClient('~/.keys/crdc_credentials.json','s3')
		anvilDRS = anvilDRSClient('~/.keys/anvil_credentials.json', '', 'gs')
		bdcDRS = bdcDRSClient('~/.keys/bdc_credentials.json','gs')
		self.drsClients = { 
			"insdc": sdlDRSClient('~/.keys/prj_11218_D17199.ngc'),
			"crdc": crdcDRS,
			"dg.4DFC": crdcDRS,
			"bdc": bdcDRS,
			"dg.4503": bdcDRS,
			"anv": anvilDRS,
			"dg.ANV0": anvilDRS,
			"insdc": sdlDRSClient('~/.keys/prj_11218_D17199.ngc'),
			"sbcgc": sbcgcDRSClient('~/.keys/sevenbridges_keys.json','s3'),
			"sbcav": cavaticaDRSClient('~/.keys/sevenbridges_keys.json','gs'),
			'sbbdc' : sbbdcDRSClient('~/.keys/sevenbridges_keys.json', 's3'),
			"sradrs": SRADRSClient('https://locate.be-md.ncbi.nlm.nih.gov')
		}
		self.debug = debug
		self.meta_resolver = meta_resolver
		self.registeredClients = []
		self.hostNameIndex = {}

		
		if getReg: self.getRegisteredDRSServices()

	def getObject(self, colonPrefixedID):
		client, id = self.getClient(colonPrefixedID)
		if client != None:
			if self.debug: print('sending id {} to: {}'.format(id, client.__class__.__name__))
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
		'''Return a DRS client  to resolve the host name based DRS URI provided, also return the drs_id that needs to be passed to the DRS client.'''
		if self.debug: print('Resolving {}'.format(hostURID))
		idParts = hostURID.split("/",3)
		if self.debug: print(idParts)
		hostName = idParts[2]
		drs_id = idParts[3]
		
		if hostName in self.hostNameIndex.keys():
			return self.hostNameIndex[hostName], drs_id
		
		else:
			return None
			
	def getObject2(self, hostURID):
		client, drs_id = self.getClient2(hostURID)

		
		if client != None:
			print ('id:{}'.format(drs_id))
			print('sending to: {}'.format(client.__class__.__name__))
			return client.getObject(drs_id)
		else:
			return "host unrecognized"
	
	def getAccessURL2(self, hostURID, access_id):
		client, drs_id  = self.getClient2(hostURID)
		
		if client != None:
			return client.getAccessURL(drs_id, access_id)
		else:
			return "host unrecognized"
	
	def DRSClientFromRegistryEntry(self, service, prefix):
		
			if prefix == "crdc": 
				drsClient = crdcDRSClient('~/.keys/crdc_credentials.json','s3')
			elif prefix == "bdc": 
				drsClient = bdcDRSClient('~/.keys/bdc_credentials.json','gs')
			elif prefix == "insdc": 
				drsClient = sdlDRSClient('~/.keys/prj_11218_D17199.ngc')
			elif prefix == "sbcgc": 
				drsClient = sbcgcDRSClient('~/.keys/sevenbridges_keys.json','s3')
			elif prefix == "sbcav": 
				drsClient = cavaticaDRSClient('~/.keys/sevenbridges_keys.json','s3')
			elif service['url'] == "https://data.kidsfirstdrc.org":
				drsClient = kfDRSClient('~/.keys/kf_credentials.json')				
			else: 
				drsClient = DRSClient.fromRegistryEntry(service)
			return drsClient

			
	# Look for registered DRS services
	def getRegisteredDRSServices(self):
		reg = GA4GHRegistryClient()
		drsServices = reg.getRegisteredServices('org.ga4gh:drs')
		#if ('message', 'Service Unavailable') in drsServices.items():
		if not isinstance(drsServices, list):
			print('GA4GH registry unavailable, cannot get registered DRS services.')
			print('Continuing with locally known DRS services.')
			return None

		for service in drsServices:
			if self.debug:
				json.dumps(service, indent=3)
			serviceURL = service['url']
			if 'curiePrefix' in service:
				prefix = service['curiePrefix']
			else:
				prefix = None
			drsClient = self.DRSClientFromRegistryEntry(service, prefix)
			hostname = serviceURL.split("/")[2]
			self.registeredClients.append(drsClient)
			self.hostNameIndex[hostname] = drsClient
			self.drsClients[prefix] = drsClient
			if self.debug:
				print('__________________________')
				print("id:{}".format(service['id']))
				print (drsClient.id, drsClient.name)
				print("url:{}".format(serviceURL))
				print("prefix:{}".format(prefix))
		return None
	
	def checkResolution(self, meta_resolver=None):
		mixedIDs = ['insdc:SRR5368359.sra',
				'bdc:66eeec21-aad0-4a77-8de5-621f05e2d301',
				'dg.4503:66eeec21-aad0-4a77-8de5-621f05e2d301',
				'crdc:0e3c5237-6933-4d30-83f8-6ab721096bc7',
				'dg.4DFC:0e3c5237-6933-4d30-83f8-6ab721096bc7',
				'sbcgc:5baa8913e4b0db63859e515e',
				'sbcav:5772b6ed507c1752674486fc',
				'anv:895c5a81-b985-4559-bc8e-cecece550756',
				'dg.ANV0:895c5a81-b985-4559-bc8e-cecece550756',
				'sradrs:72ff6ff882ec447f12df018e6183de59']

	
		testResults = {}
		for id in mixedIDs:
			print('-------------------------------')
			print('sending: {}'.format(id))
			if meta_resolver:
				res = self.getObject(id)
			else:
				res = self.getObject(id)
			idParts = id.split(":", 1)
			if res == 400:
				testResults[idParts[0]] = 'request error'.format(id)
			if res == 404:
				testResults[idParts[0]] = 'id not found:{}'.format(id)
			elif res == 401:
				testResults[idParts[0]] = 'Unauthorized'
			elif res == 500:
				testResults[idParts[0]] = 'server error - may be unauthorized'
			elif res == 502:
				testResults[idParts[0]] = 'proxy error 502'
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
	print (sys.argv[0] +' -h -c -u')

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

