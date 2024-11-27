#  IMPORTS
import sys
import datetime


# a utility
from fasp.runner import FASPRunner

# The implementations we're using
from fasp.search import DataConnectClient
from fasp.loc import DRSMetaResolver
from fasp.workflow import DNAStackWESClient


def main(argv):

	faspRunner = FASPRunner(pauseSecs=0)
	creditor = faspRunner.creditor

	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = DataConnectClient('https://publisher-data.publisher.dnastack.com/data-connect/', debug=False)

	query = "SELECT file_name, compact_drs_id, hostbased_drs_id, drs_id from collections.public_datasets.onek_genomes_onek_recal_variants_drs where chromosome = 'chr21' and annotated = false"
	print(query)

	query_job = searchClient.runQuery(query)  # Send the query
	creditor.creditClass(searchClient)

	# Step 2 - DRS - use the MetaResolver send drs ids to the right service
	drsResolver = DRSMetaResolver(getReg=False)

	# Step 3 - set up a class that run a compute for us
	wesClient = DNAStackWESClient('~/.keys/dnastack_wes_credentials.json')

	# repeat steps 2 and 3 for each row of the query
	# this example should find id's for the same file in both BioDataCatalyst and Anvil
	for row in query_job:
		drs_id = row[1]
		print("vcffile={}, compact drsID={}".format(row[0], drs_id))

		# Step 2 - Use DRS to get the URL
		objInfo = drsResolver.getObject(drs_id)
		drsClient, localid = drsResolver.getClient(drs_id)
		print(drsClient)
		creditor.creditClass(drsClient)
		fileSize = objInfo['size']

		vcfurl = drsResolver.getAccessURL(drs_id, 'gs')
		# Step 3 - Run a pipeline on the file at the drs url
		pipeline_id = wesClient.runGWASWorkflow(vcfurl, 'gs://dnastack-public-bucket/thousand_genomes_meta.csv')
		creditor.creditClass(wesClient)
		print('submitted:{}'.format(pipeline_id))

		outfile = ''
		via = 'WES'
		note = 'GWAS'

		time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		faspRunner.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
			searchClient, drsClient, wesClient)


if __name__ == "__main__":
	main(sys.argv[1:])

















