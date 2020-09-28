import sys, os
import datetime

# The implementations we're using

from DiscoverySearchClient import DiscoverySearchClient
from DNAStackWESClient import DNAStackWESClient

from FASPLogger import FASPLogger

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
        ega.download_file_retry(self.credentials, identifier, display_file_name, file_name, file_size, check_sum, 3, self.key,
        saveTo, genomic_range_args, -1, 10)


def main(argv):

    # Step 1 - Discovery
    # query for relevant files
    searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/')
    query = "SELECT sample_submitter_id, fileid, filename FROM dbgap_demo.scr_ega.scr_egapancreatic_sample_multi p join dbgap_demo.scr_ega.scr_egapancreatic_files f on f.sample_primary_id = p.sample_primary_id where phenotype = 'pancreatic adenocarcinoma'"
    query_job = searchClient.runQuery(query)
    
    # Step 2 - Use htsget at EGA
    htsgetClient = EGAhtsget('~/.keys/ega.credentials')
    
    # Step 3 - set up a class that run a compute for us
    wesClient = GCPLSsamtools('gs://isbcgc-216220-life-sciences/pancreatic/')
    
    # Use this to find out the name of this file, so we can log what ran the pipeline
    thisScript =  os.path.basename(__file__)
    
    # A log is helpful to keep track of the computes we've submitted
    pipelineLogger = FASPLogger("./pipelineLog.txt", os.path.basename(__file__))
    
    # repeat steps 2 and 3 for each row of the query
    for row in query_job:

        print("sample={}, EGAFileID={}".format(row[0], row[1]))
        
        # Step 2 - Use DRS to get the URL
        fileSize = htsgetClient.getSize(row[1])
        print(fileSize)
        # we've predetermined we want to use the gs copy in this case
        #url = drsClient.getAccessURL(row[1], 'gs')
        htsgetClient.htsget(row[1], 'chr1', 100000, 102000, 'BAM', row[2])

        # Step 3 - Run a pipeline on the file at the drs url
        outfile = "{}.txt".format(row[0])
        pipeline_id = wesClient.runWorkflow(row[2], outfile)
        #print('submitted:{}'.format(pipeline_id))
        
        via = 'local'
        note = 'samtools on htsget BAM'

        time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        pipelineLogger.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
            searchClient, htsgetClient, wesClient)
        
    
if __name__ == "__main__":
    main(sys.argv[1:])
    