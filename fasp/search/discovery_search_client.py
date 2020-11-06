import requests
import pprint
import sys
import getopt

#from fasp.loc import GA4GHRegistry 

class DiscoverySearchClient:

	def __init__(self, hostURL, debug=False ):
		self.hostURL = hostURL
		self.debug = debug
		self.headers = {
			'content-type': 'application/json'
		}

	#===========================================================================
	# # Look for registered search services
	# @classmethod
	# def getRegisteredSearchServices(cls):
	# 	reg = GA4GHRegistry()
	# 	services = reg.getRegisteredServices('org.ga4gh:search')
	# 	for service in services:
	# 		serviceType=service['type']
	# 		pprint.pprint(service)
	# 		serviceURL = service['url']
	# 		hostname = serviceURL.split("/")[2]
	#===========================================================================

		return None

	def listTables(self, requestedCatalog=None):
		
		if requestedCatalog == None:
			next_url = self.hostURL + "/tables"
		else:
			next_url = "{}{}{}".format(self.hostURL,'/tables/catalog/',requestedCatalog)
		pageCount = 0
		resultRows = []
		print ("_Retrieving the table list_")
		while next_url != None :
			pageCount += 1
			print ("____Page{}_______________".format(pageCount))
			response = requests.get(next_url, headers=self.headers)
			result = (response.json())
			#pprint.pprint(result)
			if requestedCatalog == None and 'pagination' in result and 'next_page_url' in result['pagination']:
				next_url = result['pagination']['next_page_url']
			else:
				next_url = None
			for t in result['tables']:
				print(t['name'])
		return 
			
	def listCatalogs(self):
		url = self.hostURL + "/tables"

		print ("_Retrieving the catalog list_")
		response = requests.get(url, headers=self.headers)
		result = (response.json())
		for t in result['index']:
			print(t['description'])
		return 

			
	def listCatalog(self, catalog):
		self.listTables(catalog)
			
	def listTableInfo(self, table):
		url = "{}/table/{}/info".format(self.hostURL,table)
		print ("_Schema for table{}_".format(table))
		response = requests.get(url, headers=self.headers)
		result = (response.json())
		pprint.pprint(result)
			
	def runQuery(self, query):
	
		query2 = "{\"query\":\""+query+"\"}"

		next_url = self.hostURL + "search"

		pageCount = 0
		resultRows = []
		print ("_Retrieving the query_")
		while next_url != None :
			pageCount += 1
			print ("____Page{}_______________".format(pageCount))
			if pageCount == 1:
				response = requests.request("POST", next_url,
				 headers=self.headers, data = query2)
			else:
				 response = requests.request("GET", next_url)
			result = (response.json())
			if self.debug: pprint.pprint(result)
			if 'pagination' in result and 'next_page_url' in result['pagination']:
				next_url = result['pagination']['next_page_url']
			else:
				next_url = None
			rowCount = len(result['data'])
# 			if rowCount > 0:
# 				resultRows.append(result['data'])
			for r in result['data']:
				resultRows.append([*r.values()])
		return resultRows

def usage():
	print (sys.argv[0] +' -l listTables -c listCatalog -t tableInfo -r registeredServices')

def main(argv):
	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com')
	
	catalog = ''
	table = ''

	try:
		opts, args = getopt.getopt(argv, "hlc:t:ra", ["help", "listTables", "tableInfo", "registeredServices","catalogs"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
	    if opt in ("-h", "--help"):
	        usage()
	        sys.exit()
	    elif opt in ("-l", "--listTables"):
	        searchClient.listTables()
	    elif opt in ("-c", "--listCatalog"):
	        searchClient.listCatalog(arg)
	    elif opt in ("-t", "--table"):
	        searchClient.listTableInfo(arg)
	    elif opt in ("-a", "--catalogs"):
	        searchClient.listCatalogs()
	    elif opt in ("-r", "--registeredServices"):
	        DiscoverySearchClient.getRegisteredSearchServices()

			
if __name__ == "__main__":
    main(sys.argv[1:])



	#query = "select submitter_id, 'bdc:'||read_drs_id drsid from thousand_genomes.onek_genomes.ssd_drs where population = 'BEB' limit 3"
# 	res = myClient.runQuery(query)


	#searchClient.listTables()
