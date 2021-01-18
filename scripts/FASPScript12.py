import sys, os
import datetime

# a utility 
from fasp.runner import FASPRunner

from fasp.search import DiscoverySearchClient
from fasp.workflow import DNAStackWESClient
from fasp.workflow import GCPLSsamtools


import pyega3.pyega3 as ega

class EGAhtsget():
    
    def __init__(self, credentialsPath):
        *credentials, self.key = ega.load_credential(os.path.expanduser(credentialsPath))
        self.credentials = credentials
        self.token = ega.get_token(credentials)
    
    def getSize(self, identifier):
        display_file_name, file_name, file_size, check_sum = ega.get_file_name_size_md5(self.token, identifier) 
        return file_size
        
    def htsget(self, identifier, ref, start, end, type, saveTo ):
        display_file_name, file_name, file_size, check_sum = ega.get_file_name_size_md5(self.token, identifier) 
        genomic_range_args = (ref, check_sum, start, end, type)
        print(display_file_name)
        print(genomic_range_args)
        ega.download_file_retry(self.credentials, identifier, display_file_name, file_name, file_size, check_sum, 3, self.key,
        saveTo, genomic_range_args, -1, 10)


def main(argv):

    faspRunner = FASPRunner(pauseSecs=0)
    creditor = faspRunner.creditor
    settings = faspRunner.settings
	
	# Step 1 - Discovery
    # query for relevant files
    searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/')
    query = "SELECT sample_submitter_id, fileid, filename FROM dbgap_demo.scr_ega.scr_egapancreatic_sample_multi p join dbgap_demo.scr_ega.scr_egapancreatic_files f on f.sample_primary_id = p.sample_primary_id where phenotype = 'pancreatic adenocarcinoma' limit 3"
    query_job = searchClient.runQuery(query)
    
    # Step 2 - Use htsget at EGA
    htsgetClient = EGAhtsget('~/.keys/ega.credentials')
    
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
    