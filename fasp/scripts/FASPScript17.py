#  IMPORTS
import sys
import datetime
import json

# a utility 
from fasp.runner import FASPRunner

# The implementations we're using
from fasp.workflow import GCPLSsamtools
from fasp.search import BigQuerySearchClient
from fasp.loc.drs_metaresolver import crdcDRSClient, anvilDRSClient

class localSearchClient:
	
	def __init__(self):
		# edit the following for your local copy of the manifest file
		with open('../data/gtex/gtex-cram-manifest.json') as f:
			self.data = json.load(f)
			
	def runQuery(self, query):
		# return the first three records
		# edit this once your ready to run this on all the files
		results = []
		for f in self.data[20:23]:
			drsid = 'anv:'+f['object_id']
			results.append([f['file_name'], drsid ])
		return  results

def main(argv):

	
	faspRunner = FASPRunner(pauseSecs=0)
	settings = faspRunner.settings
	
	# Step 1 - Discovery
	# query for relevant DRS objects
	discoveryClients = {
		"crdc": BigQuerySearchClient(),
		"anv": localSearchClient()
	}


	# TCGA Query - CRDC
	crdcquery = """
     	SELECT 'case_'||associated_entities__case_gdc_id , 'crdc:'||file_id
		FROM `isb-cgc.GDC_metadata.rel24_fileData_active` 
		where data_format = 'BAM' 
		and project_disease_type = 'Breast Invasive Carcinoma'
		limit 3"""		
		

	results = discoveryClients['anv'].runQuery('')  # Send the query
	results += discoveryClients['crdc'].runQuery(crdcquery) 
	

	# Step 2 - DRS - set up DRS Clients	
		# Step 2 - DRS - set up DRS Clients	
	drsClients = {
		"crdc": crdcDRSClient('~/.keys/crdc_credentials.json', 'gs'),
		"anv": anvilDRSClient('~/.keys/anvil_credentials.json', settings['GCPProject'], 'gs')
	}

		
		
	# Step 3 - set up a class that runs samtools for us
	# providing the location for the results
	location = 'projects/{}/locations/{}'.format(settings['GCPProject'], settings['GCPPipelineRegion'])
	wesClient = GCPLSsamtools(location, settings['GCPOutputBucket'])

	
	# repeat steps 2 and 3 for each row of the query
	for row in results:

		print("subject={}, drsID={}".format(row[0], row[1]))
		resRow = [row[0], row[1]]
		# Step 2 - Use DRS to get the URL
		# get the prefix
		prefix, drsid = row[1].split(":", 1)
		drsClient = drsClients[prefix]
		print ('Sending id {} to {}'.format(drsid, drsClient.__class__.__name__))
		url = drsClient.getAccessURL(drsid)
		print(url)
		objInfo = drsClient.getObject(drsid)
		#print (objInfo)
		fileSize = objInfo['size']
		#fileSize = 0
				
		# Step 3 - Run a pipeline on the file at the drs url
		if url != None:
			outfile = "{}.txt".format(row[0])
			via = 'sh'
			note = 'GTEx and TCGA'
			time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
			run_id = wesClient.runWorkflow(url, outfile)
			searchClient = discoveryClients[prefix]
			faspRunner.logRun(time, via, note,  run_id, outfile, fileSize,
				searchClient, drsClient, wesClient)
			resRow.append('OK')
		else:
			print('could not get DRS url')
			resRow.append('unauthorized')

if __name__ == "__main__":
	main(sys.argv[1:])
