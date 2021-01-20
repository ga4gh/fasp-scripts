import sys
import datetime

# a utility 
from fasp.runner import FASPRunner

# The implementations we're using
from fasp.loc import sdlDRSClient
from fasp.search import BigQuerySearchClient
from fasp.workflow import DNAStackWESClient


def main(argv):

	faspRunner = FASPRunner(pauseSecs=0)
	
	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = BigQuerySearchClient()
	query = """SELECT sra.biosample, sra.acc||'.cram'
		FROM `isbcgc-216220.GECCO_CRC_Susceptibility.Subject_Phenotypes` sp
		join `isbcgc-216220.GECCO_CRC_Susceptibility.Sample_MULTI` sm on
		sm.dbgap_subject_id = sp.dbgap_subject_id
		join `nih-sra-datastore.sra.metadata` sra on sm.BioSample_Accession = sra.biosample
		where AGE between 45 and 55 and sex = 'Female' limit 3"""
	query_job = searchClient.runQuery(query)
	
	# Step 2 - DRS - set up a DRS Client
	# CRDC
	drsClient = sdlDRSClient('~/.keys/prj_14565.ngc', True)
	
	# Step 3 - set up a class that run a compute for us
	wesClient = DNAStackWESClient('~/.keys/dnastack_wes_credentials.json')
	
	# repeat steps 2 and 3 for each row of the query
	for row in query_job:

		print("sample={}, drsID={}".format(row[0], row[1]))
		
		# Step 2 - Use DRS to get the URL
		objInfo = drsClient.getObject(row[1])
		fileSize = objInfo['size']
		print(fileSize)
		# we've predetermined we want to use the gs copy in this case
		#url = drsClient.getAccessURL(row[1], 'gs')
		res = drsClient.getAccessURL(row[1],'gs.us')
		url = res['url']
		print(url)
		# Step 3 - Run a pipeline on the file at the drs url
		outfile = "{}.txt".format(row[0])
		pipeline_id = wesClient.runWorkflow(url, outfile)
		print('submitted:{}'.format(pipeline_id))
		
		via = 'WES'
		note = 'WES MD5 on NCBI SDL'

		time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		faspRunner.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
			searchClient, drsClient, wesClient)


if __name__ == "__main__":
	main(sys.argv[1:])
