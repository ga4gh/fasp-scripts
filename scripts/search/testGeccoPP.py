import requests
import pprint

query = "select id from collections.public_datasets.public_gecco_phenopackets where json_extract_scalar(phenopacket, '$.subject.sex') = 'MALE' limit 3"

payload = "{\"query\":\"" + query + "\"}"
payload = {'query':query}

headers = {
  'content-type': 'application/json'
}

next_url = "https://data.publisher.dnastack.com/data-connect/search"

pageCount = 0
while next_url != None :
	pageCount += 1
	print ("____Page{}_______________".format(pageCount))
	if pageCount == 1:
		#requests.post(next_url, json=payload)
		response = requests.request("POST", next_url, headers=headers, data=payload)

	else:
		response = requests.get(next_url)
	result = (response.json())
	pprint.pprint(result)
	if 'pagination' in result and 'next_page_url' in result['pagination']:
		next_url = result['pagination']['next_page_url']
	else:
		next_url = None

