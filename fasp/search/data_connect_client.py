import requests
import sys
import getopt
import json

from fasp.loc import GA4GHRegistryClient
#from fasp.search.MappingLibrary import MappingLibraryClient
import pandas as pd

class DataConnectClient:
	""" A wrapper class around the 
	"""

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
			#serviceType=service['type']
			print(json.dumps(service, indent=3))
			#serviceURL = service['url']
			#hostname = serviceURL.split("/")[2]

		return None

	def _url_format(self, url):
		url = str(url)
		if url.endswith('/'):
			url = url[:-1]
		return url

	def list_tables(self, requestedCatalog=None, verbose=True):

		tables = []

		if requestedCatalog == None:
			next_url = self.hostURL + "/tables"
		else:
			next_url = "{}{}{}".format(self.hostURL,'/tables/catalog/',requestedCatalog)

		pageCount = 0
		if verbose:
			print("Retrieving the table list")
		while next_url != None :
			pageCount += 1
			if verbose:
				print ("____Page{}_______________".format(pageCount))
			if self.debug:
				print(f'Retrieving {next_url}')
			response = requests.get(next_url, headers=self.headers)
			result = (response.json())
			if self.debug:
				print(json.dumps(result, indent=3))
			if requestedCatalog == None and 'pagination' in result and 'next_page_url' in result['pagination']:
				next_url = result['pagination']['next_page_url']
			else:
				next_url = None
			for t in result['tables']:
				if verbose:
					print(t['name'])
				tables.append(t['name'])

		return tables

	def list_catalogs(self):
		url = self.hostURL + "/tables"

		print ("Retrieving the catalog list")
		response = requests.get(url, headers=self.headers)
		result = (response.json())
		for t in result['index']:
			print(t['description'])
		return


	def list_catalog(self, catalog):
		return self.list_tables(catalog)

	def list_table_info(self, table, verbose=False):
		url = "{}/table/{}/info".format(self.hostURL,table)
		response = requests.get(url, headers=self.headers)
		info = json.loads(response.text)
		if verbose:
			print ("_Schema for table{}_".format(table))
			print(json.dumps(info, indent=3))
		#return info
		return SearchSchema(info)
				
	def list_table_columns(self, table, descriptions=False, enums=False):
		''' List the columns in a table. More compact and practical for many purposes compared with list_table_info '''
		schema = self.list_table_info(table).schema
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
			
	def list_column_info(self, table, verbose=False):
		url = "{}/table/{}/info".format(self.hostURL,table)
		response = requests.get(url, headers=self.headers)
		info = json.loads(response.text)
		if verbose:
			print ("_Schema for table{}_".format(table))
			print(json.dumps(info, indent=3))
		return info

	def get_mapping_template(self, table, propList=None):
		''' Get an empty template in which to create  mappings for property values 
		:param table: table for which to generate a mapping template
		:param propList: optional list of properties to include in the map
		'''
		schema = self.list_table_info(table).schema
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
			

	def get_decode_template(self, table, propList=None, numericCodes=True):
		''' Get a template which maps enumerated codes to their decoded values 
		:param table: table for which to generate a mapping template
		:param propList: optional list of properties to include in the map
		:param numericCodes: return codes as integers - will fail if the codes are not
		'''
		schema = self.list_table_info(table).schema
		template = {}
		for prop, details in schema['data_model']['properties'].items():
			if propList == None or prop in propList:
				if 'oneOf' in details:
					vList = {}
					for v in details['oneOf']:
						if numericCodes:
							vList[int(v['const'])] = v['title']
						else:
							vList[v['const']] = v['title']
						#if titles:
						#	vList[v['const']]['title'] = v['title']
					template[prop] = vList
		return template

		
	def runOneTableQuery(self, column_list, table, limit):
		col_string = ", ".join(column_list)

		query = "select {columns} from {table} limit {results}".format(columns=col_string,
																table=table, results=limit)
		res = self.run_query(query, returnType='dataframe')
		return res

	def getDataFrameFromTable(self, table, column_list=[], limit=1000):
		if isinstance(column_list, list):
			if len(column_list) == 0:
				column_list = '*'
			else:
				column_list.join(',')
		query = f"select {column_list} from {table} limit {limit}"
		print (query)
		res = self.run_query(query, returnType='dataframe')
		if res.shape[0] >= limit:
			print(f'The number of rows was limited to {limit}. Try setting limit=your_value if you need more data')
		return res

	def run_query(self, query, returnType=None, progessIndicator=None):

		query = query.replace("\n", " ").replace("\t", " ")
		query = query.strip()
		query2 = "{\"query\":\"%s\", \"parameters\":[]}" % query
		if self.debug:
			print("Query: {}".format(query2))
			
		next_url = self.hostURL + "/search"

		pageCount = 0
		resultRows = []
		column_list = []
		if not progessIndicator:
			print ("Retrieving the query")
		while next_url != None :
			pageCount += 1
			if progessIndicator:
				progessIndicator.value += 1
			else:
				print ("____Page{}_______________".format(pageCount))
			if pageCount == 1:
				response = requests.request("POST", next_url,
				 headers=self.headers, data = query2)
			else:
				response = requests.request("GET", next_url)
			if self.debug: print(response.content)
			result = (response.json())
			if self.debug:
				print(json.dumps(result, indent=3))
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

		if progessIndicator:
			progessIndicator.value = progessIndicator.max
		
		if returnType == 'dataframe':
			df = pd.DataFrame(resultRows, columns=column_list, index=None)
			return df
		else:
			return resultRows

	def run_param_query(self, query, returnType=None, progessIndicator=None):

		query_text = query['query'].replace("\n", " ").replace("\t", " ")
		query_text = query_text.strip()
		#query2 = "{\"query\":\"%s\"}" % query
		query2 = {"query":query_text, "parameters":query['parameters']}
		if self.debug:
			print("Query: {}".format(query2))
		#query2 = query
		next_url = self.hostURL + "/search"

		pageCount = 0
		resultRows = []
		column_list = []
		if not progessIndicator:
			print ("Retrieving the query")
		while next_url != None :
			pageCount += 1
			if progessIndicator:
				progessIndicator.value += 1
			else:
				print ("____Page{}_______________".format(pageCount))
			if pageCount == 1:
				#response = requests.request("POST", next_url,
				 #headers=self.headers, data = query2)
				response = requests.post(next_url, json = query2)
			else:
				response = requests.request("GET", next_url)
			if self.debug: print(response.content)
			result = (response.json())
			if self.debug:
				print(json.dumps(result, indent=3))
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

		if progessIndicator:
			progessIndicator.value = progessIndicator.max
		
		if returnType == 'dataframe':
			df = pd.DataFrame(resultRows, columns=column_list, index=None)
			return df
		else:
			return resultRows

	def query2Frame(self, query):
		return self.run_query(query, returnType='dataframe')
	
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
	print (sys.argv[0] +' -s service -l listTables -c listCatalog -t tableInfo -r registeredServices')

def main(argv):

	try:
		opts, args = getopt.getopt(argv, "hls:c:t:ra", ["help", "listTables", "service", "tableInfo", "registeredServices","catalogs"])
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit(2)
	searchClient = None
	for opt, arg in opts:
	    if opt == '-s':
	    	searchClient = DataConnectClient(arg, debug=True)
	if searchClient == None:
		print("-s service must be provided")
		usage()
		sys.exit()
	for opt, arg in opts:
	    if opt in ("-h", "--help"):
	        usage()
	        sys.exit()
	    elif opt in ("-l", "--listTables"):
	        searchClient.list_tables(verbose=True)
	    elif opt in ("-c", "--listCatalog"):
	        searchClient.list_catalog(arg)
	    elif opt in ("-t", "--table"):
	        ti = searchClient.list_table_info(arg, verbose=True)
	    elif opt in ("-a", "--catalogs"):
	        searchClient.list_catalogs()
	    elif opt in ("-r", "--registeredServices"):
	        DataConnectClient.getRegisteredSearchServices()


if __name__ == "__main__":
    main(sys.argv[1:])

