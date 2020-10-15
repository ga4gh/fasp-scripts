#  IMPORTS
import sys 

# a utility 
from fasp.runner import FASPRunner

# The implementations we're using
from fasp.loc import crdcDRSClient
from fasp.workflow import samtoolsSBClient
from fasp.search import BigQuerySearchClient



def main(argv):

	faspRunner = FASPRunner(pauseSecs=0)

	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = BigQuerySearchClient()

	query = """
     	SELECT 'case_'||associated_entities__case_gdc_id , file_id
		FROM `isb-cgc.GDC_metadata.rel24_fileData_active` 
		where data_format = 'BAM' 
		and project_disease_type = 'Breast Invasive Carcinoma'
		limit 3"""
	
	drsClient = crdcDRSClient('~/.keys/CRDCAPIKey.json', 's3')

	# Step 3 - set up a class that runs samtools for us
	sbProject = faspRunner.settings['SevenBridgesProject']
	sbInst = faspRunner.settings['SevenBridgesInstance']
	mysam = samtoolsSBClient(sbInst, sbProject)
	
	faspRunner.configure(searchClient, drsClient, mysam)
		
	faspRunner.runQuery(query, 'GDC query SB compute')
	
if __name__ == "__main__":
	main(sys.argv[1:])


	
	

	
	









