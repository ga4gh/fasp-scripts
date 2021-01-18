#  IMPORTS

import datetime
import sys

# a utility 
from fasp.runner import FASPRunner

# The implementations we're using
from fasp.workflow import GCPLSsamtools
from fasp.search import BigQuerySearchClient
from fasp.search import Gen3ManifestClient
from fasp.loc.drs_metaresolver import crdcDRSClient, anvilDRSClient

	

def main(argv):

	
	faspRunner = FASPRunner()
	settings = faspRunner.settings
	
	# Step 1 - Discovery
	# query for relevant DRS objects
	discoveryClients = {
		"crdc": BigQuerySearchClient(),
		"anv": Gen3ManifestClient('./fasp/data/gtex/gtex-cram-manifest_wCuries.json')
	}


	# TCGA Query - CRDC
	crdcquery = """
     	SELECT 'case_'||associated_entities__case_gdc_id , 'crdc:'||file_id
		FROM `isb-cgc.GDC_metadata.rel24_fileData_active` 
		where data_format = 'BAM' 
		and project_disease_type = 'Breast Invasive Carcinoma'
		limit 3"""		
		

	# Run both queriues abd aggregate results
	results = discoveryClients['anv'].runQuery(3)  # Send the query
	results += discoveryClients['crdc'].runQuery(crdcquery) 
	

	# Step 2 - DRS - set up DRS Clients	
	# TODO Use DRSMetaresolver so we don't have to build our own resolver in this code	
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
		# This is a local solution to resolve prefixed DRS ids, DRS Metarolver would be better
		# get the prefix

		prefix, drsid = row[1].split(":", 1)
		drsClient = drsClients[prefix]
		print ('Sending id {} to {}'.format(drsid, drsClient.__class__.__name__))
		
		url = drsClient.getAccessURL(drsid)
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
