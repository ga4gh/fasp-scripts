import sys, os
import datetime

# a utility
from fasp.runner import FASPRunner

from fasp.search import DataConnectClient
from fasp.loc import EGAFileClient
from fasp.workflow import DNAStackWESClient
from fasp.workflow import GCPLSsamtools


import pyega3.pyega3 as ega


def main(argv):

    faspRunner = FASPRunner(pauseSecs=0)
    creditor = faspRunner.creditor
    settings = faspRunner.settings

	# Step 1 - Discovery
    # query for relevant files
    searchClient = DataConnectClient('https://publisher-data.publisher.dnastack.com/data-connect/')
    query = "SELECT sample_submitter_id, fileid, filename FROM collections.public_datasets.scr_egapancreatic_sample_multi p join collections.public_datasets.scr_egapancreatic_files f on f.sample_primary_id = p.sample_primary_id where phenotype = 'pancreatic adenocarcinoma' limit 3"
    query_job = searchClient.runQuery(query)

    # Step 2 - Use htsget at EGA
    htsgetClient = EGAFileClient('~/.keys/ega.credentials')

    # Step 3 - set up a class that run a compute for us
    location = 'projects/{}/locations/{}'.format(settings['GCPProject'], settings['GCPPipelineRegion'])
    wesClient = GCPLSsamtools(location, settings['GCPOutputBucket'])



    # repeat steps 2 and 3 for each row of the query
    for row in query_job:

        print("sample={}, EGAFileID={}".format(row[0], row[1]))

        # Step 2 - Use htsget to access the file
        fileSize = htsgetClient.getSize(row[1])
        print("File size:{}".format(fileSize))
        localfile = row[2]
        htsgetClient.htsget(row[1], 'chr1', 100000, 102000, 'BAM', localfile)

        # Step 3 - Run a pipeline on the file
        outfile = "{}.txt".format(row[0])
        pipeline_id = wesClient.runWorkflow(localfile, outfile)
        #print('submitted:{}'.format(pipeline_id))

        via = 'lsapi'
        note = 'samtools on htsget BAM'

        time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        faspRunner.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
            searchClient, htsgetClient, wesClient)


if __name__ == "__main__":
    main(sys.argv[1:])
