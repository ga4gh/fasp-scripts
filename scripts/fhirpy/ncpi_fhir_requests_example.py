import requests
import os.path
import json
import pprint
import sys
import getopt

class FHIRSearchClient:
	''' Class to call FHIR server directly as a GA4GHSearch-like client
	This does not use the fhirpy library '''
	def __init__(self, hostURL, cookies, debug=False ):
		self.hostURL = hostURL
		self.debug = debug
		self.headers = {
			'content-type': 'application/json'
		}
		self.cookies = cookies
			
	def runQuery(self, query):


		next_url = "{}/Patient?gender={}".format(self.hostURL, query)
		pageCount = 0
		#resultRows = []
		print ("_Retrieving the query_")
		if self.debug: print(self.cookies)
		while next_url != None :
			if self.debug:
				print(next_url)
			pageCount += 1
			print ("____Page{}_______________".format(pageCount))

			response = requests.request("GET", next_url, cookies=self.cookies)
			if self.debug:
				print(response.content)
			result = (response.json())
			if self.debug:
				print(result)
			if 'link' in result :
				nxt = next((sub for sub in result['link'] if sub['relation'] == 'next'), None)
				if nxt == None:
					next_url = None
				else:
					next_url = nxt['url']
			else:
				next_url = None
			for t in result['entry']:
				print('patient id :',t['resource']['id'])
# 			if rowCount > 0:
# 				resultRows.append(result['data'])
#			for r in result['data']:
#				resultRows.append([*r.values()])
#		return resultRows



	def listResources(self):
		
		
		next_url = self.hostURL + "/StructureDefinition"


		pageCount = 0
		resultRows = []
		print ("_Retrieving the resource list_")
		while next_url != None :
			if self.debug:
				pprint.pprint(next_url)
			pageCount += 1
			print ("____Page{}_______________".format(pageCount))
			#response = requests.get(next_url, headers=self.headers)
			response = requests.get(next_url, cookies=self.cookies)
			if self.debug:
				print(response.content)
			result = (response.json())
			
			if 'link' in result :
				nxt = next((sub for sub in result['link'] if sub['relation'] == 'next'), None)
				next_url = nxt['url']
			else:
				next_url = None
			for t in result['entry']:
				print(t['fullUrl'])
		return 


def usage():
	print (sys.argv[0] +' -l listResources  -r runQuery')


def main(argv):
	
	endpoint = 'https://ncpi-api-fhir-service-dev.kidsfirstdrc.org'
	full_cookie_path = os.path.expanduser('~/.keys/kf_cookies.json')
	print(full_cookie_path)
	with open(full_cookie_path) as f:
			cookies = json.load(f)
	searchClient = FHIRSearchClient(endpoint, cookies)
		
	try:
		opts, args = getopt.getopt(argv, "hlr:", ["help", "listResources",  "runQuery"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
	    if opt in ("-h", "--help"):
	        usage()
	        sys.exit()
	    elif opt in ("-l", "--listTables"):
	    	searchClient.listResources()
	    elif opt in ("-r", "--runQuery"):
	    	searchClient.runQuery(arg)


	

			

if __name__ == "__main__":
    main(sys.argv[1:])
			
	



