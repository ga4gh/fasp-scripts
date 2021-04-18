import requests
import pprint
import sys
import getopt
import json

from fasp.loc import GA4GHRegistryClient
import pandas as pd

class DataConnectClient:

	def __init__(self, hostURL, debug=False ):
		self.hostURL = self._url_format(hostURL)
		self.debug = debug
		self.headers = {
			'content-type': 'application/json'
		}

	# Look for registered search services
	@classmethod
	def getRegisteredSearchServices(cls):
		reg = GA4GHRegistryClient()
		services = reg.getRegisteredServices('org.ga4gh:search')
		for service in services:
			serviceType=service['type']
			pprint.pprint(service)
			serviceURL = service['url']
			hostname = serviceURL.split("/")[2]

		return None

	def _url_format(self, url):
		url = str(url)
		if url.endswith('/'):
			url = url[:-1]
		return url

	def listTables(self, requestedCatalog=None, verbose=True):

		tables = []

		if requestedCatalog == None:
			next_url = self.hostURL + "/tables"
		else:
			next_url = "{}{}{}".format(self.hostURL,'/tables/catalog/',requestedCatalog)
		pageCount = 0
		if verbose:
			print("_Retrieving the table list_")
		while next_url != None :
			pageCount += 1
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
				tables.append(t['name'])

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

	def listTableInfo(self, table, verbose=False):
		url = "{}/table/{}/info".format(self.hostURL,table)
		response = requests.get(url, headers=self.headers)
		info = json.loads(response.text)
		if verbose:
			print ("_Schema for table{}_".format(table))
			print(json.dumps(info, indent=3))
		#return info
		return SearchSchema(info)
				
	def listTableColumns(self, table, descriptions=False, enums=False):
		''' List the columns in a table. More compact and practical for many purposes compared with listTableInfo '''
		schema = self.listTableInfo(table).schema
		if self.debug: print(json.dumps(schema, indent=3))
		for c, v in schema['data_model']['properties'].items():
			print (c)
			if descriptions:
				if 'description' in v: print (v['description'])
				if '$comment' in v: print (v['$comment'])
			if enums:
				if 'oneOf' in v:
					for c in v['oneOf']:
						print ('\t\t{}'.format(c['const']))
				if '$comment' in v: print (v['$comment'])
			print('_______________________________________')
			
	def listColumnInfo(self, table, verbose=False):
		url = "{}/table/{}/info".format(self.hostURL,table)
		response = requests.get(url, headers=self.headers)
		info = json.loads(response.text)
		if verbose:
			print ("_Schema for table{}_".format(table))
			print(json.dumps(info, indent=3))
		return info

	def getMappingTemplate(self, table, propList=None):
		''' Get an empty template in which to create  mappings for property values 
		:param table: table for which to generate a mapping template
		:param propList: optional list of properties to include in the map
		'''
		schema = self.listTableInfo(table).schema
		template = {}
		for prop, details in schema['data_model']['properties'].items():
			if propList == None or prop in propList:
				if 'oneOf' in details:
					vList = {}
					for v in details['oneOf']:
						vList[v['const']] = 'replaceThis'
						#if titles:
						#	vList[v['const']]['title'] = v['title']
					template[prop] = vList
		return template
			

	def runOneTableQuery(self, column_list, table, limit):
		col_string = ", ".join(column_list)

		query = "select {columns} from {table} limit {results}".format(columns=col_string,
																table=table, results=limit)
		res = self.runQuery(query, returnType='dataframe')
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
			print ("____Page{}_______________".format(pageCount))
			if pageCount == 1:
				response = requests.request("POST", next_url,
				 headers=self.headers, data = query2)
			else:
				response = requests.request("GET", next_url)
			if self.debug: print(response.content)
			result = (response.json())
			if self.debug:
				pprint.pprint(result)
			if 'pagination' in result and 'next_page_url' in result['pagination']:
				next_url = result['pagination']['next_page_url']
			else:
				next_url = None
			if returnType == 'json':
				resultRows += result['data']
			else:
				for r in result['data']:
					resultRows.append([*r.values()])
				
			if 'data_model' in result:
				if self.debug: print('found data model')
				column_list = result['data_model']['properties'].keys()

		if returnType == 'dataframe':
			df = pd.DataFrame(resultRows, columns=column_list, index=None)
			return df
		else:
			return resultRows

	def query2Frame(self, query):
		return self.runQuery(query, returnType='dataframe')
	
class SearchSchema():
	''' A table schema '''	
	def __init__(self, table_info ):
		self.schema = table_info
	
	def getCol(self, colName):
		if colName not in self.schema['data_model']['properties']:
			print('No column named {}'.format(colName))
		print(json.dumps(self.schema['data_model']['properties'][colName], indent=3))
		
	def getcaDSRDefinition(self, ref):
		
		from urllib.request import urlopen
		from xml.etree.ElementTree import parse
		metaresolverURL = 'http://identifiers.org/{}'.format(ref)
		var_url = urlopen(metaresolverURL)
		xmldoc = parse(var_url)

		root = xmldoc.getroot()
		requiredFields=['publicID','version','dateCreated','dateModified','longName',
                'preferredDefinition','preferredName', 'registrationStatus']

		requiredLinks=['valueDomain','dataElementConcept']
		caDSRrep = {}
		for item in root.findall('./queryResponse/class/field'):
			fName = item.get('name')
			if fName in requiredFields:
				caDSRrep[fName]=item.text
			if fName in requiredLinks:
				caDSRrep[fName]=item.get('{http://www.w3.org/1999/xlink}href')

		return caDSRrep


def usage():
	print (sys.argv[0] +' -l listTables -c listCatalog -t tableInfo -r registeredServices')

def main(argv):
	searchClient = DataConnectClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com')

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
	        ti = searchClient.listTableInfo(arg)
	    elif opt in ("-a", "--catalogs"):
	        searchClient.listCatalogs()
	    elif opt in ("-r", "--registeredServices"):
	        DataConnectClient.getRegisteredSearchServices()


if __name__ == "__main__":
    main(sys.argv[1:])



	#query = "select submitter_id, 'bdc:'||read_drs_id drsid from thousand_genomes.onek_genomes.ssd_drs where population = 'BEB' limit 3"
# 	res = myClient.runQuery(query)


	#searchClient.listTables()