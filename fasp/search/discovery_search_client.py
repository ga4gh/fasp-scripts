import requests
import pprint
import sys
import getopt

#from fasp.loc import GA4GHRegistry
import pandas as pd

class DiscoverySearchClient:

	def __init__(self, hostURL, debug=False ):
		self.hostURL = self._url_format(hostURL)
		self.debug = debug
		self.headers = {
			'content-type': 'application/json'
		}
		#self.tables = self.listTables(verbose=False)

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

	def _url_format(self, url):
		url = str(url)
		if url.endswith('/'):
			url = url[:-1]
		return url

	def listTables(self, requestedCatalog=None, verbose=True):

		tables = {}

		if requestedCatalog == None:
			next_url = self.hostURL + "/tables"
		else:
			next_url = "{}{}{}".format(self.hostURL,'/tables/catalog/',requestedCatalog)
		pageCount = 0
		if verbose:
			print("_Retrieving the table list_")
		while next_url != None :
			pageCount += 1
			tableCount = 0
			if verbose:
				print ("____Page{}_______________".format(pageCount))
			response = requests.get(next_url, headers=self.headers)
			result = (response.json())
			#pprint.pprint(result)
			if requestedCatalog == None and 'pagination' in result and 'next_page_url' in result['pagination']:
				next_url = result['pagination']['next_page_url']
			else:
				next_url = None
			for t in result['tables']:
				if verbose:
					print(t['name'])
				tableCount += 1
				key = "table" + str(tableCount)
				tables[key] = t['name']
		return tables

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

	def runOneTableQuery(self, column_list, table, limit):
		col_string = ", ".join(column_list)

		query = "select {columns} from {table} limit {results}".format(columns=col_string,
																table=table, results=limit)
		res = resultRows = self.runQuery(query, returnType='dataframe')
		return res

	def runQuery(self, query, returnType=None):

		query = query.replace("\n", " ").replace("\t", " ")
		query2 = "{\"query\":\"%s\"}" % query

		next_url = self.hostURL + "/search"

		pageCount = 0
		resultRows = []
		column_list = []
		print ("_Retrieving the query_")
		while next_url != None :
			pageCount += 1
			#print ("____Page{}_______________".format(pageCount))
			if pageCount == 1:
				response = requests.request("POST", next_url,
				 headers=self.headers, data = query2)
			else:
				response = requests.request("GET", next_url)
			result = (response.json())
			if self.debug:
				pprint.pprint(result)
			if 'pagination' in result and 'next_page_url' in result['pagination']:
				next_url = result['pagination']['next_page_url']
			else:
				next_url = None
			for r in result['data']:
				resultRows.append([*r.values()])
				
			if 'data_model' in result:
				print('found data model')
				column_list = result['data_model']['properties'].keys()

		if returnType == 'dataframe':
			df = pd.DataFrame(resultRows, columns=column_list, index=None)
			return df
		else:
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