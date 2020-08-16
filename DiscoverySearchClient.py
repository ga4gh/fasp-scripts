import requests
#import pprint

class DiscoverySearchClient:

	def __init__(self, hostURL ):
		self.hostURL = hostURL


	def runQuery(self, query):
	
		query2 = "{\"query\":\""+query+"\"}"
		headers = {
			'content-type': 'application/json'
		}

		next_url = self.hostURL + "search"

		pageCount = 0
		resultRows = []
		print ("_Retrieving the query_")
		while next_url != None :
			pageCount += 1
			print ("____Page{}_______________".format(pageCount))
			if pageCount == 1:
				response = requests.request("POST", next_url,
				 headers=headers, data = query2)
			else:
				 response = requests.request("GET", next_url)
			result = (response.json())
			#pprint.pprint(result) 
			next_url = result['pagination']['next_page_url']
			rowCount = len(result['data'])
# 			if rowCount > 0:
# 				resultRows.append(result['data'])
			for r in result['data']:
				resultRows.append([*r.values()])
		return resultRows
			
if __name__ == "__main__":
	myClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/')

	query = "select submitter_id, 'bdc:'||read_drs_id drsid from thousand_genomes.onek_genomes.ssd_drs where population = 'BEB' limit 3"
	res = myClient.runQuery(query)
	print (res)
